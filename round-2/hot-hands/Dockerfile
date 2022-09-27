FROM python:3.6-alpine
WORKDIR /dist
RUN apk add --update build-base libffi-dev openssl-dev
COPY src/requirements.txt /dist/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && mkdir db
COPY src .

CMD ["python", "-u", "app.py"]
EXPOSE 8777
