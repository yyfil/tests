HOWTO:
* download image: 
  ```bash
  docker pull azshoo/alaska:1.0
  ```
* run tests:
  ```bash
  > git clone https://github.com/yyfil/tests.git
  > cd tests/arvl
  > virtualenv -p python3 .venv
  > source .venv/bin/activate
  > pip install -r requirements.txt
  > export PYTHONPATH="`pwd`/lib:$PYTHONPATH" && pytest --html=report.html
  > deactivate
  ```
* to access HTML report open report.html in any browser

* get info:
  * start application:
    ```bash
    docker run -d --name alaska_bears azshoo/alaska:1.0
    ```
  * get info resource:
    ```bash
    docker exec -it alaska_bears curl 0.0.0.0:8091/info
    ```
* stop application and remove container:
  ```bash
  docker kill alaska_bears && docker rm alaska_bears
  ```