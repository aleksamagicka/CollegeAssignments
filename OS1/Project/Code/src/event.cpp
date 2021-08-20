#include "event.h"
#include "KrnlEvnt.h"

// Samo prosledjuje KernelEvent-u pozive

Event::Event(IVTNo ivtNo) {
	lock
	myImpl = new KernelEv(ivtNo);
	unlock
}

Event::~Event() {
	lock
	delete myImpl;
	unlock
}

void Event::wait() {
	myImpl->wait();
}

void Event::signal() {
	myImpl->signal();
}
