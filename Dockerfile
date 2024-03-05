# Choose the base image
FROM mcr.microsoft.com/mssql/server:2019-latest

# Create app directory
WORKDIR /usr/src/app

# Copy initialization scripts
COPY . /usr/src/app

# Expose port 1433 in case accessing from other container
EXPOSE 1433

CMD ["/bin/bash", "./init_db.sh"]