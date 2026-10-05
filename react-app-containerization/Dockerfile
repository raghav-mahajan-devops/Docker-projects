FROM node:20-alpine

WORKDIR /react-app

COPY package*.json ./

RUN npm install 

COPY . .

CMD ["npm", "run", "dev"]
