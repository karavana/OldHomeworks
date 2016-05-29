#ifndef _PRECEDENCE_MAP_H
#define _PRECEDENCE_MAP_H

int precedenceMap(char c)
{
	switch(c){
	  case '(': return 1;
	  case '|': return 2; // alternate
	  case '&': return 3; // concatenate

	  case '?': return 4;// zero or one
	  case '*': return 4; // zero or more
	  case '+': return 4; // one or more
	  case '{': return 4; // {m,n} m to n repetitions
	  case '^': return 5; // complement
	  default: return 6;  
	}
  // else 6

};

#endif