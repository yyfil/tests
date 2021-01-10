import pytest
#from aiohttp_requests import requests
import requests
import json
from test_data.alaska import INFO_MESSAGE_CORRECT, INFO_MESSAGE_CURRENT, BEAR_TYPES_LIST, EMPTY_VALUE
import aiohttp
import asyncio


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
    response = requests.get(f'{ALASKA_SERVER_URL}/info')
    assert response.status_code == 200
    response_text = response.text
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
    response = requests.get(f'{ALASKA_SERVER_URL}/bear')
    assert response.status_code == 200
    response_text = response.text
    assert json.loads(response_text) == []


@pytest.mark.testcase_id('TC-3.1')
async def test_add_a_bear(unit_under_test):
    """
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
        Response body contains JSON object that describes created bear"""
    mikhail_json = {"bear_type": "BLACK", "bear_name": "Mikhail", "bear_age": 17.5}
    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 200
    bear_id = post_response.text
    mikhail_json['bear_id'] = int(bear_id)
    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
    response_text = get_response.text
    # Following assertion raises error.
    # Inconsistent behaviour: bear_name is cast to upper case. Should be discussed with stakeholders.
    assert json.loads(response_text) == mikhail_json


@pytest.mark.testcase_id('TC-3.2')
async def test_add_a_bear_uppercase(unit_under_test):
    """
    Summary:
        You can create a bear with a POST request to /bear endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send POST request to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id from response body
         # Send GET request to ALASKA_SERVER_URL/bear/<bear_id>
    Expected result:
        Response with HTTP/200 status
        Response body contains JSON object that describes created bear"""
    mikhail_json = {"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 17.5}
    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 200
    bear_id = post_response.text
    mikhail_json['bear_id'] = int(bear_id)
    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
    response_text = get_response.text
    assert json.loads(response_text) == mikhail_json


@pytest.mark.parametrize('bear_type', BEAR_TYPES_LIST)
@pytest.mark.testcase_id('TC-4')
async def test_modify_bear_type(unit_under_test, bear_type):
    """
    Summary:
        You can modify bear's ензу with a PUT request to /bear/<bear_id> endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send POST request to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id from response body
         # Send PUT request to ALASKA_SERVER_URL/bear/<bear_id> endpoint with JSON that contains modified bear_type
         field
         # Send GET request to ALASKA_SERVER_URL/bear/<bear_id> endpoint
    Expected result:
        Response with HTTP/200 status
        Response body contains JSON object that describes a bear with modified bear type"""
    mikhail_json = {"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 17.5}
    update_json = {"bear_type": bear_type, "bear_name": "MIKHAIL", "bear_age": 17.5}
    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 200
    bear_id = post_response.text

    put_response = requests.put(f'{ALASKA_SERVER_URL}/bear/{bear_id}', data=json.dumps(update_json))
    assert put_response.status_code == 200

    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
    response_text = get_response.text
    update_json['bear_id'] = int(bear_id)

    assert json.loads(response_text) == update_json


@pytest.mark.testcase_id('TC-5')
async def test_modify_bear_name(unit_under_test):
    """
    Summary:
        You can modify bear's name with a PUT request to /bear/<bear_id> endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send POST request to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id from response body
         # Send PUT request to ALASKA_SERVER_URL/bear/<bear_id> endpoint with JSON that contains modified bear_type
         field
         # Send GET request to ALASKA_SERVER_URL/bear/<bear_id> endpoint
    Expected result:
        Response with HTTP/200 status
        Response body contains JSON object that describes a bear with modified name"""
    mikhail_json = {"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 17.5}
    update_json = {"bear_type": "BLACK", "bear_name": "IVAN", "bear_age": 17.5}
    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 200
    bear_id = post_response.text

    put_response = requests.put(f'{ALASKA_SERVER_URL}/bear/{bear_id}', data=json.dumps(update_json))
    assert put_response.status_code == 200

    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
    response_text = get_response.text
    update_json['bear_id'] = int(bear_id)

    assert json.loads(response_text) == update_json


@pytest.mark.testcase_id('TC-6')
async def test_modify_bear_age(unit_under_test):
    """
    Summary:
        You can modify bear's age with a PUT request to /bear/<bear_id> endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send POST request to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id from response body
         # Send PUT request to ALASKA_SERVER_URL/bear/<bear_id> endpoint with JSON that contains modified bear_type
         field
         # Send GET request to ALASKA_SERVER_URL/bear/<bear_id> endpoint
    Expected result:
        Response with HTTP/200 status
        Response body contains JSON object that describes a bear with modified age"""
    mikhail_json = {"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 17.5}
    update_json = {"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 8}
    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 200
    bear_id = post_response.text

    put_response = requests.put(f'{ALASKA_SERVER_URL}/bear/{bear_id}', data=json.dumps(update_json))
    assert put_response.status_code == 200

    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
    response_text = get_response.text
    update_json['bear_id'] = int(bear_id)

    assert json.loads(response_text) == update_json


@pytest.mark.testcase_id('TC-7')
async def test_remove_a_bear_by_id(unit_under_test):
    """
    Summary:
        You can remove a bear with a DELETE request to /bear/<bear_id> endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send POST request to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id from response body
         # Send DELETE request to ALASKA_SERVER_URL/bear/<bear_id> endpoint
         # Send GET request to ALASKA_SERVER_URL/bear/<bear_id> endpoint
         # Send GET request to ALASKA_SERVER_URL/bear endpoint
    Expected result:
        Response with HTTP/200 status
        Response body contains 'EMPTY' string for request to ALASKA_SERVER_URL/bear/<bear_id>
        Response body contains empty JSON list for request to ALASKA_SERVER_URL/bear"""
    mikhail_json = {"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 17.5}
    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 200
    bear_id = post_response.text

    delete_response = requests.delete(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
    assert delete_response.status_code == 200

    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
    response_text = get_response.text
    assert response_text == EMPTY_VALUE

    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear')
    response_text = get_response.text
    assert json.loads(response_text) == []


@pytest.mark.testcase_id('TC-8')
async def test_remove_a_bear_by_id_and_then_add_one(unit_under_test):
    """"""
    mikhail_json = {"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 17.5}

    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 200
    bear_id = post_response.text

    delete_response = requests.delete(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
    assert delete_response.status_code == 200

    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
    response_text = get_response.text
    assert response_text == EMPTY_VALUE

    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 200
    bear_id_new = post_response.text
    mikhail_json['bear_id'] = int(bear_id_new)

    get_by_id_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bear_id_new}')
    assert get_by_id_response.status_code == 200
    response_text = get_by_id_response.text
    assert json.loads(response_text) == mikhail_json

    get_all_response = requests.get(f'{ALASKA_SERVER_URL}/bear')
    assert get_all_response.status_code == 200
    response_text = get_all_response.text
    assert json.loads(response_text) == [mikhail_json]


@pytest.mark.testcase_id('TC-9')
async def test_remove_all_bears(unit_under_test):
    """
    Summary:
        You can remove all bears with a DELETE request to /bear endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send POST request to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id from response body
         # Send DELETE request to ALASKA_SERVER_URL/bear endpoint
         # Send GET request to ALASKA_SERVER_URL/bear/<bear_id> endpoint
         # Send GET request to ALASKA_SERVER_URL/bear endpoint
    Expected result:
        Response with HTTP/200 status
        Response body contains 'EMPTY' string for request to ALASKA_SERVER_URL/bear/<bear_id>
        Response body contains empty JSON list for request to ALASKA_SERVER_URL/bear"""
    mikhail_json = {"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 17.5}
    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 200
    bear_id = post_response.text

    delete_response = requests.delete(f'{ALASKA_SERVER_URL}/bear')
    assert delete_response.status_code == 200

    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
    response_text = get_response.text
    assert response_text == EMPTY_VALUE

    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear')
    response_text = get_response.text
    assert json.loads(response_text) == []


@pytest.mark.parametrize('bear_type', BEAR_TYPES_LIST)
@pytest.mark.testcase_id('TC-10')
async def test_add_a_bear_uppercase_different_types(unit_under_test, bear_type):
    """
    Summary:
        You can create a bear with a POST request to /bear endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send POST request to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id from response body
         # Send GET request to ALASKA_SERVER_URL/bear/<bear_id>
    Expected result:
        Response with HTTP/200 status
        Response body contains JSON object that describes created bear"""
    mikhail_json = {"bear_type": bear_type, "bear_name": "MIKHAIL", "bear_age": 17.5}
    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 200
    bear_id = post_response.text
    mikhail_json['bear_id'] = int(bear_id)
    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
    response_text = get_response.text
    assert json.loads(response_text) == mikhail_json


@pytest.mark.parametrize('bear_age', [17.5, 1, 0.6])
@pytest.mark.testcase_id('TC-11')
async def test_add_a_bear_uppercase_different_ages(unit_under_test, bear_age):
    """
    Summary:
        You can create a bear with a POST request to /bear endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send POST request to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id from response body
         # Send GET request to ALASKA_SERVER_URL/bear/<bear_id>
    Expected result:
        Response with HTTP/200 status
        Response body contains JSON object that describes created bear"""
    mikhail_json = {"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": bear_age}
    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 200
    bear_id = post_response.text
    mikhail_json['bear_id'] = int(bear_id)
    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
    response_text = get_response.text
    assert json.loads(response_text) == mikhail_json
