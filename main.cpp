#include "infixToPostfix.h"
#include "generateTree.h"


// tests

int main(){
	//string ascii = "(a|b|c)";
	string org_regex ;
	//string org_regex = "bill|will";
	//string org_regex = "bill&will";
	//string org_regex = "bill*will";
	//string org_regex = "(bill|will)&Clinton";
	//string org_regex = "(bill|will)|Clinton";
	
	cout << "Enter a regex: " << endl;
	cin >> org_regex;

	string copy_regex = org_regex;

	replaceAllRemastered(copy_regex);

	cout << "COPY_REGEX IS: " << copy_regex << endl;

	copy_regex = infixToPostfixRe(copy_regex); 

	cout << "COPY_REGEX IS: " << copy_regex << endl;

	physical_access_plan();

	//result();
	
	return 0;
}
