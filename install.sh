#!/bin/sh
#Install Dirs
INSTALL_DIR=/var/opt/robot-vision
UART_INSTALL_DIR=/var/opt/uart-enable

# User to run vision service as
USER=pi
PASSWORD=raspberry

# User to run UART-enabler as
UART_USER=root
UART_GROUP=root

# Install directory of python
PYTHON_INSTALL_PATH=/usr/local/bin/cvpython
PYTHON_LOCATION=/home/pi/.virtualenvs/cv/bin/python

# Location of opencv package
CV_LOCATION=/usr/local/lib/python2.7/site-packages/cv2.so

# Name of services
SERVICE=robot-vision.service
UART_SERVICE=uart-enable.service

# Name of the config file
CONFIG_FILE=./config.properties

# Destination dirs
SYSTEMD_DIR=/etc/systemd/system
SRC_DIR=./src
UART_SCRIPT=./enable-uart.sh
UART_SRC=uart_script.c
UART_OUT=uart-enable

# Compile options
COMPILE=gcc
COMPILE_OUT=-o

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

# Delete UART-service if needed
if [ -f "$SYSTEMD_DIR/$UART_SERVICE" ]; then
	systemctl stop $UART_SERVICE
	echo "Deleting $UART_SERVICE"
	rm -f $SYSTEMD_DIR/$UART_SERVICE
fi

# Delete service if needed, otherwise stop it
if [ -f "$SYSTEMD_DIR/$SERVICE" ]; then
	systemctl stop $SERVICE
	echo "Deleting $SERVICE"
	rm -f $SYSTEMD_DIR/$SERVICE
fi

# Copy over service files
echo "Copying over $SERVICE and $UART_SERVICE"
cp $SERVICE $SYSTEMD_DIR/$SERVICE
cp $UART_SERVICE $SYSTEMD_DIR/$UART_SERVICE

if [ ! -d "$UART_INSTALL_DIR" ]; then
	echo "Creating $UART_INSTALL_DIR"
	mkdir $UART_INSTALL_DIR
	chown -R $UART_USER.$UART_GROUP $UART_INSTALL_DIR
fi

# Install uart script
echo "Installing UART Enable script"
cp $UART_SCRIPT $UART_INSTALL_DIR/$UART_SCRIPT

# Compile C program to run UART script
echo "Compiling $UART_SRC to $UART_OUT"
$COMPILE $COMPILE_OUT $UART_OUT $UART_SRC
cp $UART_OUT $UART_INSTALL_DIR/$UART_OUT
chmod +x $UART_INSTALL_DIR/$UART_OUT
rm $UART_OUT

if [ ! -d "$INSTALL_DIR" ]; then
	echo "Creating $INSTALL_DIR"
	mkdir $INSTALL_DIR
	chown -R $USER $INSTALL_DIR
fi

echo "Installing Vision Service"
find $INSTALL_DIR -maxdepth 1 -type f -not -name '*.properties' -delete

# Copy source folder
cp src/*.py $INSTALL_DIR/
cp $CONFIG_FILE $INSTALL_DIR/

# Change perms
chown -R $USER $INSTALL_DIR
chmod 644 $INSTALL_DIR/*.py

# Enable services
echo "Enabling Services"
systemctl daemon-reload
systemctl enable $UART_SERVICE
systemctl enable $SERVICE

# Start service
echo "Starting Services"
systemctl start $UART_SERVICE
systemctl start $SERVICE
