FROM ubuntu:latest

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y python3.11 python3-pip

RUN pip3 install -r requirements.txt

EXPOSE 443

CMD ["streamlit", "run", "Home_Page.py", "--server.port", "443", "--server.address", "0.0.0.0"]