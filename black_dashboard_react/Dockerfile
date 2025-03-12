FROM node:23.9.0

WORKDIR /app

# Install requirements
COPY package*.json /app
RUN npm install --legacy-peer-deps

# Install app
COPY . /app
EXPOSE 3000
CMD ["npm", "start"]
