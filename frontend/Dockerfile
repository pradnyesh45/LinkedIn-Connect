# Build stage
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port 3000 (React's default development port)
EXPOSE 3000

# Start the app in development mode
CMD ["npm", "start"] 