FROM python:3

WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
RUN pip install gunicorn
# ENTRYPOINT ["gunicorn", "--bind", "-w", "2", "-t", "2", "0.0.0.0:5000", "app:app"]