# 가상머신의 베이스 이미지 선택
# ubuntu 16.04 version 생성
FROM    ubuntu:16.04

# Dockerfile 관리자의 이름 및 이메일 정보(빌드에는 영향이 없는 사항)
MAINTAINER  DoHyang Kim "hanoul1124@gmail.com"

# shell 환경변수
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Docker 컨테이너 생성 및 실행 후 진행시킬 명령어
# 기본적인 업데이트부터 실행
RUN apt -y update
RUN apt -y dist-upgrade

# python3-pip install
RUN apt -y install python3-pip

# requirements.txt로 패키지 설치
COPY    requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# 현재 폴더 내부에 있는 모든 파일을 복사하여
# 생성될 Docker 이미지의 /srv/project/ 안에 붙여넣는다
# Git으로부터 Clone받은 소스코드들을 Docker로 옮겨 서버를 실행하기 위함
COPY    ./ /srv/project/

# Working Directory 변경
WORKDIR /srv/project/app

# collectstatic으로 정적파일 정리
RUN python3 manage.py collectstatic --noinput

# 서버 실행
CMD python3 manage.py runserver 0:8000



