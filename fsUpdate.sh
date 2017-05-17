#!/bin/sh

mv /var/fspanel /var/fspanel.1

tar czvf fspanel.tar.gz /var/fspanel.1
# tar xzvf fspanel.tar.gz -C /var/fspanel.1

cd /home/pi/git/fspanel
git pull
cp -r * /var/fspanel.2

ln -s /var/fspanel.2 /var/fspanel

rm /var/fspanel
ln -s /var/fspanel.1 /var/fspanel

