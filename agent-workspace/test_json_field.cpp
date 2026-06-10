#include <cstdio>
#include <cstring>
#include <string>

static char* _json_field(const char* json, const char* key) {
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
    while(start < j.length() && j[start] != (char)34 && i < sizeof(buf)-1) { buf[i++] = j[start++]; }
    buf[i] = 0; return buf;
}

int main() {
    const char* json1 = "{\"offset\":0,\"status\":\"ok\"}\n";
    const char* json2 = "{\"cmd\":\"whoami\",\"seq\":\"1\"}\n";
    printf("status=%s\n", _json_field(json1, "status") ? _json_field(json1, "status") : "(null)");
    printf("cmd=%s\n", _json_field(json2, "cmd") ? _json_field(json2, "cmd") : "(null)");
    printf("seq=%s\n", _json_field(json2, "seq") ? _json_field(json2, "seq") : "(null)");
    return 0;
}
