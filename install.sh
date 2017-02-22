#!/bin/sh
INSTALL_DIR=/var/opt/robot-vision
USER=pi
PASSWORD=123456
PYTHON_INSTALL_PATH=/usr/local/bin/cvpython
PYTHON_LOCATION=/home/pi/.virtualenvs/cv/bin/python
CV_LOCATION=/usr/local/lib/python2.7/site-packages/cv2.so
SERVICE=robot-vision.service
CONFIG_FILE=./config.properties
SYSTEMD_DIR=/etc/systemd/system
SRC_DIR=./src

# Check if we are root
if [ "$(id -u)" != "0" ]; then
	echo "Run as root" 1>&2
	exit 1
fi

# See if opencv is installed
if [ ! -f "$CV_LOCATION" ]; then
	echo "1. Please install OpenCV 3.2.0 into Python 2.7"
	echo "2. Create virtualenv named cv into pi user"
	echo "3. Make sure cv virtualenv can use cv2 module"
	exit 1
fi

# Create symlink if needed
if [ ! -f "$PYTHON_INSTALL_PATH" ]; then
	echo "Creating symlink to $PYTHON_LOCATION as $PYTHON_INSTALL_PATH"
	ln -s $PYTHON_LOCATION $PYTHON_INSTALL_PATH
fi

ret=false
getent passwd $USER > /dev/null 2>&1 && ret=true

# Create user if he doesnt exist
if $ret; then
	echo ""
else
	useradd -p $(openssl passwd -1 $PASSWORD) $USER -G users
fi

# Create service if needed, otherwise stop it
if [ ! -f "$SYSTEMD_DIR/$SERVICE" ]; then
	echo "Creating $SERVICE"
	cp $SERVICE $SYSTEMD_DIR/$SERVICE
	systemctl daemon-reload
	systemctl enable $SERVICE
else
	echo "Stopping $SERVICE"
	systemctl stop $SERVICE
fi

# Create Install dir if needed
if [ ! -d "$INSTALL_DIR" ]; then
	echo "Creating $INSTALL_DIR"
	mkdir $INSTALL_DIR
	chown -R $USER $INSTALL_DIR
fi

# Remove old files
find $INSTALL_DIR -maxdepth 1 -type f -not -name '*.properties' -delete

# Copy source folder
cp src/*.py $INSTALL_DIR/
cp $CONFIG_FILE $INSTALL_DIR/

# Change perms
chown -R $USER $INSTALL_DIR
chmod 644 $INSTALL_DIR/*.py

# Start service
systemctl start $SERVICE

