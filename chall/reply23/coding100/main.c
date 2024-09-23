#include <stdio.h>
#include <stdlib.h>

char* grid = "f f c d d\n"
"f f c c h\n"
"g f a h h\n"
"g f a a b\n"
"g e e a b";

char* cmds = "a 16 *\n"
"b 2 -\n"
"c 13 +\n"
"d 1 -\n"
"e 3 -\n"
"f 48 *\n"
"g 12 +\n"
"h 5 +";

int main() {
    // FILE* f = fopen("lvl_1.txt", "r");
    printf("%s\n", cmds);

    return 0;
}
