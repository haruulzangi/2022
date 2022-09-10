# syntax=docker/dockerfile:1
FROM golang:alpine

WORKDIR /app

COPY *.go go.mod ./
RUN go build -o /app/server

CMD [ "/app/server" ]
