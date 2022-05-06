FROM phusion/baseimage:master

CMD ["/sbin/my_init"]
# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Install python3.6 & pip
RUN apt-get update && \
    apt-get install -y python3.8 && \
    apt-get install -y python3-pip && \
    apt-get clean;

RUN apt-get update && \
   apt-get install -y openjdk-8-jdk && \
   apt-get install -y ant && \
   apt-get clean;

RUN python3 -m pip install -U pip
# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

# create root directory for our project in the container
RUN mkdir /mantistablex-tool.py

# Set the working directory
WORKDIR /mantistablex-tool.py

# Copy the current directory contents into the container
ADD ./requirements.txt /mantistablex-tool.py/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt