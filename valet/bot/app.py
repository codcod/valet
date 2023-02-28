"""
Slack bot.
"""

from slack_bolt.adapter.starlette.async_handler import AsyncSlackRequestHandler
from slack_bolt.async_app import AsyncApp
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route

from valet.logging import get_logger
from valet.settings import BASE_DIR, load_config

logger = get_logger(__name__)

config = load_config(BASE_DIR / '.instance/slack-config.toml')['slack']


async def proxy_endpoint(req: Request):
    return await app_handler.handle(req)


app = AsyncApp(token=config['TOKEN'], signing_secret=config['SIGNING_SECRET'])
app_handler = AsyncSlackRequestHandler(app)


api = Starlette(
    debug=True,
    routes=[Route('/slack/events', endpoint=proxy_endpoint, methods=['POST'])]
)


from valet.bot import routes

# def app_factory():
#     logger.debug('Web App starts from app factory')
#     return app.web_app(path='/slack/events')
