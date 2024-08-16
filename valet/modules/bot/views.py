import typing as tp

from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.context.async_context import AsyncBoltContext
from sqlalchemy.ext.asyncio import AsyncEngine

from valet.lib import date
from valet.logging import get_logger
from valet.modules.bot import queries as db

logger = get_logger(__name__)


async def command_parking(
    ack: AsyncAck, body: dict[str, tp.Any], context: AsyncBoltContext, respond
):
    slack_id = body['user_id']
    parking_day = date.to_date(body['text'])

    engine: AsyncEngine = context['engine']

    async with engine.connect() as conn:
        user_id = await db.find_by_slack_id(conn, slack_id)
        await db.insert_request(conn, user_id, parking_day)

    await ack(
        f'Request made by <@{slack_id}> ({user_id=}) for {parking_day} has been placed'
    )


async def fetch_standing_requests(context, event):
    slack_id = event['user']

    engine = context['engine']
    async with engine.connect() as conn:
        user_id = await db.find_by_slack_id(conn, slack_id)
        rows = await db.user_standing_requests(conn, user_id)

    requests = []
    for r in rows:
        requests.append(
            {
                'parking_day': r._mapping['parking_day'],
                'status': r._mapping['status'],
            }
        )

    return requests


async def create_sections(requests):
    blocks = []
    for request in requests:
        parking_day, status = request.values()
        blocks.append(
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'*{status}*\n{parking_day}',
                },
                'accessory': {
                    'type': 'button',
                    'text': {'type': 'plain_text', 'text': 'Cancel'},
                    'action_id': 'cancel_request',
                    'value': f'{parking_day}',
                },
            }
        )
    return blocks


async def update_home_tab(client, event, context):
    logger.debug('**** APP HOME OPENED')

    requests = await fetch_standing_requests(context, event)
    blocks = await create_sections(requests)

    try:
        await client.views_publish(
            user_id=event['user'],
            # view=await views.view_home_tab(),
            view={'type': 'home', 'blocks': blocks},
        )
    except Exception as e:
        # logger.error(f'Error publishing home tab: {e}')
        print(f'Error publishing home tab: {e}')


async def handle_cancel_request(ack, body, context, client):
    await ack()

    slack_id = body['user']['id']
    parking_day = date.to_date(body['actions'][0]['value'])

    logger.debug(f'Cancelling request on {parking_day} on behalf of {slack_id}')

    engine: AsyncEngine = context['engine']
    async with engine.connect() as conn:
        user_id = await db.find_by_slack_id(conn, slack_id)
        await db.cancel_request(conn, user_id, parking_day)

    event = {'user': slack_id}
    await update_home_tab(client, event, context)


async def handle_datepicker(ack, body, logger):
    await ack()
    logger.debug(f'************* {body=}')
