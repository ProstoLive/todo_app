echo "DROP DATABASE todo; CREATE DATABASE todo" | psql -h 127.0.0.1 -p 5433 -U postgres
psql -h 127.0.0.1 -p 5433 -U postgres todo < init.sql