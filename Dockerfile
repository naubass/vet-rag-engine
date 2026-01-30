# Python Image
FROM python:3.11

# Set Working Directory
WORKDIR /code

# Copy Requirements & Install
COPY ./backend/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy Kode & Data
COPY ./backend/app /code/app
COPY ./backend/data /code/data
COPY ./frontend /code/frontend

# Setup Cache
RUN mkdir -p /code/cache && chmod 777 /code/cache
ENV HF_HOME=/code/cache

CMD ["sh", "-c", "python -m app.rag.ingest && uvicorn app.main:app --host 0.0.0.0 --port 7860"]