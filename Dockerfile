FROM python:3.11

WORKDIR /code

COPY ./backend/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./backend/app /code/app

COPY ./frontend /code/frontend

RUN mkdir -p /code/cache && chmod 777 /code/cache
ENV HF_HOME=/code/cache

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]