FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["streamlit", "run", "Home_Page.py", "--server.port", "8000", "--server.address", "0.0.0.0"]