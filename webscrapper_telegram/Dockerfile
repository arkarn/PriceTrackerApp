FROM joyzoursky/python-chromedriver:3.7
COPY . /
WORKDIR /
RUN pip install -r requirements.txt
EXPOSE 5501
CMD [ "python3", "-u", "webscrapper.py"]