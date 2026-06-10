#include <iostream>
#include <string>
int main() {
    std::string s = "{\"" + std::string("guid") + "\":\"" + std::string("val") + "\"}";
    std::cout << s << std::endl;
    return 0;
}

