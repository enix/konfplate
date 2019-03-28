FROM golang:1.10
WORKDIR /root/
COPY konfplate.go .
RUN go get -d -v && CGO_ENABLED=0 GOOS=linux go build -a konfplate.go

FROM alpine:latest
ARG VERSION=2
COPY --from=0 /root/konfplate /bin/
ENTRYPOINT [ "konfplate" ]
CMD [ "--help" ]
