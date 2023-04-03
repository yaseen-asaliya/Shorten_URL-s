# Shorten_URL-s

### Private DNS
* Install necessary utilities
```
# yum install bind bind-utils -y
```
* Edit BIND DNS configuration file `/etc/named.conf` and add `shorten.url` zone
```
options {
    listen-on port 53 { 127.0.0.1; 10.0.2.9; };
    allow-query     { localhost; 10.0.2.0/24; };
    allow-transfer  { localhost; 10.0.2.0/24; };
};

zone "shorten.url" IN {
    type master;
    file "/var/named/shorten.url.zone";
    allow-update { none; };
};
```
* Create a zone file in `/var/named/shorten.url.zone`
```
$TTL 86400
@   IN  SOA shorten.url. root.shorten.url. (
        2016010101  ; serial
        3600        ; refresh
        1800        ; retry
        604800      ; expire
        86400       ; minimum
)
@   IN  NS  shorten.url.
@   IN  A   10.0.2.9
```
* Ser servername in `/etc/resolv.conf`
```
nameserver 10.0.2.9
```
* Change owner and permissions for zone file 
```
# chown named:named /var/named/shorten.url.zone
# chmod 640 /var/named/shorten.url.zone
```
* Restart the BIND DNS server to apply the new configuration
```
# systemctl restart named
```
* To check the DNS status 
```
# dig shorten.url
```

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
