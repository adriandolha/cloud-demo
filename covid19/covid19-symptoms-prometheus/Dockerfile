FROM python:3.6

RUN useradd demo

WORKDIR /home/demo

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements.txt requirements.txt

COPY . .
RUN pip install /home/demo/

ENV FLASK_APP app.py
RUN chown -R demo:demo /home/demo
USER demo

EXPOSE 8081
CMD ["python","app.py","8081","http://localhost:8000/symptoms/metrics"]