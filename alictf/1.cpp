#define NDEBUG
#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <ctype.h>
#include <assert.h>
#include <signal.h>
#include <time.h>
#include <pthread.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <event2/event.h>
#include <event2/buffer.h>
#include <event2/bufferevent.h>
#include <zlog.h>
#include <unistd.h>
#include <sys/stat.h>

#include <iostream>
#include <fstream>
#include <string>
#include <tr1/unordered_map>
using namespace std;

#define SUCCESS 0
#define FAIL -1
#define BUFF_SIZE 100
#define PORT 30000
#define LISTEN_BACKLOG 512
#define SOCKET_TIMEOUT_SECOND 5
#define MAX_SOCKET_NUM 50000
#define MAX_USER_SOCKET_NUM 1
#define UINT_SIZE 4
#define MAX_REQUEST_DATA_SIZE 1024
#define MAX_TOKEN_SIZE 255
#define MAX_REQUEST_SIZE MAX_TOKEN_SIZE+MAX_REQUEST_DATA_SIZE + 2 + UINT_SIZE
#define MAX_RESPONSE_DATA_SIZE 1024
#define MAX_RESPONSE_SIZE MAX_RESPONSE_DATA_SIZE + UINT_SIZE
#define DURABLE_INTERVAL_SECOND 3
#define MAX_FUNCTION_ID 7
#define SAFE_SPACE_LEN 130

#define TOKEN_FILE "/rpcserver/token.data"
#define TOKEN_FILE_TMP "/rpcserver/token.data.tmp"
#define zlog_conf_file_path  "/rpcserver/zlog.conf"
#define zlog_category_name  "rpc_server"
#define pid_file_path  "/rpcserver/rpc_server.pid"

#define hstr__alloc(x) malloc (x)
#define hstr__free(p) free (p)
#define hstr__realloc(p,x) realloc ((p), (x))
#define hstr__memcpy(d,s,l) memcpy ((d), (s), (l))
#define hstr__memset(d,c,l) memset ((d), (c), (l))
#define hstr__memmove(d,s,l) memmove ((d), (s), (l))
#define hBlockCopy(D,S,L) { if ((L) > 0) hstr__memmove ((D),(S),(L)); }
#define SAFE_POSITIVE(x) ( x = x > 0 ? x : x + SAFE_SPACE_LEN ) > 0

zlog_category_t * handle = NULL;

typedef struct tag_request_t {
	unsigned char len_token;
	char *token;
	unsigned char fucntion_id;
	unsigned int len_data;
	char *data;
} request_t;

typedef struct tag_response_t {
	unsigned int len_data;
	char *data;
} response_t;

typedef struct tag_user_t {
	int retry_num;
} user_t;

typedef struct tag_global_context_t {
	int fd_listen;
	struct event_base *event_base;
	struct event *accept_event;
	int socket_alive_number;
	std::tr1::unordered_map<string, user_t> user_map;
} context_global_t;

typedef struct tag_socket_context_t {
	context_global_t *context_global;
	int fd_client;
	struct sockaddr_in sin_client;
	struct bufferevent *bev_client;
	request_t *request;
	response_t *response;
	int error_code;
} context_socket_t;

typedef enum tag_error_code_t {
	EMPTY = 0,
	TOO_MUCH_DATA ,
	ILLEGAL_FUNCTION_ID,
	ILLEGAL_TOKEN_LENGTH,
	ILLEGAL_DATA_LENGTH,
	ILLEGAL_TOKEN,
	EXCEED_MAX_RETRY,
	SOCKET_TIMEOUT,
	SOCKET_ERROR,
	SOCKET_CLOSE,
	MEMORY_ERROR,
	ERROR_COUNT
} error_code_t;

typedef struct taghstring * hstring;
typedef const struct taghstring * const_hstring;

struct taghstring {
	int mlen;
	int slen;
	unsigned char * data;
};

typedef struct tag_len_str_t{
	char len;
	char string[128];
} len_str_t;

typedef struct tag_req_t{
	len_str_t str1;
	len_str_t str2;
	int pos;
	char len;
	char secretKey[50];
	int logRequest;
} req_t;

char *error_msg[ERROR_COUNT] = {
		"Empty",
		"Too much request data",
		"Illegal function id",
		"The length of token cannot be zero or more than 255",
		"The length of data cannot be zero or more than 1024",
		"Illegal token",
		"Sorry, you have reach the max retry limit, no more chance-_-",
		"Socket timeout",
		"Socket error",
		"Socket close",
		"Memory error"
};

response_t *create_response(unsigned int len_data, char *data);
void destroy_response(response_t *response);
void send_response(context_socket_t *context);

context_socket_t *create_context_socket();
void destroy_context_socket(context_socket_t *context);

static int extendSize (int i) {
	if (i < 8) {
		i = 8;
	} else {
		unsigned int j;
		j = (unsigned int) i;
		j |= (j >>  1);
		j |= (j >>  2);
		j |= (j >>  4);
		j |= (j >>  8);	
#if (UINT_MAX != 0xffff)
		j |= (j >> 16);	
#if (UINT_MAX > 0xffffffffUL)
		j |= (j >> 32);	
#endif
#endif
		j++;
		if ((int) j >= i) i = (int) j;
	}
	return i;
}

int halloc (hstring b, int olen) {
	int len;

	if (b == NULL || b->data == NULL || b->slen < 0 || b->mlen <= 0 || 
	    b->mlen < b->slen || olen <= 0) {
		return FAIL;
	}

	if (olen >= b->mlen) {
		unsigned char * x;

		if ((len = extendSize (olen)) <= b->mlen) return SUCCESS;

		if (7 * b->mlen < 8 * b->slen) {

			reallocStrategy:;

			x = (unsigned char *) hstr__realloc (b->data, (size_t) len);
			if (x == NULL) {
				if (NULL == (x = (unsigned char *) hstr__realloc (b->data, (size_t) (len = olen)))) {
					return FAIL;
				}
			}
		} else {
			if (NULL == (x = (unsigned char *) hstr__alloc ((size_t) len))) {
				goto reallocStrategy;
			} else {
				if (b->slen) hstr__memcpy ((char *) x, (char *) b->data, (size_t) b->slen);
				hstr__free (b->data);
			}
		}
		b->data = x;
		b->mlen = len;
		b->data[b->slen] = (unsigned char) '\0';
	}
	return SUCCESS;
}

int hdestroy (hstring b) {
	if (b == NULL || b->slen < 0 || b->mlen <= 0 || b->mlen < b->slen ||
	    b->data == NULL)
		return FAIL;

	hstr__free (b->data);
	b->slen = -1;
	b->mlen = -__LINE__;
	b->data = NULL;
	hstr__free (b);
	return SUCCESS;
}

hstring hfromcstr (const char * str) {
	hstring b;
	int i;
	size_t j;

	if (str == NULL) return NULL;
	j = (strlen) (str);
	i = extendSize ((int) (j + (2 - (j != 0))));
	assert(i > j);

	if (i <= (int) j) return NULL;

	b = (hstring) hstr__alloc (sizeof (struct taghstring));
	if (NULL == b) return NULL;
	b->slen = (int) j;
	if (NULL == (b->data = (unsigned char *) hstr__alloc (b->mlen = i))) {
		hstr__free (b);
		return NULL;
	}

	hstr__memcpy (b->data, str, j+1);
	return b;
}

hstring hstrcpy (const_hstring b) {
	hstring b0;
	int i,j;

	if (b == NULL || b->slen < 0 || b->data == NULL) return NULL;

	b0 = (hstring) hstr__alloc (sizeof (struct taghstring));
	if (b0 == NULL) {
		return NULL;
	}

	i = b->slen;
	j = extendSize (i + 1);

	b0->data = (unsigned char *) hstr__alloc (j);
	if (b0->data == NULL) {
		j = i + 1;
		b0->data = (unsigned char *) hstr__alloc (j);
		if (b0->data == NULL) {
			hstr__free (b0);
			return NULL;
		}
	}

	b0->mlen = j;
	b0->slen = i;

	if (i) hstr__memcpy ((char *) b0->data, (char *) b->data, i);
	b0->data[b0->slen] = (unsigned char) '\0';

	return b0;
}

int hconcat (hstring b0, const_hstring b1) {
	int len, d;
	hstring aux = (hstring) b1;

	if (b0 == NULL || b1 == NULL || b0->data == NULL || b1->data == NULL) return FAIL;

	d = b0->slen;
	len = b1->slen;
	assert(d + len > 0);
	if ((d | (b0->mlen - d) | len | (d + len)) < 0) return FAIL;

	if (b0->mlen <= d + len + 1) {
		ptrdiff_t pd = b1->data - b0->data;
		if (0 <= pd && pd < b0->mlen) {
			if (NULL == (aux = hstrcpy (b1))) return FAIL;
		}
		if (halloc (b0, d + len + 1) != SUCCESS) {
			if (aux != b1) hdestroy (aux);
			return FAIL;
		}
	}

	hBlockCopy (&b0->data[d], &aux->data[0], (size_t) len);
	b0->data[d + len] = (unsigned char) '\0';
	b0->slen = d + len;
	if (aux != b1) hdestroy (aux);
	return SUCCESS;
}

int hinsert (hstring b1, int pos, const_hstring b2, unsigned char fill) {
	int d, l;
	ptrdiff_t pd;
	hstring aux = (hstring) b2;

	if (pos < 0 || b1 == NULL || b2 == NULL || b1->slen < 0 || 
	    b2->slen < 0 || b1->mlen < b1->slen || b1->mlen <= 0) return FAIL;

	if ((pd = (ptrdiff_t) (b2->data - b1->data)) >= 0 && pd < (ptrdiff_t) b1->mlen) {
		if (NULL == (aux = hstrcpy (b2))) return FAIL;
	}

	d = b1->slen + aux->slen;
	l = pos + aux->slen;
	assert(d > 0);
	assert(l > 0);
	if ((d|l) < 0) {
		hdestroy(aux);
		return FAIL;
	}

	if (l > d) {
		if (halloc (b1, l + 1) != SUCCESS) {
			if (aux != b2) hdestroy (aux);
			return FAIL;
		}
		hstr__memset (b1->data + b1->slen, (int) fill, (size_t) (pos - b1->slen));
		b1->slen = l;
	} else {
		if (halloc (b1, d + 1) != SUCCESS) {
			if (aux != b2) hdestroy (aux);
			return FAIL;
		}
		hBlockCopy (b1->data + l, b1->data + pos, d - l);
		b1->slen = d;
	}
	hBlockCopy (b1->data + pos, aux->data, aux->slen);
	b1->data[b1->slen] = (unsigned char) '\0';
	if (aux != b2) hdestroy (aux);
	return SUCCESS;
}

int hsetstr (hstring b0, int pos, const_hstring b1, unsigned char fill) {
	int d, newlen;
	ptrdiff_t pd;
	hstring aux = (hstring) b1;

	if (pos < 0 || b0 == NULL || b0->slen < 0 || NULL == b0->data || 
	    b0->mlen < b0->slen || b0->mlen <= 0) return FAIL;
	if (b1 != NULL && (b1->slen < 0 || b1->data == NULL)) return FAIL;

	d = pos;

	if (NULL != aux) {
		if ((pd = (ptrdiff_t) (b1->data - b0->data)) >= 0 && pd < (ptrdiff_t) b0->mlen) {
			if (NULL == (aux = hstrcpy (b1))) return FAIL;
		}
		d += aux->slen;
	}

	if (halloc (b0, d + 1) != SUCCESS) {
		if (aux != b1) hdestroy (aux);
		return FAIL;
	}

	newlen = b0->slen;

	if (pos > newlen) {
		hstr__memset (b0->data + b0->slen, (int) fill, (size_t) (pos - b0->slen));
		newlen = pos;
	}

	if (aux != NULL) {
		hBlockCopy ((char *) (b0->data + pos), (char *) aux->data, aux->slen);
		if (aux != b1) hdestroy (aux);
	}

	if (d > newlen) newlen = d;

	b0->slen = newlen;
	b0->data[newlen] = (unsigned char) '\0';

	return SUCCESS;
}

int hreplace (hstring b1, int pos, int len, const_hstring b2, 
		  unsigned char fill) {
	int pl, ret;
	ptrdiff_t pd;
	hstring aux = (hstring) b2;

	if (pos < 0 || len < 0 || (pl = pos + len) < 0 || b1 == NULL || 
	    b2 == NULL || b1->data == NULL || b2->data == NULL || 
	    b1->slen < 0 || b2->slen < 0 || b1->mlen < b1->slen ||
	    b1->mlen <= 0) return FAIL;

	if (pl >= b1->slen) {
		if ((ret = hsetstr (b1, pos, b2, fill)) < 0) return ret;
		if (pos + b2->slen < b1->slen) {
			b1->slen = pos + b2->slen;
			b1->data[b1->slen] = (unsigned char) '\0';
		}
		return ret;
	}

	if ((pd = (ptrdiff_t) (b2->data - b1->data)) >= 0 && pd < (ptrdiff_t) b1->slen) {
		if (NULL == (aux = hstrcpy (b2))) return FAIL;
	}

	if (aux->slen > len) {
		if (halloc (b1, b1->slen + aux->slen - len) != SUCCESS) {
			if (aux != b2) hdestroy (aux);
			return FAIL;
		}
	}

	if (aux->slen != len) hstr__memmove (b1->data + pos + aux->slen, b1->data + pos + len, b1->slen - (pos + len));
	hstr__memcpy (b1->data + pos, aux->data, aux->slen);
	b1->slen += aux->slen - len;
	b1->data[b1->slen] = (unsigned char) '\0';
	if (aux != b2) hdestroy (aux);
	return SUCCESS;
}

int hdelete (hstring b, int pos, int len) {
	if (pos < 0) {
		len += pos;
		pos = 0;
	}
	assert(len > 0);
	if (len < 0 || b == NULL || b->data == NULL || b->slen < 0 || 
	    b->mlen < b->slen || b->mlen <= 0) 
		return FAIL;
	if (len > 0 && pos < b->slen) {
		if (pos + len >= b->slen) {
			b->slen = pos;
		} else {
			hBlockCopy ((char *) (b->data + pos),
			            (char *) (b->data + pos + len), 
			            b->slen - (pos+len));
			b->slen -= len;
		}
		b->data[b->slen] = (unsigned char) '\0';
	}
	return SUCCESS;
}

int hstrcmp (const_hstring b0, const_hstring b1) {
	int i, v, n;

	if (b0 == NULL || b1 == NULL || b0->data == NULL || b1->data == NULL ||
		b0->slen < 0 || b1->slen < 0) return SHRT_MIN;
	n = b0->slen; 
	if (n > b1->slen) n = b1->slen;
	if (b0->slen == b1->slen && (b0->data == b1->data || b0->slen == 0))
		return SUCCESS;

	for (i = 0; i < n; i ++) {
		v = ((char) b0->data[i]) - ((char) b1->data[i]);
		if (v != 0) return v;
		if (b0->data[i] == (unsigned char) '\0') return SUCCESS;
	}

	if (b0->slen > n) return 1;
	if (b1->slen > n) return -1;
	return SUCCESS;
}

int validkey(req_t* req){
	char *key = "c4852c709698e3270a9966692ed1e373f453b599e5aca3e6";
	if(strcmp(req->secretKey,key))
		return FAIL;	
	else
		return SUCCESS;
}

int writelog(char* token,unsigned char len_token,req_t* req,char* response){
	char filename[512] = "/rpcserver/";
	char buffer[1024];

	memcpy(filename + 11,token,len_token);
	memcpy(filename + 11 + len_token,".log",5);

	int fd = open(filename,O_WRONLY|O_CREAT|O_APPEND,0644);
	
	if(fd < 0)
		return FAIL;

	snprintf(buffer,1024,"str1:%s\nstr2:%s\n",req->str1.string,req->str2.string);
	write(fd,buffer,strlen(buffer));
	snprintf(buffer,1024,"pos:%d\nlen:%d\n",req->pos,(int)(req->len));
	write(fd,buffer,strlen(buffer));
	snprintf(buffer,1024,"%s\n",response);
	write(fd,buffer,strlen(buffer));
	close(fd);
	return SUCCESS;
}

int readlog(char* token,unsigned char len_token,req_t* req,char* response){
    int fd;
    int pos = req->pos;
    char len = req->len;
    char filename[512] = "/rpcserver/";
    char *filecontent;
	int filesize = 0;
    struct stat buf;

    if(pos < 0)
    	return FAIL;
    if(len < 0){
    	pos = pos + len;
        len = -len;
    }
    assert(SAFE_POSITIVE(len));

    memcpy(filename + 11,token,len_token);
    memcpy(filename + 11 + len_token,".log",5);

    if((fd = open(filename,O_RDONLY,0644)) < 0)
        return FAIL;
    if(fstat(fd,&buf) < 0){
        close(fd);
        return FAIL;
    }
    filesize = buf.st_size;
    if(pos < 0 || pos > filesize || pos + len > filesize || (filecontent = (char*)malloc(filesize)) == NULL ){
        close(fd);
        return FAIL;
    }

    if(filesize != read(fd,filecontent,filesize)){
        close(fd);
        free(filecontent);
        return FAIL;
    }
	
	char l = len;
	do{
		response[l] = filecontent[pos + l];
		l--;
	}while(l >= 0);
	
	close(fd);
	free(filecontent);
	return SUCCESS;
}

response_t *rpc_strcat(request_t *request) {
	req_t req;
	memcpy(&req,request->data,sizeof(req_t));
	if(req.str1.len != strlen(req.str1.string) || req.str2.len != strlen(req.str2.string) || req.pos != 0 || req.len != 0 || validkey(&req) == FAIL){
		char *message = "Wrong Argument.";
		return create_response(strlen(message), message);
	}

	hstring h1 = hfromcstr(req.str1.string);
	hstring h2 = hfromcstr(req.str2.string);
	if(SUCCESS != hconcat(h1,h2)){
		hdestroy(h1);
		hdestroy(h2);
		char *message = "Operation Error.";
		return create_response(strlen(message), message);
	}
	char message[1024];
	snprintf(message,1024,"%s",h1->data);
	
	if(req.logRequest)
		writelog(request->token,request->len_token,&req,message);
	
	response_t *response = create_response(strlen(message),message);
	hdestroy(h1);
	hdestroy(h2);
	return response;
}

response_t *rpc_insert(request_t *request){
	req_t req;
	memcpy(&req,request->data,sizeof(req_t));
	if(req.str1.len != strlen(req.str1.string) || req.str2.len != strlen(req.str2.string) || req.pos > 512 || req.len != 0  || validkey(&req) == FAIL){
		char *message = "Wrong Argument.";
		return create_response(strlen(message), message);
	}
	
	hstring h1 = hfromcstr(req.str1.string);
	hstring h2 = hfromcstr(req.str2.string);
	if(SUCCESS != hinsert(h1,req.pos,h2,' ')){
		hdestroy(h1);
		hdestroy(h2);
		char *message = "Operation Error.";
		return create_response(strlen(message), message);		
	}
	char message[1024];
	snprintf(message,1024,"%s",h1->data);
	
	if(req.logRequest)
		writelog(request->token,request->len_token,&req,message);
	
	response_t *response = create_response(strlen(message),message);
	hdestroy(h1);
	hdestroy(h2);
	return response;	
}

response_t *rpc_setstr(request_t *request){
	req_t req;
	memcpy(&req,request->data,sizeof(req_t));
	if(req.str1.len != strlen(req.str1.string) || req.str2.len != strlen(req.str2.string) || req.pos > 512 || req.len != 0 || validkey(&req) == FAIL){
		char *message = "Wrong Argument.";
		return create_response(strlen(message), message);
	}
	
	hstring h1 = hfromcstr(req.str1.string);
	hstring h2 = hfromcstr(req.str2.string);
	if(SUCCESS != hsetstr(h1,req.pos,h2,' ')){
		hdestroy(h1);
		hdestroy(h2);
		char *message = "Operation Error.";
		return create_response(strlen(message), message);		
	}
	char message[1024];
	snprintf(message,1024,"%s",h1->data);
	
	if(req.logRequest)
		writelog(request->token,request->len_token,&req,message);
	
	response_t *response = create_response(strlen(message),message);
	hdestroy(h1);
	hdestroy(h2);
	return response;	
}

response_t *rpc_replace(request_t *request){
	req_t req;
	memcpy(&req,request->data,sizeof(req_t));
	if(req.str1.len != strlen(req.str1.string) || req.str2.len != strlen(req.str2.string) || req.pos > 512 || req.len > 127 || validkey(&req) == FAIL){
		char *message = "Wrong Argument.";
		return create_response(strlen(message), message);
	}
	
	hstring h1 = hfromcstr(req.str1.string);
	hstring h2 = hfromcstr(req.str2.string);
	if(SUCCESS != hreplace(h1,req.pos,req.len,h2,' ')){
		hdestroy(h1);
		hdestroy(h2);
		char *message = "Operation Error.";
		return create_response(strlen(message), message);		
	}
	char message[1024];
	snprintf(message,1024,"%s",h1->data);
	
	if(req.logRequest)
		writelog(request->token,request->len_token,&req,message);
	
	response_t *response = create_response(strlen(message),message);
	hdestroy(h1);
	hdestroy(h2);
	return response;	
}

response_t *rpc_delete(request_t *request){
	req_t req;
	memcpy(&req,request->data,sizeof(req_t));
	if(req.str1.len != strlen(req.str1.string) || req.str2.len != strlen(req.str2.string) || req.str2.len != 0 || req.pos > 127 || req.len > 127  || validkey(&req) == FAIL){
		char *message = "Wrong Argument.";
		return create_response(strlen(message), message);
	}
	
	hstring h1 = hfromcstr(req.str1.string);
	if(SUCCESS != hdelete(h1,req.pos,req.len)){
		hdestroy(h1);
		char *message = "Operation Error.";
		return create_response(strlen(message), message);		
	}
	char message[1024];
	snprintf(message,1024,"%s",h1->data);
	
	if(req.logRequest)
		writelog(request->token,request->len_token,&req,message);
	
	response_t *response = create_response(strlen(message),message);
	hdestroy(h1);
	return response;	
}

response_t *rpc_strcmp(request_t *request) {
	req_t req;
	memcpy(&req,request->data,sizeof(req_t));
	if(req.str1.len != strlen(req.str1.string) || req.str2.len != strlen(req.str2.string) || req.pos != 0 || req.len != 0 || validkey(&req) == FAIL){
		char *message = "Wrong Argument.";
		return create_response(strlen(message), message);
	}
	
	hstring h1 = hfromcstr(req.str1.string);
	hstring h2 = hfromcstr(req.str2.string);
	int result = hstrcmp(h1,h2);	
	char message[1024];
	
	if(result == SHRT_MIN){
		hdestroy(h1);
		hdestroy(h2);
		char *message = "Operation Error.";
		return create_response(strlen(message), message);
	}
	else if(result < 0)
		snprintf(message,1024,"string1 < string2");
	else if(result > 0)
		snprintf(message,1024,"string1 > string2");
	else
		snprintf(message,1024,"string1 = string2");
	
	if(req.logRequest)
		writelog(request->token,request->len_token,&req,message);
	
	response_t *response = create_response(strlen(message),message);
	hdestroy(h1);
	hdestroy(h2);
	return response;
}

response_t *rpc_readlog(request_t *request){
	req_t req;
	memcpy(&req,request->data,sizeof(req_t));
	if(req.str1.len != strlen(req.str1.string) || req.str2.len != strlen(req.str2.string) || req.str1.len != 0 || req.str2.len != 0 || req.pos < 0 || req.len == 0 || validkey(&req) == FAIL){
		char *message = "Wrong Argument.";
		return create_response(strlen(message), message);
	}
	
	char *buffer;
	char len = req.len;
	
	if(len < 0)
		len = -len;
	if((buffer = (char*)malloc(len + SAFE_SPACE_LEN)) == NULL){
		char *message = "Malloc Error.";
		return create_response(strlen(message),message);
	}
	memset(buffer,0,len + SAFE_SPACE_LEN);
	if((readlog(request->token,request->len_token,&req,buffer)) < 0){
		free(buffer);
		char *message = "Operation Error.";
		return create_response(strlen(message),message);
	}
	
	response_t *response = create_response(len,buffer);
	free(buffer);
	return response;
}

response_t *rpc_test(request_t *request) {

	char *message = "Test Function Called.";
	return create_response(strlen(message), message);
}

response_t *create_response(unsigned int len_data, char *data) {
	if (data == NULL || len_data == 0){
		return NULL;
	}
	if (len_data > MAX_RESPONSE_DATA_SIZE) {
		len_data = MAX_RESPONSE_DATA_SIZE;
	}
	response_t *response = (response_t *) malloc(sizeof(response_t));
	if (response == NULL){
		return NULL;
	}
	response->len_data = len_data;
	response->data = (char *) malloc(len_data * sizeof(char));
	if (response->data == NULL){
		free(response);
		return NULL;
	}
	memcpy(response->data, data, len_data);
	return response;
}

void destroy_response(response_t *response) {
	if (response == NULL)
		return;
	if (response->data != NULL)
		free(response->data);
	free(response);
}

void send_response(context_socket_t *context) {
	if (context == NULL || context->bev_client == NULL
		|| context->response == NULL || context->response->data == NULL) {
		destroy_context_socket(context);
		return;
	}
	char response_buffer[MAX_RESPONSE_SIZE];
	unsigned int network_len_data = htonl(context->response->len_data);
	memcpy(response_buffer, &network_len_data, UINT_SIZE);
	memcpy(response_buffer+UINT_SIZE,context->response->data, context->response->len_data);
	if (bufferevent_write(context->bev_client, response_buffer, UINT_SIZE + context->response->len_data) < 0) {
		destroy_context_socket(context);
	}
}

void response_error(context_socket_t *context){
	context->response = create_response(
			strlen(error_msg[context->error_code]),
			error_msg[context->error_code]);
	send_response(context);
}

int recv_request(context_socket_t *context) {
	if (context == NULL)
		return FAIL;

	char buffer[MAX_REQUEST_SIZE];
	struct evbuffer* ev_buffer = bufferevent_get_input(context->bev_client);
	unsigned int len_buffer = evbuffer_copyout(ev_buffer, buffer, MAX_REQUEST_SIZE);
	if (len_buffer < 1) {
		return FAIL;
	}

	unsigned int len_token = (unsigned char) buffer[0];
	if (len_token <=0  || len_token > MAX_TOKEN_SIZE){
		context->error_code = ILLEGAL_TOKEN_LENGTH;
		response_error(context);
		return FAIL;
	}

	if (len_buffer < len_token + 2 + UINT_SIZE) {
		return FAIL;
	}

	unsigned int function_id = (unsigned char) buffer[len_token + 1];
	if (function_id > MAX_FUNCTION_ID) {
		context->error_code = ILLEGAL_FUNCTION_ID;
		response_error(context);
		return FAIL;
	}

	unsigned int network_len_data;
	memcpy(&network_len_data, buffer + len_token + 2, UINT_SIZE);
	unsigned int host_len_data = ntohl(network_len_data);

	if (host_len_data <= 0 || host_len_data > MAX_REQUEST_DATA_SIZE){
		context->error_code = ILLEGAL_DATA_LENGTH;
		response_error(context);
		return FAIL;
	}

	if (len_buffer < len_token + 2 + UINT_SIZE + host_len_data) {
		return FAIL;
	} else if (len_buffer > len_token + 2 + UINT_SIZE + host_len_data) {
		context->error_code = TOO_MUCH_DATA;
		response_error(context);
		return FAIL;
	}
	context->request = (request_t *) malloc(sizeof(request_t));
	if (context->request == NULL) {
		context->error_code = MEMORY_ERROR;
		destroy_context_socket(context);
		return FAIL;
	}

	context->request->len_token = len_token;
	context->request->token = (char *) malloc(len_token * sizeof(char));
	if (context->request->token == NULL) {
		context->error_code = MEMORY_ERROR;
		destroy_context_socket(context);
		return FAIL;
	}

	memcpy(context->request->token, buffer + 1, len_token);
	context->request->fucntion_id = function_id;
	context->request->len_data = host_len_data;
	context->request->data = (char *) malloc(host_len_data * sizeof(char));
	if (context->request->data == NULL) {
		context->error_code = MEMORY_ERROR;
		destroy_context_socket(context);
		return FAIL;
	}
	memcpy(context->request->data, buffer + len_token + 2 + UINT_SIZE, host_len_data);

	evbuffer_drain(ev_buffer, len_buffer);

	return SUCCESS;
}

void destroy_request(request_t *request) {
	if (request == NULL)
		return;
	if (request->token != NULL)
		free(request->token);
	if (request->data != NULL)
		free(request->data);
	free(request);
}

void output_context(context_socket_t *context) {
	if (context == NULL)
		return;
	char buffer_token[MAX_TOKEN_SIZE + 1];
	char buffer_function[BUFF_SIZE];

	if (context->request != NULL && context->request->token != NULL) {
		memcpy(buffer_token, context->request->token,
				context->request->len_token);
		buffer_token[context->request->len_token] = '\0';
	} else {
		sprintf(buffer_token, "%s", "null");
	}

	if(context->request != NULL){
		sprintf(buffer_function, "%u", context->request->fucntion_id);
	}else{
		sprintf(buffer_function, "null");
	}

	zlog_info(handle,
			"ip:%s fd:%d token:%s function:%s error:%s\n",
			inet_ntoa(context->sin_client.sin_addr),
			context->fd_client,
			buffer_token,
			buffer_function,
			error_msg[context->error_code]
		);
}

context_socket_t *create_context_socket() {
	context_socket_t *context = (context_socket_t *) malloc(sizeof(context_socket_t));
	if (context == NULL) {
		return NULL;
	}
	context->context_global = NULL;
	context->bev_client = NULL;
	context->fd_client = -1;
	bzero(&(context->sin_client), sizeof(context->sin_client));
	context->request = NULL;
	context->response = NULL;
	context->error_code = EMPTY;
	return context;
}

void destroy_context_socket(context_socket_t *context) {
	if (context == NULL) {
		return;
	}

	output_context(context);

	if (context->bev_client != NULL) {
		bufferevent_free(context->bev_client);
		context->bev_client = NULL;
		if (context->context_global != NULL){
			--(context->context_global->socket_alive_number);
			context->context_global = NULL;
		}
	}
	context->fd_client = -1;
	bzero(&(context->sin_client), sizeof(context->sin_client));
	if (context->request != NULL) {
		destroy_request(context->request);
		context->request = NULL;
	}
	if (context->response != NULL) {
		destroy_response(context->response);
		context->response = NULL;
	}
	context->error_code = EMPTY;
	free(context);
}

int check_token(context_socket_t *context) {
	char token_str[MAX_TOKEN_SIZE + 1] = { 0 };
	memcpy(token_str, context->request->token, context->request->len_token);

	std::tr1::unordered_map<string, user_t>::iterator p =
			context->context_global->user_map.find(string(token_str));
	if (p != context->context_global->user_map.end()) {
		if (p->second.retry_num > 0){
			--(p->second.retry_num);
			return SUCCESS;
		}else{
			context->error_code = EXCEED_MAX_RETRY;
			response_error(context);
			return FAIL;
		}
	} else {
		context->error_code = ILLEGAL_TOKEN;
		response_error(context);
		return FAIL;
	}
}

void socket_read_callback(struct bufferevent *bev_client, void *arg) {
	context_socket_t *context = (context_socket_t*) (arg);

	if (recv_request(context) == FAIL) {
		return;
	}

	if (check_token(context) == FAIL) {
		return;
	}

	switch (context->request->fucntion_id) {
	case 0:
		context->response = rpc_strcat(context->request);
		break;
	case 1:
		context->response = rpc_insert(context->request);
		break;
	case 2:
		context->response = rpc_setstr(context->request);
		break;
	case 3:
		context->response = rpc_replace(context->request);
		break;
	case 4:
		context->response = rpc_delete(context->request);
		break;
	case 5:
		context->response = rpc_strcmp(context->request);
		break;
	case 6:
		context->response = rpc_readlog(context->request);
		break;
	case 7:
		context->response = rpc_test(context->request);
		break;
	default:
		break;
	}

	send_response(context);
}

void socket_write_callback(struct bufferevent *bev_client, void *arg) {
	context_socket_t *context = (context_socket_t*) (arg);
	if (context->response != NULL) {
		destroy_context_socket(context);
	}
}

void socket_event_callback(struct bufferevent *bev_client, short event,
		void *arg) {
	context_socket_t *context = (context_socket_t*) (arg);

	if (event & BEV_EVENT_TIMEOUT) {
		context->error_code = SOCKET_TIMEOUT;
	} else if (event & BEV_EVENT_EOF) {
		context->error_code = SOCKET_CLOSE;
	} else if (event & BEV_EVENT_ERROR) {
		context->error_code = SOCKET_ERROR;
	}
	destroy_context_socket(context);
}

void accpet_socket_callback(evutil_socket_t listener, short event, void *arg) {
	context_global_t * context_global = (context_global_t *) arg;
	struct sockaddr_in sin_client;
	socklen_t slen = sizeof(sin_client);
	int fd_client = accept(listener, (struct sockaddr *) &sin_client, &slen);
	if (fd_client < 0) {
		zlog_error(handle, "accept client fd error\n");
		return;
	}

	if (context_global->socket_alive_number > MAX_SOCKET_NUM) {
		zlog_error(handle, "accept to the max socket num: %d\n",
				context_global->socket_alive_number);
		close(fd_client);
		return;
	}

	++(context_global->socket_alive_number);

	context_socket_t *context_socket = create_context_socket();
	if (context_socket == NULL) {
		zlog_error(handle, "Create socket %d context error\n", fd_client);
		close(fd_client);
		return;
	}

	struct bufferevent *bev_client = bufferevent_socket_new(
			context_global->event_base, fd_client, BEV_OPT_CLOSE_ON_FREE);
	if (bev_client == NULL) {
		close(fd_client);
		zlog_error(handle, "Can't create new bufferevent for socket %d\n", fd_client);
		destroy_context_socket(context_socket);
		return;
	}
	context_socket->fd_client = fd_client;
	context_socket->sin_client = sin_client;
	context_socket->bev_client = bev_client;
	context_socket->context_global = context_global;

	struct timeval read_timeout = { SOCKET_TIMEOUT_SECOND, 0 };
	struct timeval write_timeout = { SOCKET_TIMEOUT_SECOND, 0 };
	bufferevent_set_timeouts(bev_client, &read_timeout, &write_timeout);

	bufferevent_setwatermark(bev_client, EV_READ, 0, MAX_REQUEST_SIZE);

	bufferevent_setcb(bev_client, socket_read_callback, socket_write_callback,
			socket_event_callback, context_socket);
	bufferevent_enable(bev_client, EV_READ | EV_WRITE | EV_PERSIST);

}

int ignore_sigpipe(void) {
	struct sigaction sa;
	memset(&sa, 0, sizeof(sa));
	sa.sa_handler = SIG_IGN;
	if (sigemptyset(&sa.sa_mask) < 0 || sigaction(SIGPIPE, &sa, NULL) < 0) {
		zlog_error(handle, "Could not ignore the SIGPIPE signal");
		return FAIL;
	}
	return SUCCESS;
}

int init_zlog(const char *conf_path, const char *category)
{
	if (zlog_init(conf_path) == 1)
	{
		perror("Cannot read the zlog configure file\n");
		zlog_fini();
		return FAIL;
	}
	handle = zlog_get_category(category);
	if (!handle)
	{
		perror("Cannot get category\n");
		zlog_fini();
		return FAIL;
	}
	return SUCCESS;
}

void end_zlog()
{
	zlog_fini();
}

int set_pid_file(const char * filepath)
{
	int fd;
	int tmp = 0;
	int pidsize = 0;
	char buf[BUFF_SIZE] ={ 0 };
	pid_t pid;
	pid = getpid();
	fd = open(filepath, O_RDWR | O_CREAT, 0644);
	if (fd < 0)
	{
		zlog_error(handle, "Open pid file error!!\n");
		return FAIL;
	}
	struct flock lock;
	lock.l_type = F_WRLCK;
	lock.l_start = 0;
	lock.l_whence = SEEK_SET;
	lock.l_len = 0;
	lock.l_pid = -1;
	fcntl(fd, F_GETLK, &lock);
	if (lock.l_type == F_WRLCK)
	{
		zlog_error(handle, "Pid file write lock already set by %d\n", lock.l_pid);
		close(fd);
		return FAIL;
	}

	lock.l_type = F_WRLCK;
	if ((fcntl(fd, F_SETLKW, &lock)) < 0)
	{
		zlog_error(handle, "Pid file lock failed:type=%d\n", lock.l_type);
		close(fd);
		return FAIL;
	}
	sprintf(buf, "%d\n", (int) pid);
	pidsize = strlen(buf);
	tmp = write(fd, buf, pidsize);
	if (tmp != (int) pidsize)
	{
		zlog_error(handle, "Write pid file lock failed\n");
		close(fd);
		return FAIL;
	}
	return SUCCESS;
}

context_global_t * create_context_global() {
	context_global_t * context = new (std::nothrow) context_global_t;
	if (context == NULL) {
		return NULL;
	}
	context->fd_listen = -1;
	context->event_base = NULL;
	context->socket_alive_number = 0;
	context->accept_event = NULL;
	return context;
}

void destroy_context_global(context_global_t *context) {
	if (context == NULL) {
		return;
	}
	if (context->fd_listen >= 0) {
		close(context->fd_listen);
		context->fd_listen = -1;
	}
	if (context->event_base != NULL) {
		event_base_free(context->event_base);
		context->event_base = NULL;
	}
	if (context->accept_event != NULL){
		event_free(context->accept_event);
		context->accept_event = NULL;
	}
	context->socket_alive_number = 0;
	delete (context);
}

int read_user_list(context_global_t * context_global) {
	ifstream fin(TOKEN_FILE);
	if (!fin.good()) return FAIL;
	string token;
	int retry_limit;
	user_t user;
	int count = 0;
	while(fin>>token>>retry_limit )
	{
		user.retry_num = retry_limit;
		context_global->user_map[token] = user;
		count++;
	}
	fin.close();
	zlog_info(handle, "Read %d token\n", count);
	return SUCCESS;
}

int write_user_list(context_global_t * context_global){
	ofstream fout(TOKEN_FILE_TMP);
	if (!fout.good()) return FAIL;
	std::tr1::unordered_map<string, user_t>::iterator p = context_global->user_map.begin();
	while (p != context_global->user_map.end()){
		fout<<(p->first)<<" "<<(p->second.retry_num)<<endl;
		p++;
	}
	fout.close();
	remove(TOKEN_FILE);
	rename( TOKEN_FILE_TMP,TOKEN_FILE);
	return SUCCESS;
}

void *data_durable_thread(void *arg){
	context_global_t * context_global = (context_global_t *)(arg);
	while (1){
		sleep(DURABLE_INTERVAL_SECOND);
		write_user_list(context_global);
	}
	return NULL;
}

int start_durable_thread(context_global_t * context_global)
{
	pthread_t thread;
	int ret = pthread_create(&thread, NULL, data_durable_thread, (void *) context_global);
	if (ret != SUCCESS){
		return FAIL;
	}
	return SUCCESS;
}

int listen_rpc_socket() {

	context_global_t *context_global = create_context_global();
	if (context_global == NULL){
		return FAIL;
	}

	if (read_user_list(context_global) == FAIL){
		zlog_error(handle, "Read user list file \"%s\" error\n", TOKEN_FILE);
		destroy_context_global(context_global);
		return FAIL;
	}

	if (start_durable_thread(context_global) == FAIL){
		zlog_error(handle, "Start durable thread error\n");
		destroy_context_global(context_global);
		return FAIL;
	}

	context_global->fd_listen = socket(AF_INET, SOCK_STREAM, 0);
	if (context_global->fd_listen < 0) {
		zlog_error(handle, "Create listen socket error\n");
		destroy_context_global(context_global);
		return FAIL;
	}

	evutil_make_listen_socket_reuseable(context_global->fd_listen);
	evutil_make_socket_nonblocking(context_global->fd_listen);

	struct sockaddr_in sin;
	sin.sin_family = AF_INET;
	sin.sin_addr.s_addr = INADDR_ANY;
	sin.sin_port = htons(PORT);

	if (bind(context_global->fd_listen, (struct sockaddr *) &sin, sizeof(sin))
			< 0) {
		zlog_error(handle, "Bind port:%u error.\n", PORT);
		destroy_context_global(context_global);
		return FAIL;
	}

	if (listen(context_global->fd_listen, LISTEN_BACKLOG) < 0) {
		zlog_error(handle, "Begin listen error\n");
		destroy_context_global(context_global);
		return FAIL;
	}

	context_global->event_base = event_base_new();
	if (context_global->event_base == NULL) {
		zlog_error(handle, "Create event base error\n");
		destroy_context_global(context_global);
		return FAIL;
	}

	context_global->accept_event = event_new(context_global->event_base,
			context_global->fd_listen,
			EV_READ | EV_PERSIST, accpet_socket_callback, context_global);

	if (context_global->accept_event == NULL) {
		zlog_error(handle, "Create accept event error\n");
		destroy_context_global(context_global);
		return FAIL;
	}

	if (event_add(context_global->accept_event, NULL) != SUCCESS) {
		zlog_error(handle, "Add accept event error\n");
		destroy_context_global(context_global);
		return FAIL;
	}

	zlog_info(handle, "Rpc Server start, listen to port %d\n", PORT);

	if (event_base_dispatch(context_global->event_base) != SUCCESS) {
		zlog_error(handle, "Event loop error\n");
		destroy_context_global(context_global);
		return FAIL;
	}

	zlog_info(handle, "Rpc Server end\n");
	destroy_context_global(context_global);
	return FAIL;
}

int main() {

	if (init_zlog(zlog_conf_file_path, zlog_category_name) == FAIL)
	{
		return FAIL;
	}

	if (set_pid_file(pid_file_path) == FAIL)
	{
		end_zlog();
		return FAIL;
	}

	if (ignore_sigpipe() == FAIL) {
		end_zlog();
		return FAIL;
	}

	if (listen_rpc_socket() == FAIL) {
		end_zlog();
		return FAIL;
	}

	return SUCCESS;
}
