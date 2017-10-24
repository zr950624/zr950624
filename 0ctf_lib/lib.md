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
paper:(0x20)   	double * point_num;   
	char * title;    	float price;    	char * publisher;    	char * author;    	int subject;    	DWORD is_paper;    	28-31: 0;    
```
```book:(0x34)   	void * func_table;	float price;	char * publisher;	char * author;	int subject;	DWORD is_paper;	28-31: 0;	int total_num;	36-52: 0;
```   
So we can see the length of book is longer than the paper.   
But for each option, the book and the paper will be processed in the same function.
In ***update the kindle***    
we can see the follow codes.   
```
int __usercall sub_21D50@<eax>(char *a1@<xmm0>, int a2){  char **v2; // esi@1  int v3; // eax@7  int v4; // eax@7  char v6; // [sp+7h] [bp-1h]@1  v6 = 121;  v2 = 0;  output_redirection(std::cout, "live or not (y/n)?: ");  sub_23D30(std::cin, &v6);  if ( v6 == 89 || v6 == 121 )  {    v2 = (char **)HeapAlloc(hHeap, 0, 8u);    *v2 = aLiveOnKindleNo;    sub_21460("kindle price");    v2[1] = a1;  }  else if ( v6 == 78 || v6 == 110 )  {    v2 = &off_2701C;  }  *(_DWORD *)(a2 + 44) = v2;  v3 = output_redirection(std::cout, "\n");  v4 = output_redirection(v3, "the book's kindle related information has been updated.");  return output_redirection(v4, "\n");}
```   
The function accepts a item number we give(whatever it is paper or book), then updates the `*(_DWORD *)(a2 + 44) = v2;`.   
But as we know, if the item is a paper structure, only 0x20(32) btes will be alloc.   
For this sake, that makes a written out of range.   
   
Also I found a stack overflow and heap overflow in the challenge.   
```
char __fastcall sub_22080(int a1, int a2){  int v2; // esi@1  int v3; // edi@1  const char *v4; // ebx@1  const char *v5; // edx@1  int v6; // eax@3  int v7; // eax@3  int v8; // eax@3  char result; // al@4  int v10; // eax@7  int v11; // eax@7  int v12; // eax@7  int v13; // eax@7  char v14; // [sp+Fh] [bp-49h]@1  char Dst; // [sp+10h] [bp-48h]@5  v2 = a1;  v14 = 89;  v3 = a2;  v4 = *(const char **)(a1 + 4);  output_redirection(std::cout, "\n");  v5 = "book #";  if ( *(_DWORD *)(v2 + 24) )    v5 = "paper #";  v6 = output_redirection(std::cout, v5);  std::basic_ostream<char,std::char_traits<char>>::operator<<(v6, v3);  v7 = output_redirection(std::cout, " has a title called ");  v8 = output_redirection(v7, v4);  output_redirection(v8, "\n");  output_redirection(std::cout, "do you want an update? (y/n)");  sub_23D30(std::cin, &v14);  getchar();  if ( *(_BYTE *)(*(_DWORD *)(std::cin + 4) + std::cin + 12) & 6 )  {    std::basic_ios<char,std::char_traits<char>>::clear(0, 0);    result = std::basic_istream<char,std::char_traits<char>>::ignore(std::cin, 1, 0, -1);  }  else  {    memset(&Dst, 0, 0x40u);    result = v14;    if ( v14 == 89 || v14 == 121 )    {      v10 = output_redirection(std::cout, "input your new title");      output_redirection(v10, "\n");      gets(&Dst);      memcpy((void *)v4, &Dst, strlen(&Dst));      v11 = output_redirection(std::cout, "the title is successfully updated to ");      v12 = output_redirection(v11, v4);      v13 = output_redirection(v12, ".");      result = output_redirection(v13, "\n");    }  }  return result;}
```   
See the codes above.   
`gets(&Dst);` will produce a stack overflow.   
` memcpy((void *)v4, &Dst, strlen(&Dst));` will make a heap overflow.   

**Exploitation**   
This program will run in window 10, full patch.   
That means we should face ASLR and DEP.    
But we still can find ways to pwn it. 
     
***to be continue***

