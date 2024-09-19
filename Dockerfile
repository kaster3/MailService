FROM python:3.12

ENV PYTHONBUFFERED=1

WORKDIR /app

RUN pip install -U pip "poetry==1.8.3"
RUN poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

CMD ["make", "run"]
