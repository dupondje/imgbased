#!/usr/bin/bash

set -ex

export PATH=$PATH:/sbin/:/usr/sbin/

./autogen.sh
./configure

make image-install SQUASHFS_URL=$SQUASHFS_URL

IMG="$(make verrel).squashfs.img"
ln -v rootfs.squashfs.img $IMG

# Create an index file for imgbase remote
echo $IMG > .index

# Create a kickstart for a specific location
mv -v data/kickstarts/installation.ks auto-installation.ks

# Create an inteactive kickstart for a specific location
sed -e "/^clearpart / d" data/kickstarts/installation.ks > interactive-installation.ks
