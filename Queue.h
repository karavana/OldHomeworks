#ifndef _QUEUE_H
#define _QUEUE_H

//most of the parts are adopted from the data structures lecture slides, added some extra features and will be added more..

template <class Object> 
class QueueNode
{
    public:
        QueueNode(const Object& e = Object(), QueueNode* n = NULL)
            : item(e), next(n) {}

        Object item;
        QueueNode* next;
};

template <class T>
class Queue {
public:
	Queue();                     	// default constructor
  Queue(const Queue& rhs);       	// copy constructor
  ~Queue();                   	// destructor
  Queue& operator=(const Queue & rhs); //assignment operator

	bool isEmpty() const;	// Determines whether the queue is empty
 	void enqueue(const T& newItem);  // Inserts an item at the back of a queue
	void dequeue() throw();   // Dequeues the front of a queue
 	 	// Retrieves and deletes the front of a queue.
	void dequeue(T& queueFront) throw();
 		// Retrieves the item at the front of a queue.
	void getFront(T& queueFront) const throw();
private:
	QueueNode<T> *backPtr;
   QueueNode<T> *frontPtr;
};

template<class T>
Queue<T>::Queue() : backPtr(NULL), frontPtr(NULL){}  // default constructor

template<class T>
Queue<T>::~Queue() {       // destructor
   while (!isEmpty())
      dequeue();   // backPtr and frontPtr are NULL at this point
}

template<class T>
bool Queue<T>::isEmpty() const{  
   return backPtr == NULL;
}

template<class T>
void Queue<T>::enqueue(const T& newItem) {  
    // create a new node
    QueueNode<T> *newPtr = new QueueNode<T>;

        // set data portion of new node
    newPtr->item = newItem;
    newPtr->next = NULL;

    // insert the new node
        if (isEmpty())    // insertion into empty queue
           frontPtr = newPtr;
    else      // insertion into nonempty queue
           backPtr->next = newPtr;

    backPtr = newPtr;   // new node is at back
}

template<class T>
void Queue<T>::dequeue() throw() {
   if (isEmpty())
    throw "QueueException: empty queue, cannot dequeue";
   else {   // queue is not empty; remove front
      QueueNode<T> *tempPtr = frontPtr;
      if (frontPtr == backPtr) {    // one node in queue
         frontPtr = NULL;
         backPtr = NULL;
      }
      else
         frontPtr = frontPtr->next;

      tempPtr->next = NULL;   // defensive strategy
      delete tempPtr;
    }
}

template<class T>
void Queue<T>::dequeue(T& queueFront) throw() {
   if (isEmpty())
      throw "QueueException: empty queue, cannot dequeue";
   else {   // queue is not empty; retrieve front
      queueFront = frontPtr->item;
      dequeue();  // delete front
   }
}
template<class T>
void Queue<T>::getFront(T& queueFront) const throw() {
   if (isEmpty())
      throw "QueueException: empty queue, cannot getFront";
   else   // queue is not empty; retrieve front
      queueFront = frontPtr->item;
} 

#endif