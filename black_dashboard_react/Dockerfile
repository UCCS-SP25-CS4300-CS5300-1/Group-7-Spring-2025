FROM node:latest

WORKDIR /app

# Install requirements
COPY package*.json /app
RUN npm install

# Install app
COPY . /app
EXPOSE 3000
CMD ["npm", "start"]
