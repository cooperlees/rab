FROM python:3-slim

RUN mkdir -p /src/rab && mkdir /config
ADD default_config.json /config/rab.json
ADD CHANGES.md README.md setup.py requirements.txt /src/
ADD rab/ /src/rab

RUN find /src
RUN pip --no-cache-dir install --upgrade pip setuptools wheel
RUN pip --no-cache-dir install --upgrade -r /src/requirements.txt
RUN pip --no-cache-dir install /src/

RUN rm -r /src

CMD ["rab"]
