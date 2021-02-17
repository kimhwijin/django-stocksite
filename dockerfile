FROM python:3.8.1

COPY . /stocksite
#app name
WORKDIR /stocksite

RUN pip install --upgrade pip 
RUN python3 -m pip install django
RUN pip install -r requirements.txt

ADD requirements.txt /stocksite/

CMD

EXPOSE 8000
