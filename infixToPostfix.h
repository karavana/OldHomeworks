#ifndef _INFIX_TO_POSTFIX_H
#define _INFIX_TO_POSTFIX_H

#include <iostream>
#include <stack>
#include <string>
#include <algorithm>
#include "precedenceMap.h"

// helper, top element of an array w/o removing it
using namespace std;
string* pStr = new string[5000];
string ALPHABET = "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)";


static inline string unaryRange(string regex, int i){
	int rightParanthesisCount = 1;
	int leftParanthesisCount = 0;
	int j=i-2;
	
	string ranged = ")";
	while(rightParanthesisCount != leftParanthesisCount){
		if(regex[j] == '('){
			leftParanthesisCount++;
		}
		else if(regex[j] == ')'){
			rightParanthesisCount++;
		}
		ranged.insert(0, 1, regex[j]); //insert char at the beginning of the string
		j--;
	}
	return ranged;
}


static inline int handleBrackets(string &regex, int i)
{
	
	if(i==0){/*do nothing*/}
	else{
		if(precedenceMap(regex[i-1]) > 1 && precedenceMap(regex[i-1]) < 6){ //it is an operand, do nothing
			
		}
		else{
			if(regex[i-1] != '('){
				regex.insert(i, "&");
				i++;
			}
		}
	}
	int j=i+1;
	char from = 'x';
	char to = 'y';
	string toBeReplaced = "(";
	int bracketLength = 0;
	//if there is between character somewhere especially in j = i+2
	if(regex[j+1] == '-'){//TWO ALTERNATIVES [x-y] or [x-y0-9]
		if(regex[j+3] == ']'){ //ex:[x-y]
			from = regex[j];
			to = regex[j+2];
			for(unsigned int iter = from; iter<(unsigned int)to; iter++){
				toBeReplaced += iter;
				toBeReplaced += '|';
			}
			toBeReplaced += to;
			toBeReplaced += ')';
			cout << toBeReplaced << endl;
			regex.replace(j-1, 5, toBeReplaced);
			//cout << "REGEX NOW HERE IS : " << regex << endl;
		}
		else{ //ex:[x-y0-9]
			
		}
	}
	else{//put '|' between consecutively written characters
		int tempJ = j;
		while(regex[j] != ']'){
			toBeReplaced += regex[j];
			toBeReplaced += '|';
			j++;
			bracketLength++;
		}
		toBeReplaced.pop_back();
		toBeReplaced += ')';
		bracketLength += 2; //add '[' and ']' to the length to be replaced
		cout << "TOBEREPLACED: " << toBeReplaced << endl;
		cout << "bracket length: " << bracketLength << endl;
		regex.replace(tempJ-1, bracketLength, toBeReplaced);
	}	
		//cout << "After this operation regex become " << regex << " and...";
	return i;
	
}

static inline void replaceAllRemastered(string &regex){
	unsigned int i = 0;
	if(regex.length() == 1){
		if(precedenceMap(regex[i]) < 6)//its an operand or a paranthesis
		{
			regex = "INVALID";
			return;
		}
		if(regex[i] == '.')//any character
		{
			regex.erase(i, 1);
			regex.insert(i, ALPHABET);
		}
		
	}
	else{//length greater than 1
		while(i<regex.length()){
			int insertCount = 0;
			//****************************************DOT CHARACTER**************************************************//
			if(regex[i] == '.'){//any character
				if(i == 0){
					if (precedenceMap(regex[i+1]) > 1 && precedenceMap(regex[i+1]) < 6){ //it is an operand, do nothing

					}
					else{
						regex.insert(i+1, "&");
						insertCount++;
					}
				}
				else if(i == regex.length()-1){
					if(precedenceMap(regex[i-1]) > 1 && precedenceMap(regex[i-1]) < 6){ //it is an operand, do nothing

					}
					else{
						regex.insert(i-1, "&");
					}
				}
				else{
					//cout << "There is " << regex[i-1] << " before NOKTA and, " << regex[i+1] << " after NOKTA!" << endl;
					if(precedenceMap(regex[i-1]) > 1 && precedenceMap(regex[i-1]) < 6){ //it is an operand, do nothing
						//cout << "There is an operand or a parantez before NOKTA" << endl;
					}
					else{
						if(regex[i-1] != '('){
							regex.insert(i, "&");
							//cout << "There is no operand before NOKTA" << endl;
							//cout << "an & is inserted into " << i << " place and regex became: " << regex << endl;
							i++;
						}
					}
					if(precedenceMap(regex[i+1]) > 1 && precedenceMap(regex[i+1]) < 6){ //it is an operand, do nothing
						//cout << "There is an operand or a parantez after NOKTA" << endl;
					}
					else{
						if(regex[i+1] != ')'){
							regex.insert(i+1+insertCount, "&");
							insertCount++;
							//cout << "There is " << regex[i+1] << " after NOKTA" << endl;
							//cout << "There is no operand after NOKTA" << endl;
							//cout << "an & is inserted into " << i+1+insertCount << " place and regex became: " << regex << endl;
						}
					}
				}
				regex.erase(i, 1);
				regex.insert(i, ALPHABET);
				insertCount += ALPHABET.length()-1;
				//cout << "After this operation regex become " << regex << " and..." << endl;
			}
			//**************************************ADD '&' ASIDE PARENTHESIS IF NEEDED*****************************************//
			else if(regex[i] == '(' && i != 0){
				if(precedenceMap(regex[i-1]) > 1 && precedenceMap(regex[i-1]) < 6){ //it is an operand, do nothing
						
				}
				else{
					if(regex[i-1] != '(' && regex[i-1] != '['){
						regex.insert(i, "&");
						insertCount++;
					}
				}
				//cout << "After this operation regex become " << regex << " and..." << endl;
			}
			//**************************************ADD '&' ASIDE PARENTHESIS IF NEEDED*****************************************//
			else if(regex[i] == ')' && i != regex.length()-1){
				if(precedenceMap(regex[i+1]) > 1 && precedenceMap(regex[i+1]) < 6){ //it is an operand, do nothing
						
				}
				else{
					if(regex[i+1] != ')' && regex[i+1] != ']'){
						regex.insert(i+1, "&");
						insertCount++;
					}
				}
				//cout << "After this operation regex become " << regex << " and..." << endl;
			}
			//*************************************ADD '&' ASIDE KLEENE STAR IF NEEDED******************************************//
			else if(regex[i] == '*' && i != regex.length()-1){
				if(precedenceMap(regex[i+1]) > 1 && precedenceMap(regex[i+1]) < 6){ //it is an operand, do nothing

				}
				else{
					if(regex[i+1] != ')'){
						regex.insert(i+1, "&");
						insertCount++;
					}
				}
				//cout << "After this operation regex become " << regex << " and..." << endl;
			}
			//********************************ADD '&' ASIDE PLUS AND REPLACE IT WITH ITS EQUIVALENT****************************//
			else if(regex[i] == '+'){
				if(precedenceMap(regex[i+1]) > 1 && precedenceMap(regex[i+1]) < 6){ //it is an operand, do nothing

				}
				else{
					if(i!=regex.length()-1 && regex[i+1] !=')'){
						regex.insert(i+1, "&");
						insertCount++;
					}
				}
				if(regex[i-1] == ')'){ // +'s effect is on a set of characters bounded with parenthesis
					string ranged = unaryRange(regex, i);
					regex.erase(i,1); //delete + character
					string toBeInserted = "&";
					toBeInserted += ranged;
					toBeInserted += "*";
					//cout << "to be inserted regex :" << toBeInserted << endl;
					regex.insert(i, toBeInserted);
					insertCount += toBeInserted.length()-1;
					//cout << "ranged string: " << ranged << endl;
				}
				else{ // +'s effect is on a single character
					regex.erase(i, 1);
					string toBeInserted = "&";
					toBeInserted += regex[i-1];
					toBeInserted += "*";
					//cout << "to be inserted regex :" << toBeInserted << endl;
					regex.insert(i, toBeInserted);
					insertCount += toBeInserted.length()-1;
				}
				//cout << "After this operation regex become " << regex << " and..." << endl;
			}
			//******************************************************************************************************************//
			else if(regex[i] == '?'){
				//define one or more character case
				regex = "IS NOT DEFINED YET";
			}
			//******************************************************************************************************************//
			//not character ('^') inside the bracket is not handled yet
			//***************************ADD AND ASIDE BRACKETS AND REPLACE IT WITH ITS EQUIVALENT******************************//
			
			else if(regex[i] == '['){
				i = handleBrackets(regex,i);
			}

			else if(regex[i] == '\\'){
				if(regex[i+1] == 'a'){//ALPHABETIC
					regex.replace(i, 2, "[a-z]");
					i = handleBrackets(regex,i);
				}
				else if(regex[i+1] == 'd'){//DIGIT	
					regex.replace(i, 2, "[0-9]");
					i = handleBrackets(regex, i);
					
				}
				else if(regex[i+1] == 'w'){//WORD (ALPHANUMERIC)
					regex.replace(i, 2, "[0-9a-z]");
					i = handleBrackets(regex, i);
				}
				else if(regex[i+1] == 's'){//SPACE
					if(regex[i-1] != '&' && regex[i-1] != '(' && regex[i-1] != '['){
						regex.insert(i, "&");
						i++;
					}
					regex.replace(i, 2, " ");
					//need a function named handlePlus for code reusability
				}

				else{//USED AS ESCAPE CHARACTER
					if(regex[i-1] != '&' && regex[i-1] != '(' && regex[i-1] != '['){
						regex.insert(i, "&");
						i++;
					}
					regex.replace(i, 2, string(1,regex[i+1]));
				}
				cout << "After this operation regex become " << regex << " and..." << endl;
			}
			else if(regex[i] == '{'){//*********DO NOT LET M = 0 OR M>N************
				int j=i+1;
				string m = "";//m repetitions
				string n = "";//n repetitions
				bool isM = true;
				string toBeReplaced = "";
				int replacementLength = 2; // '{' and '}' characters are counted as 2
				while(regex[j] != '}'){
					if(regex[j] != ',' && isM){
						m += regex[j];
					}
					else{
						if(regex[j] == ','){isM = false;}
						else{n += regex[j];}//isM=false
					}
					j++;
					replacementLength++;
				}
				int M = atoi(m.c_str());
				if(!isM){//{m,n}
					int N = atoi(n.c_str());
					if(regex[i-1] == ')'){ // {m,n}'s effect is on a set of characters bounded with parenthesis
						string ranged = unaryRange(regex, i);
						replacementLength += ranged.length();
						for(int iter1=M; iter1<=N; iter1++){
							string tmpString = "";
							for(int iter2=0; iter2<iter1; iter2++){
								tmpString += ranged;
								if(iter2!=iter1-1){tmpString += '&';}
							}
							toBeReplaced += tmpString;
							if(iter1!=N){toBeReplaced += '|';}
						}
						regex.replace(i-ranged.length(), replacementLength, toBeReplaced);
						cout << "LENGTH OF THE STRING TO BE REPLACED: " << toBeReplaced.length() << endl;
						i = i+toBeReplaced.length()-3-ranged.length();//set index to the character before the last character ')'
					}
					else{ // {m,n}'s effect is on a single character
						replacementLength += 1;
						for(int iter=M; iter<=N; iter++){
							string tmpString = string(iter, regex[i-1]);
							if(iter!=N){tmpString += '|';} // add '|' until last repetition
							toBeReplaced += tmpString;
						}
						regex.replace(i-1, replacementLength, toBeReplaced);
						//cout << "LENGTH OF THE STRING TO BE REPLACED: " << toBeReplaced.length() << endl;
						i = i+toBeReplaced.length()-2;//set index to the last character of newly replaced string
					}
				}
				else{//{m}
					if(regex[i-1] == ')'){ // {m}'s effect is on a set of characters bounded with parenthesis
						string ranged = unaryRange(regex, i);
						replacementLength += ranged.length();
						for(int iter=0; iter<M; iter++){
							toBeReplaced += ranged;
							if(iter!=M-1){toBeReplaced += '&';}
						}
						regex.replace(i-ranged.length(), replacementLength, toBeReplaced);
						//cout << "LENGTH OF THE STRING TO BE REPLACED: " << toBeReplaced.length() << endl;
						i = i+toBeReplaced.length()-3-ranged.length();//set index to the character before the last character ')'
					}
					else{ // {m}'s effect is on a single character
						replacementLength += 1;
						toBeReplaced = string(M, regex[i-1]);
						regex.replace(i-1, replacementLength, toBeReplaced);
						//cout << "LENGTH OF THE STRING TO BE REPLACED: " << toBeReplaced.length() << endl;
						i = i+toBeReplaced.length()-2;//set index to the last character of newly replaced string
					}
				}
				//cout << "After this operation regex become " << regex << " and..." << endl;
			}
			//*************************** '[^abc]' = not a, b, nor c *************************************//

			i += insertCount+1;
			cout << "i became: " << i << ", and regex length became: " << regex.length() << endl;
		} 
	}





	cout << "regex become: " << regex << endl;
}


/***********Dijkstra's Shunting Yard Algorithm***********/
static inline string infixToPostfixRe(string reStr) {
  
  string output = "",term = "";
  stack<char> S;
  int length = reStr.length();
  
  int t=0;
  //


	for (int k=0;  k < length;  k++) {

	// current char
	char c = reStr[k];
	//cout<<"char " << c << endl;

	if (c == '('){
	  S.push(c);
	}

	else if (c == ')') {
		//cout<<"elseif";
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
		char topChar = S.top();

		int topCharPrecedence = precedenceMap(topChar);
		int currentCharPrecedence = precedenceMap(c);

		if (topCharPrecedence >= currentCharPrecedence) {
			//cout<<"ifte stack top "<<topChar<<endl;
			//cout<<"ifte current char "<<c<<endl;
			output += S.top();
			term += S.top();
			S.pop();
			if(topCharPrecedence == currentCharPrecedence)
				break;
			if(topCharPrecedence > currentCharPrecedence){
				pStr[t++] = term;
				term = "";
			}
		}

		else{
			if(term != "")
				pStr[t++] = term;
			//cout<<"elsete stack top "<<topChar<<endl;
			//cout<<"elsete current char "<<c<<endl;
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
  /*for (int i = 0; pStr[i] != ""; ++i)
  {
	 	 << i << " " <<pStr[i]<<endl;
  }*/

  

  return output;
}

#endif