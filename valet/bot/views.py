import typing as tp

from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.context.async_context import AsyncBoltContext
from sqlalchemy.ext.asyncio import AsyncEngine

from valet import date
from valet.bot import queries as db
from valet.logging import get_logger

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


async def update_home_tab(client, event, context):
    logger.debug('**** APP HOME OPENED')
    try:
        await client.views_publish(
            user_id=event['user'],
            # view=await views.view_home_tab(),
            view={'type': 'home', 'blocks': context['blocks']},
        )
    except Exception as e:
        # logger.error(f'Error publishing home tab: {e}')
        print(f'Error publishing home tab: {e}')


async def handle_datepicker(ack, body, logger):
    await ack()
    logger.debug(f'************* {body=}')
