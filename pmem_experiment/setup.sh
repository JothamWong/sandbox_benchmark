#!/bin/bash

sudo apt-get update
sudo apt-get install ndctl daxctl

sudo ndctl create-namespace -f -e namespace0.0 --mode=fsdax
sudo mkfs.xfs /dev/pmem0
sudo mkdir -p /mnt/pmem0
sudo mount -o dax /dev/pmem0 /mnt/pmem0
mount | grep pmem0