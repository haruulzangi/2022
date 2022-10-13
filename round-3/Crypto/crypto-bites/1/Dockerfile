FROM python:3.6-alpine
WORKDIR /dist

COPY src .
COPY flag.txt.enc .

CMD ["python", "-u", "app.py"]
EXPOSE 8777
