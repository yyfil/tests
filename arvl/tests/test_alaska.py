import pytest
from aiohttp_requests import requests

pytestmark = pytest.mark.asyncio

ALASKA_SERVER_URL = 'http://0.0.0.0:8091'


async def test_info(unit_under_test):
    """
    TC-1
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send GET request to ALASKA_SERVER_URL/info endpoint
    Expected result:
        Response with HTTP/200 status
        Response body contains text that describes Alaska server functionality (body is not empty)
    """
    await unit_under_test()
    response = await requests.get(f'{ALASKA_SERVER_URL}/info')
    assert response.status == 200
    assert await response.text()
