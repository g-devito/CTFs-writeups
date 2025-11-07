#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

int main(void)
{
    int rand_num1;
    unsigned int int_time_seed;
    unsigned int rand_num2;
    long file_index;
    FILE* encrypted_file;
    size_t file_length;
    void* decrypted_content;
    FILE* decrypted_file;
    encrypted_file = fopen("flag.enc", "rb");

    fread(&int_time_seed, 1, 4, encrypted_file);

    fseek(encrypted_file, 0, SEEK_END);
    file_length = ftell(encrypted_file) - 4;

    fseek(encrypted_file, 4, SEEK_SET);
    decrypted_content = malloc(file_length);
    fread(decrypted_content, 1, file_length, encrypted_file);

    srand(int_time_seed);

    for (file_index = 0; file_index < (long)file_length; file_index++) {
        rand_num1 = rand();
        rand_num2 = rand() & 7;

        *(unsigned char *)((long)decrypted_content + file_index) =            
            *(unsigned char *)((long)decrypted_content + file_index) >> (char)rand_num2 |
            *(unsigned char *)((long)decrypted_content + file_index) << 8 - (char)rand_num2;
        
        *(unsigned char *)((long)decrypted_content + file_index) = 
            *(unsigned char *)((long)decrypted_content + file_index) ^ (unsigned char )rand_num1;
    }
    
    decrypted_file = fopen("flag", "wb");
    fwrite(decrypted_content, 1, file_length, decrypted_file);
    fclose(decrypted_file);
    return 0;
}