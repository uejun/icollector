FROM python:2-onbuild
MAINTAINER uejun

WORKDIR /usr/src/app
ENV FLASK_APP=interface.py

EXPOSE 5000
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
