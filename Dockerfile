FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
# CMD ["gunicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 app.main:app