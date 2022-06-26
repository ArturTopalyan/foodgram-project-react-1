FROM python:3.7-slim
WORKDIR ../back
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]
