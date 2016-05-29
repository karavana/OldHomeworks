#include <iostream>
#include <stack>
#include <string>
#include <algorithm>
#include "BST.h"



// helper, top element of an array w/o removing it
using namespace std;
string* pStr = new string[50];



int precedenceMap(char c)
{
	switch(c){
	  case '(': return 1;
	  case '|': return 2; // alternate
	  case '&': return 3; // concatenate

	  case '?': // zero or one
	  case '+': 
	  case '*': return 4; // one or more

	  case '^': return 5; // complement
	  default: return 6;  
	}
  // else 6

};



static inline void ReplaceAll(string &str, const string& from, const string& to)
{
	size_t start_pos = 0;
	string copy_from = from;
	string copy_to = to;
	string and_string = "&";
	bool flag = false;
	if(from == "."){
		while((start_pos = str.find(from, start_pos)) != std::string::npos) {
			if(6 == precedenceMap(str[start_pos+1])){
				copy_to.append(and_string);
				cout<<"to string "<<copy_to<<endl;
				flag = true;
			}
			if(6 == precedenceMap(str[start_pos-1])){
				if(flag){
					flag =false;
					and_string.append(copy_to);
				}
				else
					and_string.append(to);
				cout<<"to string "<<and_string<<endl;
			}
			if(flag){
				flag = false;
				str.replace(start_pos, from.length(), copy_to);
			}
			else{
				str.replace(start_pos, from.length(), and_string);   
			}
			start_pos += copy_to.length(); // Handles case where 'to' is a substring of 'from'    

			
		}
	}
	
	else if(from == "*"){
		while((start_pos = str.find(from, start_pos)) != std::string::npos) {
			if(start_pos != 0){ //if the kleene star is not at the start of the string already
				if(str[start_pos-1] == ")"){ //check if the previous string is right parenthesis
					int i = start_pos-1;
					int j = 1; //amount of right parenthesis
					while(str[start_pos-j] == ")"){ //go ALA you see right parenthesis and inc j
						j++;
					}
					while(str[i] != "(" || j != 0){ //go till you see the last left parenthesis
						if(str[i] == "("){ // if its left parenthesis, dec right parenthesis count
							j--;
						}
						else{
							i--;		//else start_pos pointer points to one left of the current position on the string
						}
					}
					str.insert(i,from); //put kleene star where the last left parenthesis stands
										//pushes the remaining string to right
					
				}
				else if(precedenceMap(str[start_pos-1]) == 6){ // there is already a term and no parenthesis
					str.insert(start_pos-1,from); //insert * there
					
				}
				
			}
			
			else{
				break; // do nothing since kleene star is at the beginning of the string
			}
			
		}
		
	}
}






string infixToPostfixRe(string reStr) {
  
  string output = "",term = "";
  stack<char> S;
  int length = reStr.length();
  
  int t=0;
  //


	for (int k=0;  k < length;  k++) {

	// current char
	char c = reStr[k];
	cout<<"char " << c << endl;

	if (c == '('){
	  S.push(c);
	}

	else if (c == ')') {
		cout<<"elseif";
		while (S.top() != '(') {
			output += S.top();

			if(precedenceMap(S.top())<6){
				pStr[t++] = term;
				term = "";
			}

			term += S.top();
			S.pop();
		}
		pStr[t++] = term;
		term = "";
		S.pop(); // pop '('
	}

	// else work with the stack
	else {
		while (S.size()) {
		char peekedChar = S.top();

		int peekedCharPrecedence = precedenceMap(peekedChar);
		int currentCharPrecedence = precedenceMap(c);

		if (peekedCharPrecedence >= currentCharPrecedence) {
			cout<<"ifte stack top "<<peekedChar<<endl;
			cout<<"ifte current char "<<c<<endl;
			output += S.top();
			term += S.top();
			S.pop();
			if(peekedCharPrecedence == currentCharPrecedence)
				break;
			if(peekedCharPrecedence > currentCharPrecedence){
				pStr[t++] = term;
				term = "";
			}
		}

		else{
			if(term != "")
				pStr[t++] = term;
			cout<<"elsete stack top "<<peekedChar<<endl;
			cout<<"elsete current char "<<c<<endl;
			term = "";
			break;
		}
	  }
	  S.push(c);
	}

	} // end for loop

  while (S.size()){
	output += (S.top());
	if(precedenceMap(S.top()) == 6){
		term += S.top();
	}
	else{
		pStr[t++] = S.top();
	}
	if(term != ""){
		pStr[t++] = term;
		term = "";
	}
	S.pop();
  }


  cout<< reStr<< " => " << output << " "<< endl;
  for (int i = 0; pStr[i] != ""; ++i)
  {
	 cout << i << " " <<pStr[i]<<endl;
  }

  

  return output;

}


// tests

int main(){
	string ascii = "*(a|b|c)";
	string org_regex = "(bill|will).ozgur";
	string copy_regex = org_regex;


	ReplaceAll(copy_regex,".",ascii);
	infixToPostfixRe(copy_regex); 


	int i = 0;
	stack< BinaryNode<string>* > S;
	while(pStr[i] != "")
	{
		string current = pStr[i];
		cout << i << ": " << current << endl; 

		if(S.size() == 0)	{
			cout << "a" << endl;
			BinaryNode<string> *newbst = new BinaryNode<string>( current, nullptr, nullptr );   //create new node pointer
			S.push(newbst);                         //stack empty, push it
		}
		else if(precedenceMap(current[0]) == 6 ){      //character occurred
			cout << "b" << endl;
			BinaryNode<string> *newbst = new BinaryNode<string>( current, nullptr, nullptr );   //create new node pointer
			S.push(newbst);

		}
		else if (precedenceMap(current[0]) == 4 )   {
			cout << "c" << endl;
			cout << S.top() ->right ->element << endl;

			cout << S.top() ->left ->element << endl;	
		    deleteNode(S.top());		// Sadece freelemek için yapılabilir. Poplamak construct etmek için yeterli
		    S.pop();
		    S.push(nullptr);
		    cout << "SIZE: " << S.size() << endl;
		}
		else if(precedenceMap(current[0]) != 6 ){      //its an operand
			cout << "d" << endl;
			BinaryNode<string> *newbst = new BinaryNode<string>( current,nullptr, S.top()); //create new node pointer
			if (S.top())	cout << "1" <<S.top()->element << endl;
			S.pop();
			newbst->left = S.top();                 //below top is the left child
			if (S.top()) cout << "2" <<S.top()->element << endl;
			S.pop();
			S.push(newbst);
			if (i==2 || i==11)cout << S.top()-> element << S.top()->right-> element << S.top() ->left ->element << endl;
		}
		i++;

	}
/*
	cout << S.top() ->element << endl;
	S.pop();
	cout << S.top() ->right -> element << endl;
	S.pop();
*/

	while(S.size() > 1){                            //postfix regex over, if stack left
		cout << "a"<< endl;
		BinaryNode<string> *newbst = new BinaryNode<string>("&",nullptr, S.top()); //create new node pointer
		S.pop();
		newbst->left = S.top();                 //below top is the left child
		S.pop();                            //top of the stack is right child
		S.push(newbst);                         //push the new tree to the stack
	}


	printTree(S.top());
   
	deleteNode(S.top());


	/*
	infixToPostfixRe("a.b|c"); // ab.c|
	infixToPostfixRe("a.b+.c"); // ab+.c.
	infixToPostfixRe("a.(b.b)+.c"); // abb.+.c.
	*/
	return 0;
}