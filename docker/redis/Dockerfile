# Base redis image
FROM redis:4.0.9

# Create the tmp directory to hold the unix socket file.
RUN mkdir -p /etc/redis/ /tmp/docker/
RUN chmod -R 777 /tmp/docker/

# Copy the redis configuration file to the docker image.
COPY redis.conf /etc/redis/
