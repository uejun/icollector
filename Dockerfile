FROM python:3-onbuild
MAINTAINER uejun

WORKDIR /usr/src/app

EXPOSE 9000
ENTRYPOINT ["python", "icollector.py", "web"]
