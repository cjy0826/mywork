FROM python:3.13.9-slim

WORKDIR /mywork

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

COPY ./app ./app

RUN mkdir -p results data

CMD ["sh", "-c", "cd /mywork/app; pytest test_retrieval.py --maxfail=1 --disable-warnings -v > ../results/retrieval_test_output.txt"]
