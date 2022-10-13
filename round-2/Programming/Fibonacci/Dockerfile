FROM golang:1.19.1-alpine

WORKDIR /app
COPY . .
RUN go build -o fibonacci
EXPOSE 57777

CMD ["./fibonacci"]
