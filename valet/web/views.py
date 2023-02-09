from datetime import datetime as dt

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from valet import db
from valet.json import dumps

routes = web.RouteTableDef()


@routes.get('/')
async def index(req: Request) -> Response:
    engine = req.app['engine']

    async with engine.begin() as conn:
        records = await db.select_requestors(conn, dt(2023, 1, 2).date())

    return web.json_response({'rows': list(records)}, dumps=dumps)
