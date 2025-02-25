FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x entrypoints.sh

ENTRYPOINT ["./entrypoints.sh"]
