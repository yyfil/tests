HOWTO:
* download image: docker pull azshoo/alaska:1.0
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
* run tests:
  ```bash
  > cd arvl
  > virtualenv -p python3 .venv
  > source .venv/bin/activate
  > pip install -r requirements.txt
  > export PYTHONPATH="`pwd`/lib:$PYTHONPATH" && pytest
  > deactivate
  ```
  