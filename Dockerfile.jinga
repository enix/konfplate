FROM python:alpine

WORKDIR /src/config-template

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY konfplate.py konfplate
RUN chmod +x konfplate

ENTRYPOINT [ "./konfplate" ]
CMD [ "--help" ]