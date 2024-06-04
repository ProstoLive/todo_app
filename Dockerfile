FROM python:3.12

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--port", "8000"]

#CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
# Если используете прокси-сервер, такой как Nginx или Traefik, добавьте --proxy-headers
# CMD ["uvicorn", "code.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]