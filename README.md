# FSU-Project

## Prequisites
[Docker Installation](https://www.docker.com/products/docker-desktop/)

[Git Installation](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Clone Repo:

Open Command Line Tool, navigate to location where repository should be placed and run:

**git clone https://github.com/brettmartin97/FSU-Project.git**

## Setup Container to run:

Open a terminal session and run the following command on your localhost in the project folder (location with docker-compose.yml):

**docker-compose up --build**

Note: Due to matplotlib download and install, expect the first build to take ~30 minutes

Navigate to:

**http://localhost**

## Docker Notes
#### Docker Storage Management
docker container ls

docker [builder/image/container] prune 

#### Docker Container Interation
docker exec -it fsu-project-db-1 bash

mysql -u root -p

mysql> use fsu
