#ifndef _STACK_H
#define _STACK_H

#include <stdio.h>

template <class Object>
class StackNode
{
    public:
        StackNode(const Object& e = Object(), StackNode* n = NULL)
            : item(e), next(n) {}

        Object item;
        StackNode* next;
};




template <class T>
class Stack{
public:
   Stack();                     					// default constructor
   Stack(const Stack& rhs);  				// copy constructor
   ~Stack();                    					// destructor
   Stack& operator=(const Stack& rhs);  	// assignment operator
   bool isEmpty() const;
   void push(const T& newItem);
   void pop();
   void topAndPop(T& stackTop);
   void getTop(T& stackTop) const;
private:
   StackNode<T> *topPtr;                // pointer to the first node in the stack
};


template <class T>
Stack<T>::Stack() : topPtr(NULL) {}  	// default constructor

template <class T>
bool Stack<T>::isEmpty() const 
{
   return topPtr == NULL;
}


template <class T>
void Stack<T>::push(const T& newItem) 
{
   // create a new node
   StackNode<T> *newPtr = new StackNode<T>;

   newPtr->item = newItem; // insert the data

   newPtr->next = topPtr;     // link this node to the stack
   topPtr = newPtr;               // update the stack top
}


template <class T>
void Stack<T>::pop() 
{
   if (isEmpty())
      throw "StackException: stack empty on pop";
   else { 
      StackNode<T> *tmp = topPtr;
      topPtr = topPtr->next; // update the stack top
      delete tmp;
   }
}


template <class T>
void Stack<T>::topAndPop(T& stackTop) 
{
   if (isEmpty())
      throw "StackException: stack empty on  topAndPop";
   else { 
      stackTop = topPtr->item;
      StackNode<T> *tmp = topPtr;
      topPtr = topPtr->next; // update the stack top
      delete tmp;
   }
}


template <class T>
void Stack<T>::getTop(T& stackTop) const  
{
   if (isEmpty())
      throw "StackException: stack empty on getTop";
   else
      stackTop = topPtr->item;
}


template <class T>
Stack<T>::~Stack() 
{
   // pop until stack is empty
   while (!isEmpty())
       pop();
}


template <class T>
Stack<T>& Stack<T>::operator=(const Stack& rhs) 
{
    if (this != &rhs) {
        if (!rhs.topPtr)
            topPtr = NULL;
        else {
            topPtr = new StackNode<T>;
            topPtr->item = rhs.topPtr->item;
            StackNode<T>* q = rhs.topPtr->next;
            StackNode<T>* p = topPtr;
            while (q) {
                p->next = new StackNode<T>;
                p->next->item = q->item;
                p = p->next; 
                q = q->next;
            }
            p->next = NULL;
        }
    }
    return *this;
} 

template <class T>
Stack<T>::Stack(const Stack& rhs) 
{
    *this = rhs; // reuse assignment operator
} 




#endif