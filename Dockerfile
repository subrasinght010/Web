FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*
RUN chmod +x entrypoints.sh

ENTRYPOINT ["./entrypoints.sh"]
