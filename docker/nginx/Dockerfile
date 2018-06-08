# Base nginx image
FROM nginx:1.15.0

# Copy nginx configuration files to the docker image.
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY pytwask.conf /etc/nginx/conf.d/
