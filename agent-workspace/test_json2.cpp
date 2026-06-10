#include <stdio.h>
#include <string.h>

static char* _json_field(const char* json, const char* key) {
    static char buf[4096];
    size_t klen = strlen(key);
    const char* p = json;
    printf("Looking for key: %s (len=%zu)\n", key, klen);
    while(*p) {
        p = strchr(p, '"'); if(!p) { printf("No more quotes\n"); return NULL; } p++;
        printf("Found quote, p=%.5s\n", p);
        if(strncmp(p, key, klen) == 0 && p[klen] == '"') {
            printf("Matched key at %.5s\n", p);
            p += klen + 1; 
            printf("After key+1: p=%.5s\n", p);
            if(*p == '"') p++; 
            printf("After quote skip: p=%.5s\n", p);
            while(*p && (*p == '"' || *p == ' ' || *p == ':')) p++;
            printf("After ws skip: p=%.5s\n", p);
            if(*p != '"') { printf("Expected quote, got: %c (%d)\n", *p, (int)*p); return NULL; }
            p++;
            size_t i = 0;
            while(*p && *p != '"' && i < sizeof(buf)-1) { buf[i++] = *p; p++; }
            buf[i] = '\0'; 
            printf("Returning: %s\n", buf);
            return buf;
        } else {
            printf("No match: strncmp=%d p[klen]=%c\n", strncmp(p, key, klen), p[klen]);
        }
    }
    return NULL;
}

int main() {
    const char* json = "{\"cmd\":\"whoami\",\"seq\":\"1\"}";
    printf("json: %s\n", json);
    char* cmd = _json_field(json, "cmd");
    char* seq = _json_field(json, "seq");
    printf("cmd=%s seq=%s\n", cmd ? cmd : "(null)", seq ? seq : "(null)");
    return 0;
}
