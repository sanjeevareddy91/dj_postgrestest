docker build -t dj_postgres .
docker image tag dj_postgres sanjeevasimply/dj_postgres
docker image push sanjeevasimply/dj_postgres

export DOCKER_HOST=tcp://50.16.224.216:2375
docker-compose -f docker-compose.yml run djangoweb python /var/projects/djangofinal/manage.py collectstatic
docker-compose -f docker-compose.yml run djangoweb python /var/projects/djangofinal/manage.py migrate
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml down -v --rmi all
