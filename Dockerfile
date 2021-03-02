FROM python:3.9-alpine

WORKDIR /app
ENV PYTHONPATH "/app/lib"
ENV ENV production

COPY Pipfile.lock .
COPY Pipfile .

RUN pip install pipenv \
  && pipenv lock --requirements > requirements.txt \
  && pip install -r requirements.txt

USER nobody

COPY . .

ENTRYPOINT ["python", "main.py"]
