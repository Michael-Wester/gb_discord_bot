FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
  build-essential \
  libsdl2-dev \
  python3 \
  python3-pip \
  python3-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && pip3 install pyboy

#Set working directory
WORKDIR /app

COPY . .

#Copy files from the host machine to the container
RUN pip install azure-storage-blob
RUN pip install discord
RUN pip install python-dotenv
RUN pip install pandas

# Run the program
CMD python3 run.py
