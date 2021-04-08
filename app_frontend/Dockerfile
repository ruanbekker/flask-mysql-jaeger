FROM python:3.7-alpine
RUN apk --no-cache add gcc musl-dev libc-dev libc6-compat linux-headers build-base git libffi-dev openssl-dev
WORKDIR /src
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app.py .
CMD ["python3", "/src/app.py"]
