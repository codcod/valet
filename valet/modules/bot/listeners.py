"""
Listener middleware.

https://slack.dev/bolt-python/concepts#listener-middleware
"""

from valet.modules.bot import queries as db


async def fetch_standing_requests(context, event, next):
    slack_id = event['user']

    engine = context['engine']
    async with engine.connect() as conn:
        user_id = await db.find_by_slack_id(conn, slack_id)
        rows = await db.user_standing_requests(conn, user_id)

    requests = []
    for r in rows:
        requests.append(
            {
                'parking_day': r[0],
                'status': r[1],
                'timestamp': r[2],
                'url': 'http://fake.eu',
            }
        )

    context['requests'] = requests
    await next()


async def create_sections(context, next):
    requests_blocks = []
    for request in context['requests']:
        requests_blocks.append(
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'*{request["status"]}*\n{request["parking_day"]}',
                },
                'accessory': {
                    'type': 'button',
                    'text': {'type': 'plain_text', 'text': 'Cancel'},
                    'url': request['url'],
                },
            }
        )
    context['blocks'] = requests_blocks
    await next()
