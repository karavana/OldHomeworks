#include <iostream>
#include <stack>
#include <queue>
#include <string>
#include <vector>
#include <algorithm>
#include <fstream>
#include "precedenceMap.h"
#include "BinaryTree.h"

vector<string> postOrderedList;
vector<string> preOrderedList;
string queryString = "";


BinaryNode<string>* logical_access_plan();
void inline static physicalAccessPlan();
void inline treeToString(BinaryNode<string>* testTree);

using namespace std;

BinaryNode<string>*  logical_access_plan()
{
	int i = 0;
	stack< BinaryNode<string>* > S;

	
	while(pStr[i] != "")
	{
		string current = pStr[i];
		//cout << i << ": " << current << endl; 

		if(S.size() == 0){
			BinaryNode<string> *newbt = new BinaryNode<string>( current, nullptr, nullptr );   //create new node pointer
			S.push(newbt);                         //stack empty, push it
		}
		else if(precedenceMap(current[0]) == 6 ){      //it is a character
			BinaryNode<string> *newbt = new BinaryNode<string>( current, nullptr, nullptr );   //create new node pointer
			S.push(newbt);

		}
		else if (precedenceMap(current[0]) == 4 )   {	//it is a kleene star
			BinaryNode<string> *newbt = new BinaryNode<string>( current, S.top(), nullptr );   //create new node pointer
		    //deleteNode(S.top());		// Sadece freelemek için yapılabilir. Poplamak construct etmek için yeterli
			//printTree(S.top());
			S.pop();
			//BinaryNode<string> *nullNode = new BinaryNode<string>( nullptr, nullptr, nullptr);
		    //S.push(newbt);
		    S.push(nullptr);
		    //cout << "SIZE: " << S.size() << endl;
		}
		else if(precedenceMap(current[0]) != 6 ){      //its an operand or a paranthesis
			BinaryNode<string> *newbt = new BinaryNode<string>( current,nullptr, S.top()); //create new node pointer
			S.pop();
			newbt->left = S.top();                 //below top is the left child
			S.pop();
			//cout << "current operand: " << current[0] << endl;
			//cout << "Left tree is...." << endl;
			//printTree(newbt->left);
			//cout << "Right tree is...." << endl;
			//printTree(newbt->right);
			if(current == "&"){
				if(newbt->left == nullptr){
					if(newbt->right == nullptr){
						S.push(nullptr);
					}
					else{//right child is a regular expression tree
						S.push(newbt->right);
					}
				}
				else{//left child is a regular expression tree
					if(newbt->right == nullptr){
						S.push(newbt->left);
					}
					else{//right child is a regular expression tree
						S.push(newbt);
					}
				}
			}
			else if(current == "|"){
				if(newbt->left == nullptr){
					S.push(nullptr);
				}
				else{//left child is a regular expression tree
					if(newbt->right == nullptr){
						S.push(nullptr);
					}
					else{//right child is a regular expression tree
						S.push(newbt);
					}
				}
			}
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
		BinaryNode<string> *newbt = new BinaryNode<string>("&",nullptr, S.top()); //create new node pointer
		S.pop();
		newbt->left = S.top();                 //below top is the left child
		S.pop();                            //top of the stack is right child
		S.push(newbt);                         //push the new tree to the stack
	}

	return S.top();
}

void inline static physical_access_plan()
{
	stack< BinaryNode<string>* > S;
	S.push(logical_access_plan());
	int j;
	
	/*cout << "post order printing of tree..." << endl;
	postorder(S.top());
	cout << "print tree..." << endl;
	cout << nodeCount(S.top()) << endl;
	cout << "..."<<endl;*/
	cout << "***RESULTANT LOGICAL TREE***" << endl;
	printTree(S.top());
	//POSTORDER AND PREORDER FORMS OF RESULTANT TREE ARE STORED IN FOLLOWING VECTORS
	postorderList(S.top(), postOrderedList);
	for(unsigned int i=0; i<postOrderedList.size(); i++){
		cout << postOrderedList[i] << ", ";
	}
	cout << endl;
	preorderList(S.top(), preOrderedList);
	/*for(unsigned int i=0; i<preOrderedList.size(); i++){
		cout << preOrderedList[i] << ", ";
	}
	cout << endl;*/
   	
	deleteNode(S.top());


	//FILE* usefulGramFile;
	//usefulGramFile = fopen("freq.txt","r");
	
	ifstream usefulGramFile("freq.txt");
	cout <<"okundu"<<endl;
	stack< BinaryNode<string>* > physicalAccessPlan;
	string currentGram;	// gram from useful terms file. the file and index will include same grams
	string currentSubstring;
	queue< string > currentTermUsefulGrams;	
	bool usefulFlag; //usefulgram found, set it to true
	
	int gramFound; //counter to keep track of gram count found

	for (j=0; j < postOrderedList.size(); j++)	{
		gramFound=0;		//grams for new term, have to reset the counter of grams
		usefulFlag=false;	//
		if (postOrderedList[j] != "|" && postOrderedList[j] != "&")	{
			cout<<"its a term, generating grams"<<endl;
			if (postOrderedList[j].length() <= 10 )		{
				for (int k=3; k <= postOrderedList[j].length() ; k++)	{	// from length of the term to 3 

					for (int l=0; l+k <= postOrderedList[j].length(); l++ )	{	// for substrings
						
						currentSubstring= postOrderedList[j].substr(l,k);	// from lth index of the term to (l+k)th 
						cout<<"currentsubstr "<<currentSubstring<<endl;
						//fseek (usefulGramFile, 0, SEEK_SET);		//start reading file from the beginning
						ifstream usefulGramFile("freq.txt");
						while (usefulGramFile >> currentGram) 	{
					
							if (currentSubstring == currentGram)	{	//gram found in the index
								gramFound++;
								currentTermUsefulGrams.push(currentSubstring);
								cout<<"a gram found! pushed to stack"<<endl;
								/*if (currentGram == postOrderedList[j])	{// term itself is a useful gram
									// set a flag to control generation of grams because no more grams are needed. Original term is useful gram. We dont need smaller pieces!!! 
									// Also, smaller pieces violate presuf-free rule
									usefulFlag=true;
								}*/
								break; //gram already found, no need to search further for another match
							}
						}
						
						if (gramFound == 2){
							currentTermUsefulGrams.push("AND"); //two terms need to be AND'ed
							gramFound--; //after having found 2 grams, gotta put AND after each and every gram
						}
						
					}
				}
				
				if (!gramFound) {		// vector boşsa useful gram yok. nullptr push
					cout<<"couldnt find any grams, pushing null"<<endl;
					currentTermUsefulGrams.push("NULL");
					
				}
			}

			else {		// >10 olanlar. Üstteki if için geçerli olan her yorum bunda da geçerli
				for (int k=3; k <= 10; k--)	{	
					for (int l=0; l+k <= postOrderedList[j].length(); l++)	{
						currentSubstring = postOrderedList[j].substr(l,k);

						while (usefulGramFile >> currentGram)	{
							if (currentSubstring == currentGram)	{
								gramFound++;
								
								ifstream usefulGramFile("freq.txt");
								currentTermUsefulGrams.push(currentSubstring);

								if (gramFound == 2){
									currentTermUsefulGrams.push("AND"); //two terms need to be AND'ed
									gramFound--; //after having found 2 grams, gotta put AND after each and every gram
								}

								

								// <=10 için burada olan if burası için geçerli değil. 

							}
						}
					}
				}

				if (!gramFound)	{
					currentTermUsefulGrams.push("NULL");
				}
			} 
		}
		else	{		// to add operands to currentTermUsefulGrams vector
			if (postOrderedList[j] == "|")
				currentTermUsefulGrams.push("OR");
			else if (postOrderedList[j] == "&")
				currentTermUsefulGrams.push("AND");
		}

	   } //end of the term usefulness check
	
	/*while(!currentTermUsefulGrams.empty()){ //to print what the currentTermUsefulGrams has
		cout << currentTermUsefulGrams.front() << ", ";
		currentTermUsefulGrams.pop();
		cout << endl;
	}*/
	
	while(!currentTermUsefulGrams.empty()){
		if(currentTermUsefulGrams.front() == "NULL"){
				physicalAccessPlan.push(nullptr);
				currentTermUsefulGrams.pop();
				cout<<"null, bulunamamis gram"<<endl;
		}
		else if(physicalAccessPlan.size() == 0){
			
			BinaryNode<string> *newbt = new BinaryNode<string>( currentTermUsefulGrams.front(), nullptr, nullptr );   //create new node pointer
			physicalAccessPlan.push(newbt);                         //stack empty, push it
			currentTermUsefulGrams.pop();
			cout<<"first item"<<endl;
			printTree(physicalAccessPlan.top());
		}
		else if(currentTermUsefulGrams.front() != "AND" && currentTermUsefulGrams.front() != "OR"){
			BinaryNode<string> *newbt = new BinaryNode<string>( currentTermUsefulGrams.front(), nullptr, nullptr );   //create new node pointer
			physicalAccessPlan.push(newbt);                         //there is a term, push it
			currentTermUsefulGrams.pop();
			cout<<"term"<<endl;
			printTree(physicalAccessPlan.top());
		}
		else{
			
			BinaryNode<string> *newbt = new BinaryNode<string>( currentTermUsefulGrams.front(),nullptr, physicalAccessPlan.top()); //create new node pointer
			cout<<"ilk pop geliyore"<<endl;
			physicalAccessPlan.pop();
			newbt->left = physicalAccessPlan.top();                 //below top is the left child
			cout<<"ikinci pop geliyore"<<endl;
			physicalAccessPlan.pop();
			cout << "current operand: " << newbt->element << endl;
			cout << "Left tree is...." << endl;
			printTree(newbt->left);
			cout << "Right tree is...." << endl;
			printTree(newbt->right);
			if(currentTermUsefulGrams.front() == "AND"){
				if(newbt->left == nullptr){
					if(newbt->right == nullptr){
						physicalAccessPlan.push(nullptr);
					}
					else{//right child is a not null tree
						physicalAccessPlan.push(newbt->right);
					}
				}
				else{//left child is a not null tree
					if(newbt->right == nullptr){
						physicalAccessPlan.push(newbt->left);
					}
					else{//right child is a not null tree
						physicalAccessPlan.push(newbt);
					}
				}
				
			}
			else if(currentTermUsefulGrams.front() == "OR"){
				if(newbt->left == nullptr){
					physicalAccessPlan.push(nullptr);
				}
				else{//left child is a regular expression tree
					if(newbt->right == nullptr){
						physicalAccessPlan.push(nullptr);
					}
					else{//right child is a regular expression tree
						physicalAccessPlan.push(newbt);
						cout<<"pushed something"<<endl;
					}
				}
				
			}
			currentTermUsefulGrams.pop();
		}
	}
	
	while(physicalAccessPlan.size() > 1){                            //terms are over, if stack left
		cout<<"stack left"<<endl;
		BinaryNode<string> *newbt = new BinaryNode<string>("AND",nullptr, physicalAccessPlan.top()); //create new node pointer
		physicalAccessPlan.pop();
		newbt->left = physicalAccessPlan.top();                 //below top is the left child
		physicalAccessPlan.pop();                            //top of the stack is right child
		physicalAccessPlan.push(newbt);                         //push the new tree to the stack
	}
	cout<< "final physicalAccessPlan"<<endl;
	printTree(physicalAccessPlan.top());
	string a = "";
	treeToString(physicalAccessPlan.top()); //to get the lucene query as inorder
	cout<<queryString<<endl;
	
}



void inline treeToString(BinaryNode<string>* testTree)
{
	if(testTree)
	{
		if(testTree->left || testTree->right)
			queryString = queryString + "(";
		treeToString(testTree->left);
		queryString = queryString + testTree->element + " ";
		treeToString(testTree->right);
		if(testTree->left || testTree->right)
			queryString = queryString + ")";
	}
	
}