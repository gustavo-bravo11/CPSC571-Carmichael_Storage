#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <gmpxx.h>

#include <bits/stdc++.h>

int main()
{
    // Create an input file stream object named 'file' and
    std::ifstream file("new_table.txt");
  
    // String to store each line of the file.
    std::string line;
    
    std::vector< std::string > v;
    std::vector< mpz_class > v_nums;
    
    std::string temp_string;
    
    
    mpz_class bound = 1000;
    uint64_t counter = 0;
    uint32_t i = 2;
    uint32_t  prime_count[20] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,};
    
    if ( file.is_open()  )
    {
        // Read each line from the file and store it in the
        // 'line' variable.
        uint64_t count = 1;
        while( std::getline(file, line) )
        {
            std::stringstream ss(line);
            while (getline(ss, temp_string, ' '))
            {
                v.push_back(temp_string);
                v_nums.push_back( mpz_class(temp_string, 10) );
            }
           
            
            while( bound < v_nums[0] )
            {
                i++;
                bound *= 10;

                for( uint16_t j = 4; j < 15; j++)
                {
                    std::cout << " $" << prime_count[ j ] << "$ & " ;
                }
                std::cout << " $" << prime_count[ 15 ] << "$ \\\\  \\hline " << std::endl;
            }
            
            counter++;
            prime_count[ v_nums.size() ]++;
            

            v.clear();
            v_nums.clear();
        }
        
        for( uint16_t j = 4; j < 15; j++)
        {
            std::cout << " $" << prime_count[ j ] << "$ & " ;
        }
        std::cout << " $" << prime_count[ 15 ] << "$ \\\\  \\hline " << std::endl;
        
        file.close();
    }
    
   
    
    else
    {
        std::cerr << "Unable to open file!" << std::endl;
    }

    return 0;
}
