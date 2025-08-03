# Stage 1: Build the React app
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:1.25-alpine

# Copy the build output from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]