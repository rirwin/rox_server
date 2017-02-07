WIP readme

# rox_server
This project is designed to bring a simple client server model to rocksdb. 

The motivation is to share a key-store across different processes by a separate micro-service.



# For OS X:

## Install Python3.4 grab the installer from:

https://www.python.org/downloads/mac-osx/

## Install and start docker-machine
Instructions adapted from https://docs.docker.com/machine/install-machine/

cd ~/Downloads
curl -L https://github.com/docker/machine/releases/download/v0.8.2/docker-machine-`uname -s`-`uname -m` > docker-machine
sudo mv docker-machine /usr/local/bin/docker-machine
sudo chmod +x /usr/local/bin/docker-machine

Install virtualbox for OS X from https://www.virtualbox.org/wiki/Downloads

Create and start docker-machine with:

docker-machine create --driver virtualbox default
docker-machine env default   # just prints docker host info
eval "$(docker-machine env default)"

It is suggested to run rocksdb in a docker container.

## TODO instructutions for getting rocksdb to work on mac.  


## For OS X, grab the installer from:

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"



## For ubuntu 16.04, python 3.4 is not available through apt-get but compiling from source is pretty straightforward:

### get some basic dependencies
sudo apt-get update
apt-get install build-essential wget

### Download and install from source 
cd ~/Downloads
wget https://www.python.org/ftp/python/3.4.5/Python-3.4.5.tgz
tar xvfz Python-3.4.5.tgz
./configure
sudo make
sudo make install

sudo apt-get install python-pip python-pkg-resources python-setuptools python-virtualenv tox


 It is recommended to run rocksdb in a docker
sudo apt-get install libbz2-dev libgflags-dev libsnappy-dev zlib1g-dev 



## For windows visit https://www.ubuntu.com/ to get linux

