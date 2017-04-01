UART_DEVICE=/dev/ttyS0
USER=root
GROUP=gpio

echo "Enabling UART"
chown $USER.$GROUP $UART_DEVICE
chmod g+rw $UART_DEVICE
echo "UART Enabled for users in group $GROUP"
