"""
Listener middleware.

https://slack.dev/bolt-python/concepts#listener-middleware
"""

from valet.bot import queries as db


async def fetch_standing_requests(context, event, next):
    engine = context['engine']

    user = event['user']

    async with engine.connect() as conn:
        rows = await db.user_standing_requests(conn, id=1)

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
