FROM node:latest

WORKDIR /app

# Install requirements
RUN npm install

# Install app
COPY . /app
EXPOSE 3000
CMD ["npm", "start"]
