#include <iostream>
#include <string>

using namespace std;

bool comapre_string(string a, string b)
{
    if (a.size() != b.size())
    {
        return false;
    }
    for (int i = 0; i < a.size(); i++)
    {
        if (a[i] != b[i])
        {
            return false;
        }
    }
    return true;
}

int main()
{
    string pass = "PING20241337";
    string input = "";
    cout << "Enter the password: ";
    cin >> input;
    if (comapre_string(pass, input))
    {
        cout << "Correct password" << endl;
    }
    else
    {
        cout << "Incorrect password" << endl;
    }  
    return 0;
 
}