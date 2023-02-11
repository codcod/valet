"""Send message to a Slack channel.

"""

import logging
import socket
import typing as tp

from slack_sdk.errors import SlackApiError
from slack_sdk.http_retry import HttpRequest, HttpResponse, RetryHandler, RetryState
from slack_sdk.http_retry.builtin_interval_calculators import (
    BackoffRetryIntervalCalculator,
)
from slack_sdk.http_retry.jitter import RandomJitter
from slack_sdk.web.async_client import AsyncWebClient

from valet import settings

logger = logging.getLogger(__name__)


class ConnectionResetRetryHandler(RetryHandler):
    def _can_retry(
        self,
        *,
        _state: RetryState,
        _request: HttpRequest,
        _response: tp.Optional[HttpResponse] = None,
        error: tp.Optional[Exception] = None
    ) -> bool:
        # [Errno 104] Connection reset by peer
        return (
            error is not None and isinstance(error, socket.error) and error.errno == 104
        )


config = settings.load_config('.instance/slack-config.toml')['slack']

client = AsyncWebClient(
    token=config['TOKEN'],
    retry_handlers=[
        ConnectionResetRetryHandler(
            max_retry_count=1,
            interval_calculator=BackoffRetryIntervalCalculator(
                backoff_factor=0.5,
                jitter=RandomJitter(),
            ),
        )
    ],
)


async def post_message(text: str, channel: str = '#valet-test'):
    """
    Send message to a Slack channel.
    """
    response = await client.chat_postMessage(channel=channel, text=text)
    assert response["ok"]
    assert response["message"]["text"] == text
