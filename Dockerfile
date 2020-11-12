FROM debian:buster-slim



#### DEFINING VARS
ARG python_version=3



#### APPLICATION OPERATIONS
RUN apt-get update

# Installing system packages
RUN apt-get install -y -qq --force-yes \
    lsb-base \
	procps \
    python${python_version} \
	python${python_version}-pip \
        --no-install-recommends > /dev/null

# Installing pip modules
RUN python${python_version} -m pip install pika > /dev/null
RUN python${python_version} -m pip install mysql-connector-python > /dev/null
RUN python${python_version} -m pip install python-decouple > /dev/null
RUN python${python_version} -m pip install typing > /dev/null

####
# Creating a temporary folder for our app
RUN mkdir -p /tmp/app

# Download the entire project
COPY . /tmp/app/

# Create needed folders
RUN mkdir -p /app

# Moving application to the right place
RUN cp -r /tmp/app/* /app
RUN rm -rf /tmp/app
RUN touch /app/.env

# Changing permissions of the entire application
RUN chown root:root -R /app
RUN find /app -type f -exec chmod 644 {} \;
RUN find /app -type d -exec chmod 755 {} \;

# Crafting the entrypoint script
RUN rm -rf /entrypoint.sh && touch /entrypoint.sh
RUN echo "#!/bin/bash" >> /entrypoint.sh
RUN echo "shopt -s dotglob" >> /entrypoint.sh
RUN echo "python3 /app/main.py" >> /entrypoint.sh

RUN chown root:root /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Gaining a bit of comfort
WORKDIR "/app"

# Executing the scripts
ENTRYPOINT ["/entrypoint.sh"]