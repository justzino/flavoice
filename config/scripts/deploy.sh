#!/bin/bash

# Installing docker engine if not exists
if ! type docker > /dev/null
then
  echo "docker does not exist"
  echo "Start installing docker"
  sudo apt-get update
  sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
  sudo apt update
  apt-cache policy docker-ce
  sudo apt install -y docker-ce
  echo "Finish installing docker"
fi

# Installing docker-compose if not exists
if ! type docker-compose > /dev/null
then
  echo "docker-compose does not exist"
  echo "Start installing docker-compose"
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  echo "Finish installing docker-compose"
fi

# Installing AWS CLI if not exists
if ! type aws > /dev/null
then
  echo "AWS CLI does not exist"
  echo "Start installing AWS CLI"
  sudo apt install unzip
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
  echo "Finish installing AWS CLI"
fi

echo "docker-compose up"
sudo docker-compose -f /home/ubuntu/flavoice/docker-compose.prod.yml up --build -d

#echo "Login to the ECR repository"
#sudo aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 516199006501.dkr.ecr.ap-northeast-2.amazonaws.com
#
#echo "Push the images to ECR"
#sudo docker-compose -f /home/ubuntu/flavoice/docker-compose.prod.yml push
#
#echo "Pull the images from ECR"
#sudo docker pull 516199006501.dkr.ecr.ap-northeast-2.amazonaws.com/flavoice:web
#sudo docker pull 516199006501.dkr.ecr.ap-northeast-2.amazonaws.com/flavoice:nginx-proxy
#
#echo "Spin up the containers"
#sudo docker-compose -f docker-compose.prod.yml up -d
