FROM python:3.10-slim
WORKDIR ../backend
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]
