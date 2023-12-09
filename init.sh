#! /bin/bash Ubuntu 22.04
echo "Updating apt-get"
sudo apt-get update -y && sudo apt-get upgrade -y

echo "Updating git"
sudo apt-get install git -y

echo "Installing curl"
sudo apt-get install curl -y

echo "Installing wget"
sudo apt-get install wget -y

echo "Installing vim"
sudo apt-get install vim -y

# Install docker
echo "Installing docker"
sudo apt-get install docker.io -y

# Install docker-compose
echo "Installing docker-compose"
sudo apt-get install docker-compose -y

# Install python 3.11.6
echo "Installing python 3.11.6"
sudo apt-get install python3.11.6 -y

# Change default python to python 3.11.6
echo "Changing default python to python 3.11.6"
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11.6 1

