FROM node:23-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN adduser -D web
USER web

CMD [ "node", "index.js" ]