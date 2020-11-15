FROM python:3-slim

RUN mkdir /src && mkdir /config
ADD default_config.json /config/rab.json
ADD CHANGES.md README.md setup.py requirements.txt rab /src/

RUN pip --no-cache-dir install --upgrade pip setuptools
RUN pip --no-cache-dir install --upgrade -r /src/requirements.txt
RUN pip --no-cache-dir install /src/

RUN rm -r /src

CMD ["rab"]
