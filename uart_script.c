#include <stdlib.h>

int main() {
	setuid(0);
	char* script = "/var/opt/uart-enable/enable-uart.sh";
	int status = system(script);
	return 0;
}
