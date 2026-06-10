#include <cstdio>
#include <cstring>

#define XOR_KEY 241
static unsigned char _e_path_upload_init[13] = {222,132,129,157,158,144,149,174,152,159,152,133,241};

static void s_copy(char* dst, unsigned char* src, size_t n) {
    for(size_t i=0;i<n;i++) dst[i] = src[i] ^ XOR_KEY;
    dst[n-1] = '\0';
}

int main() {
    char pui[64]; s_copy(pui, _e_path_upload_init, sizeof(_e_path_upload_init));
    printf("path='%s' len=%zu\n", pui, strlen(pui));
    return 0;
}
