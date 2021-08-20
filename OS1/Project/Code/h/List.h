#ifndef _list_h_
#define _list_h_

#include "aconst.h"

template<class T>
class ListNode {
public:
	ListNode(T val) :
			data(val) {
	}

	T data;
	ListNode<T> *next;
};

template<class T>
class Iterator {
public:
	// Inspiracija od BI_IListIter iz BC31\CLASSLIB ili kako se vec zove
	
	Iterator(ListNode<T> *myElem) :
			current(myElem) {
	}

	bool operator !=(const Iterator<T> & other) {
		return current != other.current;
	}

	bool operator ==(const Iterator<T> & other) {
		return !(*this != other);
	}

	Iterator<T> operator ++() {
		current = current->next;
		return *this;
	}

	Iterator<T> operator ++(int) {
		current = current->next;
		return *this;
	}

	ListNode<T> *current;

	// T & zvezda op ???
	T data() {
		return current->data;
	}
};

template<class T>
class List {
public:
	List() {
		startNode = endNode = nullptr;
	}

	~List() {
		removeAll();
	}

	Iterator<T> iterStart() const {
		return Iterator<T>(startNode);
	}

	const Iterator<T> iterEnd() const {
		return Iterator<T>(0);
	}

	T & front() {
		return startNode->data;
	}

	T & back() {
		return endNode->data;
	}

	bool empty() const {
		return i_size == 0;
	}

	unsigned size() const {
		return i_size;
	}

	// Metodi sa iteratorima
	Iterator<T> insert(Iterator<T> iter, const T& data);
	Iterator<T> remove(Iterator<T> pos);

	// Metodi za listu
	void addToFront(const T& data);
	void add(const T& data);

	void popFront();

	void remove(const T &data);
	void removeAll();

	ListNode<T> *startNode, *endNode;

protected:
	unsigned i_size;
};

template<class T>
void List<T>::removeAll() {
	ListNode<T> *elem = startNode;
	while (elem != nullptr) {
		startNode = elem;
		elem = elem->next;
		delete startNode;
	}

	startNode = endNode = nullptr;
	i_size = 0;
}

template<class T>
void List<T>::remove(const T &data) {
	Iterator<T> temp = iterStart(), next = iterStart();

	while (next != iterEnd()) {
		if (next.data() == data) {
			next = remove(temp);
		} else {
			next++;
			temp++;
		}
	}
}

template<class T>
Iterator<T> List<T>::insert(Iterator<T> iter, const T& data) {
	if (iter == iterEnd()) {
		return iterEnd();
	}

	ListNode<T>* temp = new ListNode<T>(data);
	temp->next = iter.current->next;

	iter.current->next = temp;

	if (iter.current == endNode) {
		endNode = temp;
	}

	i_size++; // Sad je umetnut

	return Iterator<T>(temp);
}

// Brise posle pos
template<class T>
Iterator<T> List<T>::remove(Iterator<T> pos) {
	if (pos == iterEnd()) {
		return iterEnd();
	}

	ListNode<T>* temp = pos.current->next;
	if (temp != nullptr) { // Posle krajnjeg nema nijednog
		i_size--;

		pos.current->next = temp->next;
		delete temp;
	}

	return Iterator<T>(pos.current->next);
}

template<class T>
void List<T>::addToFront(const T& data) {
	ListNode<T>* temp = new ListNode<T>(data);
	temp->next = startNode;

	if (empty()) {
		endNode = temp;
	}

	startNode = temp;
	i_size++;
}

template<class T>
void List<T>::add(const T& data) {
	ListNode<T>* temp = new ListNode<T>(data);
	temp->next = nullptr;

	if (empty())
		startNode = temp;
	else
		endNode->next = temp;

	endNode = temp;
	i_size++;
}

template<class T>
void List<T>::popFront() {
	if (!empty()) {
		ListNode<T>* popping = startNode;
		startNode = startNode->next;
		delete popping;
		i_size--;
	}
}

#endif
