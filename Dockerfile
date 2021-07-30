#---------------------------------------------------------------------------
# Dockefile to build Docker Image of Apache WebServer running on Ubuntu
#
# Made by Denis Astahov ADV-IT  13-March-2019
#---------------------------------------------------------------------------

FROM ubuntu:20.04

# Переключаем Ubuntu в неинтерактивный режим — чтобы избежать лишних запросов
ENV DEBIAN_FRONTEND noninteractive 
# Устанавливаем локаль
RUN locale-gen ru_RU.UTF-8 && dpkg-reconfigure locales 

# Добавляем необходимые репозитарии и устанавливаем пакеты
RUN apt-get update
RUN apt-get upgrade -y
RUN sudo apt install python-pip
RUN pip install -r requirements.txt

RUN python3 main.py
