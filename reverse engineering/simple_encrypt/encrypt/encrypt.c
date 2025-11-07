#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

int main(void)
{
    int rand_num1;
    time_t time_seed;
    unsigned int int_time_seed;
    unsigned int rand_num2;
    long file_index;
    FILE* original_file;
    size_t file_length;
    void* encrypted_content;
    FILE* encrypted_file;
    int unix_timestamp = 1658225688;
    original_file = fopen("flag", "rb");

    // get file length
    fseek(original_file, 0, 2);
    file_length = ftell(original_file);
    fseek(original_file, 0, 0);


    encrypted_content = malloc(file_length);
    fread(encrypted_content, file_length, 1, original_file);
    fclose(original_file);
    time_seed = time((time_t*)0x0);
    int_time_seed = (unsigned int)time_seed;
    srand(int_time_seed);

    for (file_index = 0; file_index < (long)file_length; file_index++) {
        rand_num1 = rand();

        *(unsigned char *)((long)encrypted_content + file_index) = 
            *(unsigned char *)((long)encrypted_content + file_index) ^ (unsigned char )rand_num1;

        rand_num2 = rand();

        rand_num2 = rand_num2 & 7;
        *(unsigned char *)((long)encrypted_content + file_index) =
            *(unsigned char *)((long)encrypted_content + file_index) << (char)rand_num2 |
            *(unsigned char *)((long)encrypted_content + file_index) >> 8 - (char)rand_num2;
    }
    
    encrypted_file = fopen("flag.enc", "wb");
    fwrite(&int_time_seed, 1, 4, encrypted_file);
    fwrite(encrypted_content, 1, file_length, encrypted_file);
    fclose(encrypted_file);
    return 0;
}