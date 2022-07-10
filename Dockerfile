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
#COPY requirements.txt .

RUN pip install discord
RUN pip install python-dotenv

# Install dependencies
#RUN pip install -r requirements.txt

# Run the program
CMD python3 run.py
