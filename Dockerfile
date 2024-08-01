FROM python:3 as python

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

#CMD [ "python", "./your-daemon-or-script.py" ]