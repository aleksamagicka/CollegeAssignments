#include "semaphor.h"

#include "kernsem.h"
#include "asystem.h"

// Semaphore samo delegira KernelSem-u pozive

Semaphore::Semaphore(int init) {
	myImpl = new KernelSem(init, this);
}

Semaphore::~Semaphore() {
	lock
	//System::semaphores.remove(myImpl);
	//delete myImpl;
	unlock
}

int Semaphore::wait(Time maxTimeToWait) {
	return myImpl->wait(maxTimeToWait);
}

void Semaphore::signal() {
	myImpl->signal();
}

int Semaphore::val() const {
	return myImpl->val();
}
