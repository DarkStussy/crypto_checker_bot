FROM python:3.12-alpine
RUN apk update
RUN apk add git gcc musl-dev linux-headers python3-dev

WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

WORKDIR /
COPY start.sh /start.sh
RUN chmod +x /start.sh

WORKDIR /src