import pytest
from aiohttp_requests import requests
import json
from test_data.alaska import INFO_MESSAGE_CORRECT, INFO_MESSAGE_CURRENT


pytestmark = pytest.mark.asyncio

ALASKA_SERVER_URL = 'http://0.0.0.0:8091'


@pytest.mark.testcase_id('TC-1')
async def test_info(unit_under_test):
    """
    Summary:
        /info endpoint returns help information on Alaska service
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
    response_text = await response.text()
    assert response_text
    # Comparison to particular message is done for illustrative purpose. Usually it is a bad idea to assert text
    # equivalence because newlines or some kind of reformatting done by developers may fail otherwise valid tests.
    # I.e., following assertion raises AssertionError for info message with corrected typos and test fails:
    assert response_text == INFO_MESSAGE_CORRECT
    # And this doesn't for a current message with typos:
    #assert response_text != INFO_MESSAGE_CURRENT


@pytest.mark.testcase_id('TC-2')
async def test_no_bears_initially(unit_under_test):
    """
    Summary:
        /bear endpoint returns empty list on GET request on Alaska start
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send GET request to ALASKA_SERVER_URL/bear endpoint
    Expected result:
        Response with HTTP/200 status
        Response body contains empty JSON list
    """
    await unit_under_test()
    response = await requests.get(f'{ALASKA_SERVER_URL}/bear')
    assert response.status == 200
    response_text = await response.text()
    assert json.loads(response_text) == []


@pytest.mark.testcase_id('TC-3.1')
async def test_add_a_bear(unit_under_test):
    """
    TC-3.1
    Summary:
        You can create a bear with a POST request to /bear endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send POST request to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id from response body
         # Send GET request to ALASKA_SERVER_URL/bear
    Expected result:
        Response with HTTP/200 status
        Response body contains JSON list with an only element that describes created bear"""
    mikhail_json = {"bear_type": "BLACK", "bear_name": "Mikhail", "bear_age": 17.5}
    await unit_under_test()
    post_response = await requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status == 200
    bear_id = await post_response.text()
    mikhail_json['bear_id'] = int(bear_id)
    get_response = await requests.get(f'{ALASKA_SERVER_URL}/bear')
    response_text = await get_response.text()
    # Following assertion raises error.
    # Inconsistent behaviour: bear_name is cast to upper case. Should be discussed with stakeholders.
    assert json.loads(response_text) == [mikhail_json]


@pytest.mark.testcase_id('TC-3.2')
async def test_add_a_bear_uppercase(unit_under_test):
    """
    TC-3.2
    Summary:
        You can create a bear with a POST request to /bear endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send POST request to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id from response body
         # Send GET request to ALASKA_SERVER_URL/bear
    Expected result:
        Response with HTTP/200 status
        Response body contains JSON list with an only element that describes created bear"""
    mikhail_json = {"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 17.5}
    await unit_under_test()
    post_response = await requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status == 200
    bear_id = await post_response.text()
    mikhail_json['bear_id'] = int(bear_id)
    get_response = await requests.get(f'{ALASKA_SERVER_URL}/bear')
    response_text = await get_response.text()
    assert json.loads(response_text) == [mikhail_json]
