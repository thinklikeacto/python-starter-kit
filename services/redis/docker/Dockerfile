FROM redis:7-alpine

# Add custom configuration
COPY config/redis.conf /usr/local/etc/redis/redis.conf

# Set configuration file
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]

# Default port
EXPOSE 6379 