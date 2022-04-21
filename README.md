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
DB_NAME=  # input db name
DB_USERNAME=  # input db username
DB_PASSWORD=  # input db user password
PORT=  # input db host port for docker-compose
```

```shell
# export env variables
export $(xargs < .env)
```

```shell
# start db
sudo docker-compose up -d
```

```shell
# init db
python init_blog_db.py
```

```shell
# fill db
python fill_blog_db.py
```

```shell
# tests
python -m pytest -v -s tests/test_db.py
```
