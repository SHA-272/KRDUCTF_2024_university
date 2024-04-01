#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define AES_BLOCK_SIZE 16

void encrypt_block(unsigned char *block, unsigned char *key)
{
    for (int i = 0; i < AES_BLOCK_SIZE; i++)
    {
        block[i] ^= key[i] + i;
    }
}

void encrypt(unsigned char *input, int input_len, unsigned char *key)
{
    int num_blocks = input_len / AES_BLOCK_SIZE;
    for (int i = 0; i < num_blocks; i++)
    {
        encrypt_block(input + (i * AES_BLOCK_SIZE), key);
    }
}

void print_ascii_art()
{
    printf("  _  __           ____\n");
    printf(" | |/ /___ _   _ / ___| ___ _ __\n");
    printf(" | ' // _ \\ | | | |  _ / _ \\ '_ \\\n");
    printf(" | . \\  __/ |_| | |_| |  __/ | | |\n");
    printf(" |_|\\_\\___|\\__, |\\____|\\___|_| |_|\n");
    printf("           |___/\n");
    printf("\n");
}

int main()
{
    unsigned char key[] = "issupersecretkey";
    unsigned char plaintext[256];

    print_ascii_art();
    printf("Welcome to Key Generation Program\n\n");

    int choice;
    do
    {
        printf("Main Menu:\n");
        printf("1. KeyGen\n");
        printf("2. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        getchar();

        switch (choice)
        {
        case 1:
            printf("\nEnter phrase: ");
            fgets((char *)plaintext, sizeof(plaintext), stdin);

            int len = strlen((char *)plaintext);
            int padded_len = len + (AES_BLOCK_SIZE - (len % AES_BLOCK_SIZE));

            unsigned char *ciphertext = malloc(padded_len);
            if (ciphertext == NULL)
            {
                fprintf(stderr, "Memory error\n");
                return 1;
            }

            memcpy(ciphertext, plaintext, len);
            memset(ciphertext + len, 0, padded_len - len);

            encrypt(ciphertext, padded_len, key);

            printf("Your key: ");
            for (int i = 0; i < padded_len; i++)
            {
                printf("%02x", ciphertext[i]);
            }
            printf("\n\n");

            free(ciphertext);
            break;
        case 2:
            printf("Exiting program...\n");
            break;
        default:
            printf("Invalid choice. Please try again.\n");
            break;
        }
    } while (choice != 2);

    return 0;
}
