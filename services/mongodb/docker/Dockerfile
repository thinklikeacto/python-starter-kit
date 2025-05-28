FROM mongo:6

# Add custom configuration
COPY config/mongod.conf /etc/mongod.conf

# Add initialization scripts
COPY init/ /docker-entrypoint-initdb.d/

# Set configuration file
CMD ["mongod", "--config", "/etc/mongod.conf"]

# Default port
EXPOSE 27017 