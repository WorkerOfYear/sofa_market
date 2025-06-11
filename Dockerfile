FROM python:3.12 AS python-base

RUN mkdir sofa_server

WORKDIR  /sofa_server

COPY /pyproject.toml /sofa_server

RUN pip3 install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . .

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]