#include <stdio.h>
#include <stdlib.h>
#include <x86intrin.h>

int main() { 
    unsigned int rdtsc = __rdtsc();
    unsigned int seed = (rdtsc << 7) ^ (rdtsc >> 5) ^ rdtsc;

    srandom(seed);

    int data[16];
    int hidden[16];

    for (int i = 0; i < 16; i++) {
        data[i] = rand() & 1;
        printf("%d", data[i]);
    }
    puts("\n");

    for (int i = 0; i < 16; i++) {
        hidden[i] = rand() & 1;
        printf("%d", hidden[i]);
    }
    puts("\n");

    rdtsc = __rdtsc();
    seed = (rdtsc << 7) ^ (rdtsc >> 5) ^ rdtsc;

    srandom(seed);
    
    int idx = 0;
    int found[16];

    for (int i = 0; i < 16; i++) {
        found[i] = rand() & 1;
    }

    int search = 0;
    for (int i = 0; i< 16; i++) {
        if (data[i] == found[i]) {
            sear
        }
    }

    while(idx < 16) {
        int new = rand() & 1;
    }

    for (int i = 0; i < 16; i++) {
        printf("%d", found[i]);
    }

    for (int i = 0; i < 16; i++) {
        printf("%d", rand() & 1);
    }
    puts("\n");
}
