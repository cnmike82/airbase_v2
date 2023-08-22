FROM python:3.9

ENV streamlit_APP=airbase_app.py

RUN apt-get -y update
RUN apt-get -y upgrade

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

WORKDIR /app
COPY . .

EXPOSE 8501

ENTRYPOINT [ "streamlit", "run"]

CMD ["airbase_app.py"]