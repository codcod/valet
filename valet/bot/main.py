import logging

from slack_bolt.async_app import AsyncApp
from valet.settings import load_config, BASE_DIR


logging.basicConfig(level=logging.DEBUG)
config = load_config(BASE_DIR / '.instance/slack-config.toml')['slack']


app = AsyncApp(token=config['TOKEN'], signing_secret=config['SIGNING_SECRET'])


def app_factory():
    return app.web_app(path='/slack/events')


@app.event('app_mention')
async def event_test(body, say, logger):
    logger.info(body)
    await say('What\'s up?')


@app.command('/parking')
# or app.command(re.compile(r'/hello-.+'))(test_command)
async def parking(ack, body):
    print('*** PARKING HANDLER')
    print(body['text'])
    user_id = body['user_id']
    await ack(f'Hi <@{user_id}>!')


@app.event('app_home_opened')
async def update_home_tab(client, event, logger):
    print('**** APP HOME OPENED')
    try:
        # views.publish is the method that your app uses to push a view to the Home tab
        await client.views_publish(
            # the user that opened your app's app home
            user_id=event['user'],
            # the view object that appears in the app home
            view={
                'type': 'home',
                'callback_id': 'home_view',
                # body of the view
                'blocks': [
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': '*Welcome to your _App\'s Home_* :tada:',
                        },
                    },
                    {'type': 'divider'},
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': f'This button won\'t do much for now but you can '
                            f'set up a listener for it using the `actions()` '
                            f'method and passing its unique `action_id`. See '
                            f'an example in the `examples` folder within '
                            f'your Bolt app.',
                        },
                    },
                    {
                        'type': 'actions',
                        'elements': [
                            {
                                'type': 'button',
                                'text': {'type': 'plain_text', 'text': 'Click me!'},
                            }
                        ],
                    },
                ],
            },
        )
    except Exception as e:
        logger.error(f'Error publishing home tab: {e}')
