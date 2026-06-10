#include <stdio.h>
#include <string.h>

static char* _json_field(const char* json, const char* key) {
    static char buf[4096];
    size_t klen = strlen(key);
    const char* p = json;
    while(*p) {
        p = strchr(p, '"'); if(!p) return NULL; p++;
        if(strncmp(p, key, klen) == 0 && p[klen] == '"') {
            p += klen + 1; 
            if(*p == '"') p++; 
            while(*p && (*p == ' ' || *p == ':')) p++;
            if(*p != '"') return NULL; 
            p++;
            size_t i = 0;
            while(*p && *p != '"' && i < sizeof(buf)-1) { buf[i++] = *p; p++; }
            buf[i] = '\0'; return buf;
        }
    }
    return NULL;
}

int main() {
    const char* json = "{\"cmd\":\"whoami\",\"seq\":\"1\"}";
    printf("json: %s\n", json);
    char* cmd = _json_field(json, "cmd");
    printf("cmd=%s\n", cmd ? cmd : "(null)");
    char* seq = _json_field(json, "seq");
    printf("seq=%s\n", seq ? seq : "(null)");
    return 0;
}
