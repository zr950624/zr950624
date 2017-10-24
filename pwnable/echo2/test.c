#include <stdio.h>
#include <string.h>

int main()
{
	char s[30] = {0};
	gets(s);
	printf("%d\n",strlen(s));

	return 0;
}
