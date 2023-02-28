import logging

from aiohttp import web

from valet import database
from valet.modules.web.views import routes
from valet.settings import load_config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def setup_app(app: web.Application) -> None:
    config = load_config('config/config.toml')
    engine = await database.get_engine()

    app['config'] = config
    app['engine'] = engine


async def teardown_app(app: web.Application) -> None:
    engine = app['engine']
    await engine.dispose()


async def make_app() -> web.Application:
    app = web.Application()
    app.on_startup.append(setup_app)
    app.on_cleanup.append(teardown_app)
    app.add_routes(routes)
    return app
