FROM jupyter/scipy-notebook

USER root
RUN apt-get update &&\
  apt-get install curl apt-transport-https libv8-dev unixodbc unixODBC* odbc-postgresql python python-pip build-essential libcurl4-gnutls-dev libxml2-dev libssl-dev libpq-dev libsasl2-dev python-dev libldap2-dev libssl-dev libz-dev openjdk-8-jre openjdk-8-jdk unixodbc-dev -y

RUN pip install jupyter_contrib_nbextensions
RUN conda install -c conda-forge jupyter_contrib_nbextensions

RUN conda install --quiet --yes \
    'pyodbc' \
    'pandas' \
    'Psycopg2' && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

EXPOSE 8888



