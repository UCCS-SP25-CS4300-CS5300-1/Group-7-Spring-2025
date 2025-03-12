FROM node:23.9.0 as build

WORKDIR /app

# Install requirements
COPY package*.json /app
RUN npm install --legacy-peer-deps

# Install app
COPY . /app
EXPOSE 3000
CMD ["npm", "start"]


# # Stage 2: Serve with Nginx
# FROM nginx:alpine
# COPY --from=build /app/build /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]
