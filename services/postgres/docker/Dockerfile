FROM postgres:15-alpine

# Add custom configuration
COPY config/postgresql.conf /etc/postgresql/postgresql.conf
COPY config/pg_hba.conf /etc/postgresql/pg_hba.conf

# Add initialization scripts
COPY init/ /docker-entrypoint-initdb.d/

# Set configuration file
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]

# Default port
EXPOSE 5432 