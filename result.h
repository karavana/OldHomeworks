#ifndef _RESULT_H
#define _RESULT_H

#include "generateTree.h"
#include <cstring>

void inline result()
{

	char temp[500];

	//string pos[10]={"bill","william","|","clinton A","&"};

	FILE* in;

	string terms[100];

	unsigned int i,j,k;

	k=0;i=0;

	string pos[100];

	for (i=0; i<postOrderedList.size(); i++)
		pos[i]=postOrderedList[i];

	int len = postOrderedList.size();
	i=0;
	while (pos[i] != "")  {

		if (pos[i] == "&" && pos[i+1] != "")  {
			terms[k] = pos[i-2] + " " + pos[i-1];
			k++;
		}

		else  if (pos[i+3] != "" && pos[i+2] == "&"  )  {
			;
		}

		else  if (pos[i+2] != "" && pos[i+1] == "&"  )  {
			;
		}
		
		else    {
			terms[k] = pos[i];
			k++;
		}
		i++;
	}

	cout << "TERMS:" << endl; 
	for (i=0; terms[i] != ""; i++)
		cout << i << " " << terms[i] << endl;

	string queries[100];

	i=0;j=0;
	if (len>3)	{
		while (terms[i] != "")    {
			if (terms[i] == "|" )     {
				i++;
				continue;
			}

			if (terms[i+2] != "" && terms[i+2] == "|")    {
				queries[j] = terms[i] + " " + terms[i+3];
				j++;
				if (terms[i+4] != "" && (terms[i+4] != "&" && terms[i+4] != "|"))   {
					queries[j] = terms[i] + " " + terms[i+4];
					j++;
				}

			}

			else if (terms[i+1] != "" && terms[i+1] == "|")    {
				queries[j] = terms[i] + " " + terms[i+2];
				j++;
				if (terms[i+3] != "" && (terms[i+3] != "&" && terms[i+4] != "|"))   {
					queries[j] = terms[i] + " " + terms[i+3];
					j++;
				}

			}  

			else if (terms[i] == "&")     {
				;
			}

			i++;
		}
	}

	if (len<=3)
		for (i=0; i<3; i++)
			queries[i]=terms[i];	

	for (k=0; queries[k]!=""; k++)      {
		cout << "QUERY: "  << queries[k] << endl;

		cout << "RESULTS:" << endl;

		string query = '"' + queries[k] + '"';
		string res = "grep -rn --color='always' " + query + " test/";

		char * grep = new char [res.length()+1];
		strcpy (grep, res.c_str());

		if (!(in = popen(grep, "r")))   {
			cout << "ERROR" << endl;
		}   

		while(fgets(temp, sizeof(temp), in)!=NULL){
			cout << temp << endl;
		}
		cout << endl;
	}

	pclose(in);


}

#endif