#!/bin/python
import os
import json
import subprocess
import sys


# Command information
HAMMR_CMD = "/usr/bin/hammr" 
HAMMR_CREDENTIALS = os.path.expanduser("~") + "/.hammr/credentials.json"

# Docker information
DOCKER_CMD = "/usr/bin/docker"
DOCKER_AUTHOR = "usharesoft"
DOCKER_CREDENTIALS = os.path.expanduser("~") + "/.dockercfg"

# Template information
IMAGE_PATH="image.tar.gz"
TEMPLATE_FILENAME = "template.json"

# Check if Hammr is correctly installed
if not os.path.isfile(HAMMR_CMD):
        print "Unable to find " + HAMMR_CMD + ". Please install it before."
        exit(1)

if len(sys.argv) != 2:
	print "You must call this script with the git release/tag in argument. example: python build.py 3.6.0.1"
	exit(1)


# Check there is a hammr authentication file
if not os.path.isfile(HAMMR_CREDENTIALS):
	print "Unable to find " + HAMMR_CREDENTIALS + ". Please refer to : http://hammr.io/?page_id=1189"
	exit(1)

# Retrieve some information from the server template metadata
with open(TEMPLATE_FILENAME) as data_file:    
	data = json.load(data_file)

template_name = data["stack"]["name"]
template_version = data["stack"]["version"]
docker_repository = DOCKER_AUTHOR + "/" + template_name
docker_image = docker_repository + ":" + template_version
print "######"
print "###### Building docker image " + docker_image
print "######"

# Creating the template based on the template.json
cmd = HAMMR_CMD + " template create --file " + TEMPLATE_FILENAME + " --force"
ret = os.system(cmd)
if ret != 0:
	print "Error while creating template for " + docker_image
	exit(1)

# Generating a tar.gz image of the previously created template
cmd = HAMMR_CMD + " template build --file " + TEMPLATE_FILENAME + " | grep 'Image Id : ' | sed 's/Image Id : \(.*\)/\\1/g'"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out, err = p.communicate()
ret = p.returncode
if ret != 0:
	print "Error while generating a tar.gz image for " + docker_image
	exit(1)
image_id = out.rstrip('\r\n')

# Downloading the tar.gz image of the previously generated image
cmd = HAMMR_CMD + " image download --id " + image_id + " --file " + IMAGE_PATH
ret = os.system(cmd)
if ret != 0:
        print "Error while while downloading image for " + docker_image
        exit(1)

# Check if Hammr is correctly installed
if not os.path.isfile(IMAGE_PATH):
        print "Unable to find " + HAMMR_CMD + ". Please install it before."
        exit(1)

# Convert the tar.gz image to a Docker image
print "Converting the tar.gz image to a Docker image"
cmd = "cat " + IMAGE_PATH + " | docker import - " + docker_image
ret = os.system(cmd)
if ret != 0:
        print "Error while creating template for " + docker_image
        exit(1)

print "Docker image successfully built : " + docker_image


file = os.path.join(os.getcwd(), os.listdir(os.getcwd())[0])
SOURCE_PATH = os.path.dirname(os.path.dirname(file)) + "/src"


# run the docker image
print "run the Docker image"
cmd = "docker run -t -i -v "+SOURCE_PATH + ":/mnt " + docker_image + " sh -c 'sh /etc/UShareSoft/firstboot/1_install-rpmvenv.sh'"
ret = os.system(cmd)
if ret != 0:
        print "Error while running docker image: " + docker_image
        exit(1)
