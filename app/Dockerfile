FROM centos

RUN yum update -y
RUN yum install python3 -y
RUN yum install python3-psycopg2 -y

#RUN pip install --upgrade setuptools
# copy the app to the image 

WORKDIR /App
COPY App .

# install requirements 
RUN pip3 install -r requirements.txt

CMD [ "python3", "./app.py", "runserver" ]
EXPOSE 5000



