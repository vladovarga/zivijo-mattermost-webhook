FROM python:3.12.1-slim-bullseye

# Update the container
RUN ln -snf /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    echo "Etc/UTC" > /etc/timezone && \
    # update packages
    apt-get update && \
    apt-get -y upgrade && \
    apt-get clean && \
    # Install OS dependencies.
    apt-get install -y --no-install-recommends libmagic1 && \
    # clean up the apt cache to reduce image size
    # https://docs.docker.com/develop/develop-images/instructions/
    rm -rf /var/lib/apt/lists/*

# Move the required files into the container
RUN mkdir -p /app/src

WORKDIR /app

COPY src ./src
COPY LICENSE README.md requirements.txt /app/

# Install dependencies and build
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

CMD ["python", "./src/zivijo/__main__.py"]
