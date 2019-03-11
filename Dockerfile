FROM python:alpine

ARG VERSION=0.1
LABEL config_template_version=$VERSION

WORKDIR /src/config-template

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY config-template.py .
RUN chmod +x config-template.py

ENV CONFIG_TEMPLATE_VERSION=$VERSION TRUC=12
ENTRYPOINT [ "./config-template.py" ]
CMD [ "--help" ]