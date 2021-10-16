FROM python:3.8-slim-buster
COPY . /
WORKDIR /
RUN pip install -r requirements2.txt
EXPOSE 5502
CMD [ "python3", "-u", "appUI.py"]