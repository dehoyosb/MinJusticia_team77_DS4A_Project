# Predicting and characterizing recidivism in Colombia between 2010 and 2019

#### [Correlation Once - Data Science for All](https://www.correlation-one.com/)
#### [Ministerio de Tecnologías, Información y Comunicación](https://www.mintic.gov.co/portal/inicio/)

#### Authors:
- [Sergio Bernal](https://www.linkedin.com/in/sergionbernal/)
- [Laura Goyeneche](https://www.linkedin.com/in/goyenechelaura/)
- [Esneyder Guerrero](https://www.linkedin.com/in/esneyder-guerrero-88282262/)
- [Daniel Hoyos](https://www.linkedin.com/in/daniel-hoyos-2b3a07a1/)
- [Katerin Lopez](https://www.linkedin.com/in/kaylopezal/)


#### Context
Colombia’s current situation regarding prison matters is very delicate and has generated plenty of controversy over the last few years due to the lack of capacity and adequate legislation. Since 1998, the overcrowding percentage has increased from 34% to nearly 50% in 2015 with roughly more than 42,000 convicts without a room. Moreover,  the attempts for solving this problem are very time consuming because they depend primarily on the judicial system which can take years for a law to make. Not to mention also that the betterment of the infrastructure requires high investments and bureaucratic processes that can be affected by administration changes. For this matter, the government has the need to evaluate the effectiveness of their criminal policy, including programs and services focused on individuals released from jails, to reduce the recidivism rate and therefore preventing, controlling and reducing the overcrowding rate mentioned.

#### Objective
Currently, the DPCP and the penitentiary entities are interested in characterizing the jail population in Colombia and their recidivism risk to establish patterns, tendencies, and groups to ensure an adequate formulation and monitoring of the criminal policy.

Recidivism is one of the critical indicators that allows measuring the impact that imprisonment has in the process of convict’s reinsertion in the society. In addition, it allows assessing the effectiveness of the policies that are being implemented in criminal law matter. Hence, we believe that in the development of this project we can positively impact social outcomes such as:

- Providing key and practical data-driven analysis and reference for the decision-making process of the resocialization policies
- Decreasing and optimizing public money spent on incarceration
- Guarantee an analysis focus on equity among historical and systemic disadvantage communities
- Provide key insights for making better strategies to reduce the recidivism risk

#### Codebase
1) The first part consist of the [data](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/tree/master/data/ministry_of_justice) we were given by the Ministry of Justice.
2) The second part consists of the [exploratory data analysis](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/tree/master/misc/eda), [supervised modeling experiments](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/tree/master/misc/supervised_learning), [unsupervised modeling experiments](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/tree/master/misc/unsupervised_learning) and the creation of the early [etl pipeline](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/tree/master/misc/etl)
3) The third part consist of the creating of the [figures](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/tree/master/misc/app-figures) that we wanted to add to our dashborad.
4) The fourth part consist on our [application](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/tree/master/app) by itself.

#### The App
In the app, we created several modules to control the flow of information to the desired dashboard. 

1) First of all we have a [backend module](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/tree/master/app/backend). It deals with all the [conection to the database and the interface to apply queries](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/blob/master/app/backend/utils.py), each query is special and needed to accomplish the overall objective. Also with the [initial preprocessing of the features](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/blob/master/app/backend/etl.py) to arrange them in the way we need them best. And finally, the code to add the [Human Development Index information](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/blob/master/app/backend/etl_sdhi.py).

2) Also we have a few files to construct the docker containers for the [database and a jupyter notebook](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/blob/master/app/docker/docker-compose.yml), which we use in the initial exploration.

3) We have a folder which contains the files to [create the tables](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/blob/master/app/setup_DB/ddl_normalizado.sql) and [insert all the data](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/blob/master/app/setup_DB/dml_tablas_parametros.sql) from the initial files given by the Ministry of Justice.

4) After completing the creation of the database, and creating the api to contect to it we have an [encoding module](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/tree/master/app/encoding_module). The purpose of it is to preprocess all the features in a particular way to use directly into the modeling part of the project, the classes contains a couple of encodings and we can add more if there is a need for it.

5) Additionally, we created a module that contains all the [plotting and metric functions](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/tree/master/app/utils). It is used to clear the space in the exploration notebooks and to have a one place this part of the process.

6) Finally, we have the [frontend module](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/tree/master/app/frontend). It contains the [app.py](https://github.com/dehoyosb/MinJusticia_team77_DS4A_Project/blob/master/app/frontend/app.py) file which is using [Dash by plotly](https://plotly.com/dash/) to create a service to deploy the dashboard with all the information of the project.
