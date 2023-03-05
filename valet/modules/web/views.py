from datetime import datetime as dt

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from valet.lib.json import dumps
from valet.modules.web import queries as db

routes = web.RouteTableDef()


@routes.get('/')
async def index(req: Request) -> Response:
    engine = req.app['engine']

    async with engine.begin() as conn:
        records = await db.requestors_for_given_day(conn, dt(2023, 1, 2).date())

    return web.json_response({'rows': list(records)}, dumps=dumps)
