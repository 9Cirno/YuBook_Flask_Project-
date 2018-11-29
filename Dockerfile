FROM python:3.7.1
COPY . /fisher
WORKDIR /fisher
RUN pip install -r requirements.txt
EXPOSE 80
CMD [ "python", "fisher/Main.py" ]