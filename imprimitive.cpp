#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <gmpxx.h>

#include <bits/stdc++.h>

int main()
{
    // Create an input file stream object named 'file' and
    // open the file "GFG.txt".
    std::ifstream file("new_table.txt");

    std::ofstream output_file("divisors.txt");
    
    // String to store each line of the file.
    std::string line;
    
    std::vector< std::string > v;
    std::vector< mpz_class > v_nums;
    
    std::string temp_string;
    
    uint bad_line_counter = 0;
    uint found_comp = 0;
    

    
    if ( file.is_open()  )
    {
        // Read each line from the file and store it in the
        // 'line' variable.
        uint64_t count = 1;
        while( std::getline(file, line) )
        {
            std::stringstream ss(line);
            
            // line is space separated
            // so, v_nums[0] holds the carmichael number
            // v_nums[i] for i > 0 holds the prime divisors of v_nums[0]
            while (getline(ss, temp_string, ' '))
            {
                v.push_back(temp_string);
                v_nums.push_back( mpz_class(temp_string, 10) );
            }

            
            mpz_class divisor = 5717264681;
            
            if( 0 == v_nums[0] % divisor )
            {
                output_file << line << std::endl;
            }
            
            /*
            bool good_line = true;
            bool only_primes = true;
            
            mpz_class g;
            mpz_class l_n;
            
            mpz_class temp1 = v_nums[1]  - 1;
            mpz_class temp2 = v_nums[2]  - 1;
            
            mpz_gcd( g.get_mpz_t(), temp1.get_mpz_t(), temp2.get_mpz_t() );
            mpz_lcm( l_n.get_mpz_t(), temp1.get_mpz_t(), temp2.get_mpz_t() );
            
//            std::cout << v_nums[0] << " " << g << " " << l_n << std::endl;
            
            
            for( uint i = 3; i < v.size(); i++)
            {
                temp1 = v_nums[i] - 1;
                mpz_gcd( g.get_mpz_t(), g.get_mpz_t(), temp1.get_mpz_t() );
                mpz_lcm( l_n.get_mpz_t(), l_n.get_mpz_t(), temp1.get_mpz_t() );
             //   std::cout << v_nums[0] << " " << g << " " << l_n << std::endl;
            }

            
            if( g*g > l_n )
            {
                output_file << line << std::endl;
            }
            */

            v.clear();
            v_nums.clear();
        }

        output_file.close();
        file.close();
    }
    else
    {
        std::cerr << "Unable to open file!" << std::endl;
    }

    return 0;
}
