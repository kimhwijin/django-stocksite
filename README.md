# docker setting
Repository of stock website using docker
Plz do the following steps carefully before you meet the whale.

## Project Setup (Windows)

### 디렉토리 구조
├── Dockerfile \
├── env.dev \
├── docker-compose.yml \
└── README.md

### Docker process

0. 디렉토리 내 .env.dev를 .env로 이름을 바꿔주세요.

- 가상환경 생성

  ```shell
  $ virtualenv venv
  ```

- 가상환경 활성화

  ```shell
  $ .\venv\Scripts\activate
  (venv) $
  ```

- secret_key 받는 법 :

  ```shell
  (venv) $ python manage.py shell
  In[1]: from django.core.management.utils import get_random_secret_key
  In[2]: get_random_secret_key()
  Out[2]: '*****************************'
  exit()
  ```
- out으로 나온 결과 붙여 넣으면 됨

- local test 하고 싶다면: .env 에서 아래와 같이 두 항목 주석 처리 후 테스트하고, 다시 주석 풀기
  ```shell
	# SQL_ENGINE=django.db.backends.postgresql
	# SQL_DATABASE=db_handshakers
  ```

0. 도커 이미지 생성(build)최초실행시와 Dockerfile 수정 시 필요
1. 생성된 이미지로 도커 컨테이너 올리기(서버실행, up)
2. migrate + collectstatic + createsuperuser
3. 127.0.0.1 로 접속해보기
4. 127.0.0.1/admin/ 으로 접속하면 설정해둔 관리자 계정으로 로그인하여 데이터 관리 가능
5. 도커 컨테이너 내리기(필수!!)
6. 원한다면 내리면서 삭제하기
7. 단축키는 alias로 설정해야 함
8. 개발용과 배포용이 차이가 있음. (보안 및 개발 편의성을 위해)
	개발용: 비밀번호 공개, env파일 git에 업로드, 코드 변경 시 바로 반영
	배포용: env.template으로 git에 업로드, docker-compose.prod.yml 로  -f 옵션줘서 실행해야 함. 추후 추가할 예정

### Before you start, check the docker

- 도커 잘 설치 되어있는지 확인

  ```shell
  (venv) $ docker -v
  Docker version 19.x.x, build ******
  ```

### To make docker image

- 기존 설치되어 있던 프로그램들 도커 이미지에 반영하기 위해 requirements.txt 업데이트

- 새로 무언가를 설치하게 되면 (pip install 등) 도커 이미지 빌드 전에 무조건 다시 실행해줘야 함

  ```shell
  (venv) $ pip freeze > requirements.txt
  ```
## Run & stop the server

- 최초 실행(도커 올리기 + 이미지 build & docker-compose.yml 파일이 있는 디렉토리 내)
- 배포 버전은 위 명령어 사용, 개발 버전은 아래 명령어 사용
  ```shell
  (venv) $ docker-compose -f docker-compose.prod.yml up --build
  (venv) $ docker-compose up --build
  ```

- 중단하기 : ctrl + C

- 도커 올리기 (-d 를 붙이면 백그라운드에서 돌아감: 창에 로그가 뜨지 않음)

  ```shell
  (venv) $ docker-compose up -d
   ```

- 도커 내리기 (어떠한 경우에도 반드시 실행)

  ```shell
  (venv) $ docker-compose down
  ```

- 도커 내리면서 컨테이너(volume)삭제하고 싶을 때 (데이터나 코드가 변경되었을 때, 새로운 이미지를 다시 빌드하기 위해)

  ```shell
  (venv) $ docker-compose down -v
  ```

### DB Setup

- 컨테이너 올려두었을 때 사용. 다른 터미널을 띄우거나, 백그라운드에서 실행 시 해당 터미널에서 입력

- 도커 최초 실행 또는 DB 스키마 등이 변경될 경우 서버 실행 전 다음 명령어를 한 번씩 실행 (makemigrations는 최초 실행 시에만, 그 뒤로는 migrate만 해도 됨)

  ```shell
  (venv) $ docker-compose exec backend python manage.py makemigrations
  (venv) $ docker-compose exec backend python manage.py migrate
  ```

 - static 파일 정리하기를 해주세요

  ```shell
  (venv) $ docker-compose exec backend python manage.py collectstatic
  ```


### Create admin user

- Admin 사용자가 필요하면 다음과 같이 실행 (이후 아이디, 이메일, 비밀번호 설정)

  ```shell
  (venv) $ docker-compose exec backend python manage.py createsuperuser
  ```

## urls

- 메인페이지 : http://127.0.0.1

- 백엔드(어드민) : http://127.0.0.1:8000/admin/

## Related command

- 생성된 도커 이미지 전부 보기

  ```shell
  (venv) $ docker images
  ```

  ```shell
  (venv) $ docker image ls
  ```

- 도커 이미지 삭제하기

  ```shell
  (venv) $ docker image -q
  ```

- 삭제할 이미지 이름 확인 후 이름 복사,
  
  ```shell
  (venv) $ docker rmi -f 이미지이름
  ```
- -f 태그 붙이면 강제 삭제

- 생성된(올라가 있는) 도커 컨테이너 전부 보기

  ```shell
  (venv) $ docker container ls
  ```

- 생성된(올라가 있는) 도커 컨테이너 삭제
  ```shell
  (venv) $ docker container rm
  ```

- 위와 같은 방법으로 volume과 network도 삭제 및 조회 가능

- 도커 컨테이너 테스트 (도커 컨테이너 올려둔 상태에서)

  ```shell
  (venv) $ docker-compose exec backend python manage.py test
  ```

 - 현재는 배포용으로 실행 중. 따라서 페이지에 구체적인 오류 메시지가 보이지 않음

 - 아래를 실행하여 docker-compose 파일 옵션 변경하여 실행 가능(개발자 용 .dev)

  ```shell
  (venv) $ docker-compose -f docker-compose.dev.yml up
  ```

 - 도커 오류 시 로그 보기

  ```shell
  (venv) $ docker-compose logs
  ```

## Set PowerShell alias

- Windows 이용자일 경우 PowerShell의 `Set-Alias` 기능 사용해서 단축어 사용 가능
- PowerShell을 열고 다음 명령어를 입력:
  ```powershell
    echo $profile
  ```
- 결과물로 출력된 경로를 확인하고, 같은 곳에 파일을 만든 뒤, `profile.ps1` 파일의 내용물을 넣으면 됨
- 이후 `profile.ps1`에 정의된 단축어 사용 가능 (e.g., `dku`)
