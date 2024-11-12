# Have to pass mongo username and pass by env var
docker run --env-file .env -p 8000:8000 news_api