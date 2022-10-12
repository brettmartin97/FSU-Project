# FSU-Project

Setup Container run:

**docker-compose up --build**

Navigate to:

**http://localhost**

pull request testgvn /.,


docker container ls

CONTAINER ID   IMAGE             COMMAND                  CREATED        STATUS          PORTS                                NAMES
6f1011bcdfe9   fsu-project-app   "python rest.py"         23 hours ago   Up 16 seconds   0.0.0.0:80->5000/tcp                 fsu-project-app-1
427d81e0c15d   mysql:8.0.21      "docker-entrypoint.s…"   26 hours ago   Up 17 seconds   33060/tcp, 0.0.0.0:30000->3306/tcp   fsu-project-db-1 


docker exec -it fsu-project-db-1 bash

mysql -u root -p

mysql> use fsu