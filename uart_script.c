#include <stdlib.h>

int main() {
	setuid(0);
	char* script = "./enable-uart.sh";
	int status = system(script);
	return 0;
}
