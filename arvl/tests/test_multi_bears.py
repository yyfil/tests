import pytest
import requests
import json
import names
from random import randint, uniform
from test_data.alaska import INFO_MESSAGE_CORRECT, INFO_MESSAGE_CURRENT, BEAR_TYPES_LIST, EMPTY_VALUE, \
    ALASKA_SERVER_URL, VALID_BEAR_TYPES_LIST


pytestmark = pytest.mark.asyncio
MAX_VALID_BEAR_N = 10


def generate_bears(bears_number):
    bears_list = []
    for i in range(0, bears_number):
        bears_list.append({'bear_type': VALID_BEAR_TYPES_LIST[randint(0, len(VALID_BEAR_TYPES_LIST)-1)],
                           'bear_name': names.get_first_name().upper(),
                           'bear_age': round(uniform(0.1, 100), 1)})
    return bears_list


@pytest.mark.testcase_id('TC-13')
@pytest.mark.parametrize('bears_number', [2, 3, MAX_VALID_BEAR_N, 11])
async def test_add_n_bears(unit_under_test, bears_number):
    """
    Summary:
        You can create N bears with POST requests to /bear endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send N POST request to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id from response body
         # Send GET request to ALASKA_SERVER_URL/bear
    Expected result:
        Response with HTTP/200 status
        Response body contains JSON list with N objects that describe created bears"""
    await unit_under_test()
    bears_list = generate_bears(bears_number)
    for bear_json in bears_list:
        post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(bear_json))
        assert post_response.status_code == 200
        bear_id = post_response.text
        bear_json['bear_id'] = int(bear_id)
        get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
        response_text = get_response.text
        assert json.loads(response_text) == bear_json
    all_bears_response = requests.get(f'{ALASKA_SERVER_URL}/bear')
    response_json = json.loads(all_bears_response.text)
    # This assertion fails for N bears > 10
    assert bears_list == response_json
    # If list order is not crucial we can sort bears:
    #assert sorted(bears_list, key=lambda bear: bear['bear_id']) == sorted(response_json,
    #                                                                      key=lambda bear: bear['bear_id'])


@pytest.mark.testcase_id('TC-14')
@pytest.mark.skip
async def test_add_bears_maximum(unit_under_test):
    """
    Summary:
        This case is supposed to test limit of N bears that can be created. Skip for now as we do not have documented
        limit"""
    await unit_under_test()
    bears_list = generate_bears(1000)
    for bear_json in bears_list:
        post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(bear_json))
        assert post_response.status_code == 200
        bear_id = post_response.text
        bear_json['bear_id'] = int(bear_id)
        get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bear_id}')
        response_text = get_response.text
        assert json.loads(response_text) == bear_json
    all_bears_response = requests.get(f'{ALASKA_SERVER_URL}/bear')
    response_json = json.loads(all_bears_response.text)
    print(response_json)
    print(len(response_json))
    print(list([b['bear_id'] for b in response_json]))
    assert sorted(bears_list, key=lambda bear: bear['bear_id']) == sorted(response_json,
                                                                          key=lambda bear: bear['bear_id'])


@pytest.mark.testcase_id('TC-15')
async def test_modify_name_for_a_bear(unit_under_test):
    """
    Summary:
        You can modify bear's name with a PUT request to /bear/<bear_id> endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send N POST requests to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id from response body
         # Choose one random bear_id
         # Send PUT request to ALASKA_SERVER_URL/bear/<bear_id> endpoint with JSON that contains modified bear_name
         field
         # Send GET request to ALASKA_SERVER_URL/bear endpoint
    Expected result:
        Response with HTTP/200 status
        Response body contains JSON list that contains all bears unchanged except one specified bear"""
    await unit_under_test()
    bears_list = generate_bears(randint(2, MAX_VALID_BEAR_N))
    for bear_json in bears_list:
        post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(bear_json))
        assert post_response.status_code == 200
        bear_id = post_response.text
        bear_json['bear_id'] = int(bear_id)
    modified_bear_idx = randint(0, len(bears_list)-1)
    bears_list[modified_bear_idx]["bear_name"] = f'{bears_list[modified_bear_idx]["bear_name"]}_modified'
    update_bear_json = {'bear_name': bears_list[modified_bear_idx]["bear_name"],
                        'bear_age': bears_list[modified_bear_idx]["bear_age"],
                        'bear_type': bears_list[modified_bear_idx]["bear_type"]}
    modified_bear_id = bears_list[modified_bear_idx]['bear_id']
    put_response = requests.put(f'{ALASKA_SERVER_URL}/bear/{modified_bear_id}', data=json.dumps(update_bear_json))
    assert put_response.status_code == 200

    all_bears_response = requests.get(f'{ALASKA_SERVER_URL}/bear')
    response_json = json.loads(all_bears_response.text)
    assert sorted(bears_list, key=lambda bear: bear['bear_id']) == sorted(response_json,
                                                                          key=lambda bear: bear['bear_id'])


@pytest.mark.testcase_id('TC-16')
async def test_modify_name_for_all_bears(unit_under_test):
    """
    Summary:
        You can modify bear's name with a PUT request to /bear/<bear_id> endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send N POST requests to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id from response body
         # Send N PUT requests to ALASKA_SERVER_URL/bear/<bear_id> endpoint with JSON that contains modified bear_name
         field
         # Send GET request to ALASKA_SERVER_URL/bear endpoint
    Expected result:
        Response with HTTP/200 status
        Response body contains JSON list that contains all bears with modified names"""
    await unit_under_test()
    bears_list = generate_bears(randint(2, MAX_VALID_BEAR_N))
    update_bears_list = list()
    for bear_json in bears_list:
        post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(bear_json))
        assert post_response.status_code == 200
        bear_id = post_response.text
        bear_json['bear_id'] = int(bear_id)

    for bear_json in bears_list:
        update_bear_json = {'bear_name': f'{bear_json["bear_name"]}_modified',
                            'bear_age': bear_json["bear_age"],
                            'bear_type': bear_json["bear_type"]}
        put_response = requests.put(f'{ALASKA_SERVER_URL}/bear/{bear_json["bear_id"]}',
                                    data=json.dumps(update_bear_json))
        assert put_response.status_code == 200
        update_bear_json["bear_id"] = bear_json["bear_id"]
        update_bears_list.append(update_bear_json)

    all_bears_response = requests.get(f'{ALASKA_SERVER_URL}/bear')
    response_json = json.loads(all_bears_response.text)
    assert sorted(update_bears_list, key=lambda bear: bear['bear_id']) == sorted(response_json,
                                                                                 key=lambda bear: bear['bear_id'])


@pytest.mark.testcase_id('TC-17')
async def test_remove_a_bear_by_id(unit_under_test):
    """
    Summary:
        You can remove a bear with a DELETE request to /bear/<bear_id> endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send N POST requests to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id's from response bodies
         # Choose a random bear_id
         # Send DELETE request to ALASKA_SERVER_URL/bear/<bear_id> endpoint
         # Send GET request to ALASKA_SERVER_URL/bear/<bear_id> endpoint
         # Send GET request to ALASKA_SERVER_URL/bear endpoint
    Expected result:
        Response with HTTP/200 status
        Response body contains 'EMPTY' string for request to ALASKA_SERVER_URL/bear/<bear_id>
        Response body contains JSON list with all bears except removed one for request to ALASKA_SERVER_URL/bear"""
    await unit_under_test()
    bears_list = generate_bears(randint(2, MAX_VALID_BEAR_N))
    for bear_json in bears_list:
        post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(bear_json))
        assert post_response.status_code == 200
        bear_id = post_response.text
        bear_json['bear_id'] = int(bear_id)
    removed_bear_idx = randint(0, len(bears_list)-1)
    removed_bear_id = bears_list[removed_bear_idx]["bear_id"]
    delete_response = requests.delete(f'{ALASKA_SERVER_URL}/bear/{removed_bear_id}')
    assert delete_response.status_code == 200

    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{removed_bear_id}')
    response_text = get_response.text
    assert response_text == EMPTY_VALUE

    expected_bears_list = bears_list.copy()
    del expected_bears_list[removed_bear_idx]

    all_bears_response = requests.get(f'{ALASKA_SERVER_URL}/bear')
    response_json = json.loads(all_bears_response.text)
    assert sorted(expected_bears_list, key=lambda bear: bear['bear_id']) == sorted(response_json,
                                                                                   key=lambda bear: bear['bear_id'])


@pytest.mark.testcase_id('TC-18')
async def test_remove_two_bears_by_id(unit_under_test):
    """
    Summary:
        You can remove several bears with a DELETE request to /bear/<bear_id> endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send N POST requests to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id's from response bodies
         # Choose 2 bear_id's
         # Send 2 DELETE requests to ALASKA_SERVER_URL/bear/<bear_id> endpoint
         # Send GET request to ALASKA_SERVER_URL/bear/<bear_id> endpoint
         # Send GET request to ALASKA_SERVER_URL/bear endpoint
    Expected result:
        Response with HTTP/200 status
        Response body contains 'EMPTY' string for requests to ALASKA_SERVER_URL/bear/<bear_id>
        Response body contains JSON list with all bears except removed ones for request to ALASKA_SERVER_URL/bear"""
    await unit_under_test()
    bears_list = generate_bears(randint(3, MAX_VALID_BEAR_N))
    for bear_json in bears_list:
        post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(bear_json))
        assert post_response.status_code == 200
        bear_id = post_response.text
        bear_json['bear_id'] = int(bear_id)

    # Remove first and last bears:
    for i in [0, -1]:
        delete_response = requests.delete(f'{ALASKA_SERVER_URL}/bear/{bears_list[i]["bear_id"]}')
        assert delete_response.status_code == 200
        get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{bears_list[i]["bear_id"]}')
        response_text = get_response.text
        assert response_text == EMPTY_VALUE

    expected_bears_list = bears_list[1:-1]

    all_bears_response = requests.get(f'{ALASKA_SERVER_URL}/bear')
    response_json = json.loads(all_bears_response.text)
    assert sorted(expected_bears_list, key=lambda bear: bear['bear_id']) == sorted(response_json,
                                                                                   key=lambda bear: bear['bear_id'])


@pytest.mark.testcase_id('TC-19')
async def test_remove_all_bears(unit_under_test):
    """
    Summary:
        You can remove all bears with a DELETE request to /bear endpoint
    Setup:
        Alaska server started
    Tear down:
        Stop Alaska server
    Steps:
         # Send N POST requests to ALASKA_SERVER_URL/bear endpoint with JSON string passed as data payload
         # Remember bear_id's from response bodies
         # Select random bear_id
         # Send DELETE request to ALASKA_SERVER_URL/bear endpoint
         # Send GET request to ALASKA_SERVER_URL/bear/<bear_id> endpoint
         # Send GET request to ALASKA_SERVER_URL/bear endpoint
    Expected result:
        Response with HTTP/200 status
        Response body contains 'EMPTY' string for request to ALASKA_SERVER_URL/bear/<bear_id>
        Response body contains JSON list with all bears except removed one for request to ALASKA_SERVER_URL/bear"""
    await unit_under_test()
    bears_list = generate_bears(randint(2, MAX_VALID_BEAR_N))
    for bear_json in bears_list:
        post_response = requests.post(f'{ALASKA_SERVER_URL}/bear', data=json.dumps(bear_json))
        assert post_response.status_code == 200
        bear_id = post_response.text
        bear_json['bear_id'] = int(bear_id)
    removed_bear_idx = randint(0, len(bears_list)-1)
    removed_bear_id = bears_list[removed_bear_idx]["bear_id"]
    delete_response = requests.delete(f'{ALASKA_SERVER_URL}/bear')
    assert delete_response.status_code == 200

    get_response = requests.get(f'{ALASKA_SERVER_URL}/bear/{removed_bear_id}')
    response_text = get_response.text
    assert response_text == EMPTY_VALUE

    all_bears_response = requests.get(f'{ALASKA_SERVER_URL}/bear')
    response_json = json.loads(all_bears_response.text)
    assert response_json == []
