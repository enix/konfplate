FROM python:alpine

ARG VERSION=0.1
LABEL konfplate_version=$VERSION

WORKDIR /src/config-template

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY konfplate.py konfplate
RUN chmod +x konfplate

ENV KONFPLATE_VERSION=$VERSION
ENTRYPOINT [ "./konfplate" ]
CMD [ "--help" ]