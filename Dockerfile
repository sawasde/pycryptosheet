FROM python:3.10

WORKDIR /home

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENV BIN_API_KEY
ENV BIN_API_SECRET

#ENTRYPOINT ["python", "pycryptosheet.py"]