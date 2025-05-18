#!/bin/bash
host=$DB_HOST
port=$DB_PORT
until mysqladmin ping -h "$host" -P "$port" --silent; do
  echo "Waiting for database at $host:$port..."
  sleep 1
done
echo "Database is ready!"