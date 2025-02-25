FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y netcat
RUN chmod +x entrypoints.sh

ENTRYPOINT ["./entrypoints.sh"]
