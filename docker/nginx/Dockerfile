FROM nginx:1.25-alpine

ARG nginx_uid=1000
ARG nginx_gid=1000

RUN apk add shadow && usermod -u $nginx_uid -o nginx && groupmod -g $nginx_gid -o nginx
