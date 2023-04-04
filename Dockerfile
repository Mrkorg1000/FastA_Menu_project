FROM python:3.9-alpine

RUN mkdir /menu_proj

WORKDIR /menu_proj
COPY poetry.lock .
COPY pyproject.toml .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]