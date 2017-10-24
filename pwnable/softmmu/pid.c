#include <stdio.h>

int main()
{
	int pid = getpid();
	char fmt[40] = {0};
 
	sprintf(fmt,"cat /proc/%d/maps",pid);

	system(fmt);
}
