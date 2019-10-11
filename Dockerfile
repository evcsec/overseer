FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN wget https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN export 

COPY . .

CMD [ "python", "./overseer.py" ]