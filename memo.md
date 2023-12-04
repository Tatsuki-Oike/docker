#  1 コンテナのライフサイクル
***

## 1.1 pythonのコンテナ

### 1.1.1 コンテナの起動

 * docker runの場合
```sh
docker container run --name python_container -it python:3.9-slim /bin/bash
```


* pull, create, startを個別で行う場合
```sh
docker image pull python:3.9-slim
docker create -it --name python_container /bin/bash
docker start python_container
```

### 1.1.2 pythonの操作

* pythonの実行
```sh
python3
```


* pythonの操作
```python
print("pythonの実行")
exit() # pythonから離脱
```


* dockerから離脱
```sh
exit
```

### 1.1.3 コンテナ、イメージの確認

```sh
docker image ls
docker container ls -a
```


### 1.1.4 コンテナ、イメージの停止、消去

* コンテナの停止、消去
```sh
# docker container stop python_container
docker container rm python_container
```


* イメージの消去
```sh
docker image rm python3.9-slim
```

## 1.2 apacheのコンテナ

### 1.2.1 コンテナの起動

* docker runの場合
```sh
docker container run -dit --name apache_container -p 8080:80 httpd:2.4
```


* pull, create, startを個別で行う場合
```sh
docker image pull httpd:2.4
docker create -dit --name apache_container -p 8080:80
docker start apache_container
```

### 1.2.2 webサーバーの確認

* http://localhost:8080 にアクセス


### 1.2.3 コンテナ、イメージの停止、消去

* コンテナの停止、消去
```sh
docker container stop apache_container
docker container rm apache_container
```


* イメージの消去
```sh
docker image rm httpd:2.4
```

# 2 マウントとVolume
***

## 2.1 pythonでバインドマウント

### 2.1.1 バインドマウント

* /Users/ooikeitsuki/Documents/youtube/Docker/2_sample_python_mount/sample.py作成
```python
print("pythonの実行成功")
```


* コンテナの起動
```sh
docker container run --name python_container -it -v /Users/ooikeitsuki/Documents/youtube/Docker/2_sample_python_mount:/tmp/ python:3.9-slim /bin/bash
```

### 2.1.2 バインドマウント確認

* pythonファイルの実行
```sh
ls /tmp/
cd /tmp/
python3 sample.py
exit
```

## 2.2 pythonでボリュームマウント

### 2.2.1 ボリュームの利用

* volumeの作成
```sh
docker volume create sample_volume
```


* ボリュームマウント
```sh
docker container run --name python_container2 -it -v sample_volume:/tmp/ python:3.9-slim /bin/bash
```


* ファイル作成
```sh
echo "print('pythonの実行成功')" > /tmp/sample.py
ls /tmp/
cd /tmp/
python3 sample.py
exit
```

### 2.2.2 ボリュームマウント確認

* ボリュームマウント
```sh
docker container rm python_container2
docker container run --name python_container2 -it -v sample_volume:/tmp/ python:3.9-slim /bin/bash
ls /tmp/
exit
```


### 2.2.3 コンテナ、ボリュームの後処理
```sh
docker container rm python_container
docker container rm python_container2
docker volume ls
docker volume rm sample_volume
```

## 2.3 apatchでバインドマウント

### 2.3.1 バインドマウント

* /Users/ooikeitsuki/Documents/youtube/Docker/2_sample_apache_mount/index.html作成
```html
SUCCESS
```


* コンテナの起動
```sh
docker container run -dit --name apache_container -p 8080:80 -v /Users/ooikeitsuki/Documents/youtube/Docker/2_sample_apache_mount:/usr/local/apache2/htdocs httpd:2.4
```

### 2.3.2 バインドマウント確認
* http://localhost:8080 にアクセス


### 2.3.3 コンテナの後処理

```sh
docker container stop apache_container
docker container rm apache_container
```

# 3 network
***

## 3.1 network作成

* network作成
```sh
docker network create sample_network
```


* データベースコンテナ起動
```sh
docker container run --name db_container -dit --net=sample_network -e MYSQL_ROOT_PASSWORD=root_password -e MYSQL_USER=sample_user -e MYSQL_PASSWORD=sample_password mysql
```


* pythonコンテナ起動
```sh
docker container run --name python_container -it -v /Users/ooikeitsuki/Documents/youtube/Docker/3_sample_network:/tmp/ --net=sample_network python:3.9-slim /bin/bash
```

## 3.2 network接続確認

```sh
pip3 install mysql-connector-python
ls /tmp/
cd /tmp/
python3 network.py
exit
```

## 3.3 後処理

```sh
docker container stop db_container
docker container rm python_container
docker container rm db_container
docker network rm sample_network
```

# 4 Dockerfile
***

## 4.1 Dockerfile作成


* Dockerfile

```
FROM python:3.9-slim

WORKDIR /tmp/
COPY requirements.txt ${PWD}
RUN pip install -r requirements.txt
```


* requirements.txt
```
mysql-connector-python
```

## 4.2 Dockerfileでimage作成


* dockerfileでimage作成
```sh
docker build -t original_image1 /Users/ooikeitsuki/Documents/youtube/Docker/4_docker_file
docker image ls
```


## 4.3 作成したimageを実行

* network作成
```sh
docker network create sample_network
```


* コンテナ起動
```sh
docker container run --name db_container -dit --net=sample_network -e MYSQL_ROOT_PASSWORD=root_password -e MYSQL_USER=sample_user -e MYSQL_PASSWORD=sample_password mysql
docker container run --name python_container -it -v /Users/ooikeitsuki/Documents/youtube/Docker/3_sample_network:/tmp/ --net=sample_network original_image1 /bin/bash
```


* 接続確認
```sh
python3 network.py
exit
```


* 後処理
```sh
docker container stop db_container
docker container rm python_container
docker container rm db_container
docker network rm sample_network
```

# 5 Docker compose
***

## 5.1 Docker composeの利用

* Docker composeファイルの作成


* Dockerfileでimage作成
```sh
docker build -t original_image2 /Users/ooikeitsuki/Documents/youtube/Docker/5_1_docker_compose
```


* Docker composeの起動
```sh
docker compose -f /Users/ooikeitsuki/Documents/youtube/Docker/5_1_docker_compose/docker-compose.yml up -d
docker container ls -a
docker exec -it 5_1_docker_compose-python_container-1 /bin/bash
```


* コンテナの確認
```sh
python3 network.py
exit
```


* Docker composeの停止
```sh
docker compose -f /Users/ooikeitsuki/Documents/youtube/Docker/5_1_docker_compose/docker-compose.yml down
```

## 5.2 Docker composeとDocker fileの利用

* Docker composeファイルの作成


* Docker composeの起動
```sh
docker compose -f /Users/ooikeitsuki/Documents/youtube/Docker/5_2_docker_compose/docker-compose.yml up -d
docker container ls -a
docker exec -it 5_2_docker_compose-python_container-1 /bin/bash
```


* コンテナの確認
```sh
python3 network.py
exit
```


* Docker composeの停止
```sh
docker compose -f /Users/ooikeitsuki/Documents/youtube/Docker/5_2_docker_compose/docker-compose.yml down
```

## 5.3 ボリュームの消去

```sh
docker volume rm 5_1_docker_compose_db_volume
docker volume rm 5_2_docker_compose_db_volume
```

# 6 Docker compose のサンプル
***

## 6.1 LAMP環境構築

* Docker composeの起動
```sh
docker compose -f /Users/ooikeitsuki/Documents/youtube/Docker/6_1_lamp/docker-compose.yml up -d
```


* http://localhost:8080 にアクセス


* Docker composeの停止
```sh
docker compose -f /Users/ooikeitsuki/Documents/youtube/Docker/6_1_lamp/docker-compose.yml down
```


* volumeの消去
```sh
docker volume rm 6_1_lamp_mysql_db
```

## 6.2 jupyterlabの環境構築

* Docker composeの起動
```sh
docker compose -f /Users/ooikeitsuki/Documents/youtube/Docker/6_2_jupyterlab/docker-compose.yml up -d
```


* http://localhost:8888 にアクセス


* Docker composeの停止
```sh
docker compose -f /Users/ooikeitsuki/Documents/youtube/Docker/6_2_jupyterlab/docker-compose.yml down
```