FROM golang:1.19.1-alpine

WORKDIR /app
COPY . .
RUN go build -o prime
EXPOSE 57778

CMD ["./prime"]
