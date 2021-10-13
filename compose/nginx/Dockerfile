# stage1 as builder
FROM node:14-alpine as builder

# copy the package.json to install dependencies
COPY front-dashboard/package.json  ./

# Install the dependencies and make the folder
RUN npm install -f && mkdir /react-ui && mv ./node_modules ./react-ui

WORKDIR /react-ui

COPY ./front-dashboard/ .

# Build the project and copy the files
RUN npm run build


FROM checkitout_django as django

RUN /app/manage.py collectstatic --noinput


FROM nginx:alpine

#!/bin/sh

COPY ./compose/nginx/local.conf /etc/nginx/conf.d/default.conf

## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder /react-ui/build /srv/static

COPY --from=django /app/media/static /srv/static/static
COPY ./public/assets /srv/static/assets
COPY ./public/landing.html /srv/static/
COPY ./.certs /srv/certs


EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]

