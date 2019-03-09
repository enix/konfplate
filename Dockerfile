FROM python:alpine

ARG VERSION=0.1
LABEL config_template_version=$VERSION

WORKDIR /src/config-template

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV CONFIG_TEMPLATE_VERSION=$VERSION TRUC=12
ENTRYPOINT [ "python", "./config-template.py" ]
CMD [ "--help" ]