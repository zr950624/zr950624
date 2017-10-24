#LIB 
**introduce**   
This challenge is in ***0ctf final***, powered by Xu Wen(memeda).   
In the competition, I didn't work it out. But these days I redid it, and find the way the pwn it(at least the clues)
   
**exploration of vulnerability**    
This program alloc to struct to store book and paper.
But they are not in the same size.    
***0x34*** bytes for a book.   
``` v7 = HeapAlloc(hHeap, 0, 0x34u);```    
***0x20*** bytes for a paper.    
``` v15 = HeapAlloc(hHeap, 0, 0x20u);```      

Analyzing the details of book and paper, we can get the fields of each structure.   
```   
paper:(0x20)   
	char * title;    
```
```
```   
So we can see the length of book is longer than the paper.   
But for each option, the book and the paper will be processed in the same function.
In ***update the kindle***    
we can see the follow codes.   
```
int __usercall sub_21D50@<eax>(char *a1@<xmm0>, int a2)
```   
The function accepts a item number we give(whatever it is paper or book), then updates the `*(_DWORD *)(a2 + 44) = v2;`.   
But as we know, if the item is a paper structure, only 0x20(32) btes will be alloc.   
For this sake, that makes a written out of range.   
   
Also I found a stack overflow and heap overflow in the challenge.   
```
char __fastcall sub_22080(int a1, int a2)
```   
See the codes above.   
`gets(&Dst);` will produce a stack overflow.   
` memcpy((void *)v4, &Dst, strlen(&Dst));` will make a heap overflow.   

**Exploitation**   
This program will run in window 10, full patch.   
That means we should face ASLR and DEP.    
But we still can find ways to pwn it. 
     
***to be continue***
