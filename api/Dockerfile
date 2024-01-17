FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app

COPY ./api/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./api /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 