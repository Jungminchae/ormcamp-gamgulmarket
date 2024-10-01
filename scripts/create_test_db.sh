#!/bin/bash

# 데이터베이스 설정
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_HOST="localhost"
DB_PORT="5432"
TEST_DB_NAME="test"
CONTAINER_NAME="gamgul-postgres"  

docker exec -e PGPASSWORD=$DB_PASSWORD $CONTAINER_NAME \
    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c "CREATE DATABASE $TEST_DB_NAME;"

# hstore 확장 추가
docker exec -e PGPASSWORD=$DB_PASSWORD $CONTAINER_NAME \
    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $TEST_DB_NAME -c "CREATE EXTENSION IF NOT EXISTS hstore;"