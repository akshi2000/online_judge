PROFILE=guest
MASTER_PROFILE=root
SCHROOT_DIR="/home/$PROFILE/compile-run"
UBUNTU_VERSION=bionic
MEMLIMIT=128M

# install cgroup-tools
apt install cgroup-tools -y

# Adds a new profile where compilation will happen
# Reading and writing previledges of this profile is
# controlled by the master profile
adduser $PROFILE --disabled-password -q
chown $MASTER_PROFILE "/home/$PROFILE"
chgrp $MASTER_PROFILE "/home/$PROFILE"

echo "[INFO]: user created"

# # installing schroot
apt install schroot -y
apt install debootstrap -y

echo "[INFO]: schroot install complete"

# # setting up schroot
install -d $SCHROOT_DIR


echo "
[compile-run]
type=directory
description=schroot profile for compilation
directory=$SCHROOT_DIR
users=$PROFILE
root-groups=root
" >> /etc/schroot/schroot.conf

echo "[INFO]: schroot setup complete"

# installing linux system in schroot
debootstrap --variant=buildd --arch amd64 $UBUNTU_VERSION $SCHROOT_DIR http://archive.ubuntu.com/ubuntu/

echo "[INFO]: virtual system build complete"

schroot -c compile-run --directory /home/$PROFILE/ -- apt update -y
schroot -c compile-run --directory /home/$PROFILE/ -- apt upgrade -y
schroot -c compile-run --directory /home/$PROFILE/ -- apt install software-properties-common -y
schroot -c compile-run --directory /home/$PROFILE/ -- add-apt-repository ppa:deadsnakes/ppa
schroot -c compile-run --directory /home/$PROFILE/ -- apt update -y
schroot -c compile-run --directory /home/$PROFILE/ -- apt install python3 -y

chown $MASTER_PROFILE "$SCHROOT_DIR"
chgrp $MASTER_PROFILE "$SCHROOT_DIR"

# # add executable file
# echo 'sudo unshare -n su - guest -c "schroot -c compile-run -- timeout 15 python3 /home/ubuntu/harm.py"' > /usr/bin/safecompile
# chmod 755 /usr/bin/safecompile


# # add memory limiter systemd service
# echo "[Unit]
# Description=compile
# After=network.target 

# [Service]
# User=root
# Group=root
# Environment=DISPLAY=:0
# ExecStart=/usr/bin/safecompile
# #Restart=on-failure
# KillMode=process
# MemoryAccounting=true
# MemoryMax=$MEMLIMIT

# [Install]
# WantedBy=multi-user.target
# " > /etc/systemd/system/compile.service

# systemd-analyze verify /etc/systemd/system/compile.service
# systemctl enable compile.service
# systemctl start compile.service

