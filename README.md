# Shorten_URL-s

### Private DNS
* 

## Database Side
* Pull mariadb docker image
```
# docker pull mariadb
```
* Create docker compose file `setup-database.yml` with mariadb database image and create a new user `yaseen` and database called `monitoring_app`
```
version: "3"

services:
  db:
    image: mariadb
    container_name: my_db
    env_file: .env
    ports:
      - "3306:3306"
```
* Create `.env` file 
```
MYSQL_ROOT_PASSWORD: root
MYSQL_DATABASE: monitoring_app
MYSQL_USER: yaseen
MYSQL_PASSWORD: yaseen
```
* Run a docker compose file 
```
# docker compose -f setup-database.yml up -d
```
* To connect to the database 
```
# mysql -P 3306 --protocol=tcp -u yaseen -pyaseen
```

> 
* Here are some photo for demo
![Screenshot 2023-02-15 213406](https://user-images.githubusercontent.com/59315877/220185823-57bd3de9-a9c7-4459-8665-6122e9248d20.png)
![Screenshot 2023-02-15 213444](https://user-images.githubusercontent.com/59315877/220185929-336fdda9-66f8-4b83-9f90-7abed3c3b5cb.png)
