# Use an official Node.js runtime as a parent image
FROM node:14-alpine

# Set the working directory in the container to /app
WORKDIR /usr/local/app

# Copy package.json and package-lock.json, then install dependencies
COPY package*.json ./
RUN npm install
COPY public ./public
# Copy the rest of the directory contents into the container at /app
COPY src ./src

# Run npm start on container launch
CMD ["npm", "start"]