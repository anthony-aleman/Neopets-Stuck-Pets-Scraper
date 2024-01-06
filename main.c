#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>


bool very_well_named(int len, char* token) {
    if (!isupper(token[0]) 
        && !isalpha(token[0])) {
        return false;
    }

    
    //printf("running loop\n");
    for (int i = 0; i < len; i++)
    {

        //printf("%c\n", token[i]);
        if (!isdigit(token[i]) )
        {
            //printf("Not very well named: %s\n", token);
            return false;
        }
        
    }

    if (len < 0 || len > 8)
    {
        return false;
    }
    
    
    return true;
}

bool well_named(int len, char* token) {

    if (!isupper(token[0]) 
        && !isalpha(token[0])) {
        return false;
    }


    for (int i = 1; i < len; i++)
    {
        //printf("%c\n", token[i]);
        if (isdigit(token[i]) || token[i] == '_' || !isalpha(token[i]) || isupper(token[i]))
        {
            //printf("Not well named: %c\n", token[i]);
            return false;
        }
        
    }
    return len <= 9;
}

bool matches_criteria(char * token) {
    // Does the token match the criteria?

    /*
    // Naming conventions

    // 1. VWN: Xxxxxxxx - 8 continguous characters or less
    // 2. WN: Xxxxxxxxx, xxxxxx, XXXXXX, 9 contigious characters or more 
    */

    // Find the length of the token
    int len = strlen(token);

    // check if VWN
    if(very_well_named(len, token)) {
        printf("VWN: \n");
        return true;
    }

    //Check if WN
    if(well_named(len, token)) {
        printf("WN: \n");
        return true;
    }

    return false;
}



void read_csv(const char * filename) {
    FILE * fp = fopen(filename, "r");


    if (fp == NULL) {
        printf("Could not open file %s", filename);
        return;
    } else {
        printf("Opened file %s\n", filename);
        char line[1024];
        while (fgets(line, 1024, fp)) {
            char * token = strtok(line, ",");

            //Skip the first token
            if (token != NULL)
            {
                token = strtok(NULL, ",");
            }
            
            if (token != NULL && matches_criteria(token)) {
                // Does the token match the criteria?
                printf(" %s\n", token);
            }

            strtok(NULL, ","); // Skip column 3
            strtok(NULL, ","); // skip column 4
        }
    }

    fclose(fp);
}

int main(int argc, // Num of strings in array argv
         char* argv[], // Array holding the command line argument strings
         char ** envp // array of environment variable strings
         ) {
    printf("Hello, World!\n");

    int count;
    // Display each command line argument
    printf_s("\nCommand Line arguments: \n");
    for (count = 0; count < argc; ++count) {
        printf_s("argv[%d]  %s\n", count, argv[count]);
    }
    if (argc > 1)
    {
        //read the csv file
        read_csv(argv[1]);
    } else {
        printf_s("No arguments passed.\n");
    }

    //Display environment variables
    /*while(*envp != NULL)
        printf_s("%s\n", *(envp++));
    */
    return 0;
}
