#!/bin/bash

sudo mkdir -p /mnt/nfs/home
sudo mount -t nfs 192.168.1.1:/home /mnt/nfs/home/

sudo useradd -d /mnt/nfs/home -M student
echo "student:student" | sudo chpasswd
