FROM node:latest

# envrionment variables
ENV dir /app
ENV port 8080

# create /app and copy files
RUN mkdir -p ${dir}
COPY . ${dir}
WORKDIR ${dir}

# install NPM packages
RUN npm install

# open TCP port 8080
EXPOSE ${port}

# start chat bot service
CMD ["node", "server.js"]

# health check every 30 seconds to ensure pages are served within 3 seconds
# NOTE: you cannot use ENV variables in CMD and HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8080/ || exit 1

