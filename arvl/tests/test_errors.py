import pytest
import requests
import json
from test_data.alaska import INFO_MESSAGE_CORRECT, INFO_MESSAGE_CURRENT, BEAR_TYPES_LIST, EMPTY_VALUE


pytestmark = pytest.mark.asyncio

ALASKA_SERVER_URL = 'http://0.0.0.0:8091'


@pytest.mark.testcase_id('TC-XX')
async def test_remove_a_bear_by_id_and_then_modify_one(unit_under_test):
    """"""
    mikhail_json = {"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 17.5}
    update_json = {"bear_type": "BLACK", "bear_name": "IVAN", "bear_age": 17.5}
    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 200
    bear_id = post_response.text

    delete_response = requests.delete(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
    assert delete_response.status_code == 200

    put_response = requests.put(f'{ALASKA_SERVER_URL}/bear/{bear_id}', data=json.dumps(update_json))
    assert put_response.status_code == 500


@pytest.mark.testcase_id('TC-X')
async def test_modify_nonexistent_bear(unit_under_test):
    """
    Some destructive testing
    """
    mikhail_json = {"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 17.5}
    await unit_under_test()
    put_response = requests.put(f'{ALASKA_SERVER_URL}/bear/1', data=json.dumps(mikhail_json))
    assert put_response.status_code == 500


@pytest.mark.parametrize('bear_age', [100.1, 0, -5, 'wrong age'])
@pytest.mark.testcase_id('TC-12')
async def test_add_a_bear_uppercase_invalid_ages(unit_under_test, bear_age):
    mikhail_json = {"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": bear_age}
    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 500


@pytest.mark.parametrize('bear_type', ['wrong type', 0, ''])
@pytest.mark.testcase_id('TC-20')
async def test_add_a_bear_uppercase_invalid_types(unit_under_test, bear_type):
    mikhail_json = {"bear_type": bear_type, "bear_name": "MIKHAIL", "bear_age": 9}
    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 500


@pytest.mark.parametrize('bear_name', ['', 0])
@pytest.mark.testcase_id('TC-21')
async def test_add_a_bear_uppercase_invalid_names(unit_under_test, bear_name):
    mikhail_json = {"bear_type": "BLACK", "bear_name": bear_name, "bear_age": 9}
    await unit_under_test()
    post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(mikhail_json))
    assert post_response.status_code == 500
