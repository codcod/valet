"""
Global middleware.

https://slack.dev/bolt-python/concepts#global-middleware
"""
from valet.database import get_engine
from valet.logging import get_logger

logger = get_logger(__name__)


async def insert_db_engine(client, context, logger, payload, next):
    """
    Put database engine in the context and dispose it after the call.
    """
    engine = await get_engine()
    context['engine'] = engine
    logger.debug(f'Engine put in context {engine=}')

    await next()

    await engine.dispose()
