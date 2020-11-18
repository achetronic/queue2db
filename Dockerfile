# Use always Ubuntu LTS versions
FROM ubuntu:20.04



#### APPLICATION OPERATIONS
RUN apt-get update

# Installing system packages
RUN apt-get install -y -qq --force-yes \
    at \
    lsb-base \
	procps \
    python3 \
	python3-pip \
        --no-install-recommends > /dev/null

# Installing pip modules
RUN python3 -m pip install pika > /dev/null
RUN python3 -m pip install mysql-connector-python > /dev/null
RUN python3 -m pip install python-decouple > /dev/null

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
RUN echo "service atd start" >> /entrypoint.sh
RUN echo "sh /app/runtime/takeover.sh" >> /entrypoint.sh
RUN echo "/bin/bash" >> /entrypoint.sh

# Giving permissions to the entrypoint script
RUN chown root:root /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Giving permissions to the livenessprobe script
RUN chown root:root /app/runtime/livenessprobe.sh
RUN chmod +x /app/runtime/livenessprobe.sh

# Giving permissions to the takeover script
RUN chown root:root /app/runtime/takeover.sh
RUN chmod +x /app/runtime/takeover.sh

# Gaining a bit of comfort
WORKDIR "/app"

# Executing the scripts
ENTRYPOINT ["/entrypoint.sh"]