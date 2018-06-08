FROM nginx:1.15.0
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY pytwask.template /etc/nginx/conf.d/ 
