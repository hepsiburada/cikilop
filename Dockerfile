FROM python:3.6.4-alpine3.7

ADD ./ /app
WORKDIR /app
RUN pip install -r ./requirements.txt

RUN  python -m unittest tests/unit_tests/*.py --verbose
RUN python -m unittest tests/integration_tests/*.py --verbose

ENV PYTHONPATH /app

ENTRYPOINT [ "python", "./src/ciki.py" ]