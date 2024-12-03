FROM nginx:1.26.2-alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY frontend /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]