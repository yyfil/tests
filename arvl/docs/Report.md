## Вопросы для обсуждения: ##
1) Почему можно создавать медведя с возрастом 0.0? Сейчас тест test_errors.py::test_add_a_bear_uppercase_invalid_ages[0] падает потому, что мне кажется, что это не имеет физического смысла.
2) Почему имя приводится к верхнему регистру? Сейчас тест test_one_bear.py::test_add_a_bear падает из-за того, что я ожидаю, что переданное в POST запросе имя сохранится без изменений.
3) Почему при создании более 10 медведей сервис отдаёт несортированный список в ответ на GET запрос? Сейчас тест test_multi_bears.py::test_add_n_bears[11] падает из-за того, что я ожидаю, что список будет отсортирован.


## Bugs found: ##
### BUG-1 (High): ###
__Summary:__ Bear age >100 is cast to 0.0 without error status

__Steps:__
* Run test_errors.py::test_add_a_bear_uppercase_invalid_ages test case 
or
* Send POST request with `{"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 100.1}` to <service_url>/bear 
  endpoint.

__Expected result:__ Service responds with 500 status
__Actual result:__ Service responds with 200 status and bear_id in response body. If you send GET request to 
<service_url>/bear/<bear_id> you will get `{"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 0.0}` response.


### BUG-2 (High): ###
__Summary:__ Bear age <0 is cast to 0.0 without error status
__Steps:__
* Run test_errors.py::test_add_a_bear_uppercase_invalid_ages test case
or
* Send POST request with `{"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": -10}` to 
  <service_url>/bear endpoint.
__Expected result:__ Service responds with 500 status
__Actual result:__ Service responds with 200 status and bear_id in response body.
If you send GET request to <service_url>/bear/<bear_id> you will get 
  `{"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 0.0}` response.

### BUG-3 (Critical): ###
__Summary:__ Bear's type cannot be updated
__Steps:__ 
* Run test_one_bear.py::test_modify_bear_type
or
* Send POST request with `{"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 10}` to <service_url>/bear endpoint.
* Remember bear_id
* Send PUT request with `{"bear_type": "BROWN", "bear_name": "MIKHAIL", "bear_age": 10}` to <service_url>/bear/<bear_id> endpoint.
* Send GET request to <service_url>/bear/<bear_id> endpoint.
__Expected result:__ Service responds with `{"bear_type": "BROWN", "bear_name": "MIKHAIL", "bear_age": 10, "bear_id": <bear_id>}`
__Actual result:__ Type is not modified, service responds with `{"bear_type": "BLACK", "bear_name": "MIKHAIL", "bear_age": 10}`


### BUG-4 (Critical): ###
__Summary:__ Bear's age cannot be updated
__Steps:__ Run test_one_bear.py::test_modify_bear_age


### BUG-5 (Critical): ###
__Summary:__ GUMMY bear cannot be created
__Steps:__ Run test_one_bear.py::test_add_a_bear_uppercase_different_types


## Low priority bugs and improvements: ##
### BUG-6 (Normal): ###
__Summary:__ If more than 10 bears are created, service returns unsorted list on GET request to <service_url>/bear endpoint
__Steps:__ Run test_multi_bears.py::test_add_n_bears

### BUG-7 (Low): ###
__Summary:__ Fix typos in /info message
__Steps:__ Run tests/test_one_bear.py::test_info

### BUG-8 (Low): ###
__Summary:__ You can delete bear that doesn't exist
__Steps:__ Send DELETE request to /bear/<non_existent_id>

### BUG-9 (Low): ###
__Summary:__ Add content-type:application/json to response headers if response contains JSON object

### BUG-10 (Low): ###
__Summary:__ Service adds a bear with an empty name
__Steps:__ Run test_errors.py::test_add_a_bear_uppercase_invalid_names

### BUG-11 (Low): ###
__Summary:__ Service adds a bear with an integer name
__Steps:__ Run test_errors.py::test_add_a_bear_uppercase_invalid_names
