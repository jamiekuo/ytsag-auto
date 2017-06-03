# require
 - python3
 - docker

# install
```sh
./install
git submodule init
git submodule update
```

## BT server
 - ### modify config/setting.json
    ```
    "rpc-enabled": true,
    "rpc-password": "your password",
    "rpc-username": "login id",
    ```
 - ### permission for docker container
    look up user id
    ```sh
    id $USER
    ```
    modify PUID and PGID in docker-compose.yml file
    ```
      - PUID=1002
      - PGID=1003
    ```
 - ### run;
    ```sh
    docker-compose up -d
    ```

## Download
 - ### modify auth.json
    ```
    "user": "BT server login id",
    "password": "BT server PW "
    ```
 - ### modify capacity in main.py
    ```
    LIMIT_BYTES = XXX*1000*1000*1000   #(XXX GB)
    ```
 - ### modify yts setting in main.py (https://yts.ag/api)
    ```
    params = {
        ...
        'minimum_rating': 6     #(IMDB rating)
    }
    ignore_qualities = ['720p']
    ```
