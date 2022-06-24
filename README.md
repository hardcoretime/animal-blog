# Animal Blog

## Prerequisites
<ol>
    <li>docker-compose 1.29.2+</li>
    <li>python3.6+</li>
</ol>

## Installing
```shell
python3 -m venv .venv
pip install --upgrade pip --no-cache-dir
pip install -r requirements.txt --no-cache-dir
```

## Usage
```
# init env variables in .env file
CONFIG= # input env config name from config.py(for example "TestingConfig")
DB_NAME=  # input db name
DB_USERNAME=  # input db username
DB_PASSWORD=  # input db user password
PORT=  # input db host port for docker-compose
SECRET_KEY= # input strong flask secret-key
```

```shell
# build application
sudo docker-compose build app
```

```shell
# start app 
sudo docker-compose up -d app
```

```shell
# fill db with testing data
python init_blog_db.py
```

```shell
# tests
python -m pytest -v -s tests/test_db.py
```

## Main page
[Animal blog](http://0.0.0.0:5000)