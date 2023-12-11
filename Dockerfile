FROM ubuntu:latest

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y python3.11 python3-pip

RUN pip3 install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "Home_Page.py"]