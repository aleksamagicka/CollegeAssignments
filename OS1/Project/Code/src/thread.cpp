#include "thread.h"

#include "pcb.h"
#include "asystem.h"
#include "iostream.h"

Thread::Thread(StackSize stackSize, Time timeSlice) {
	myPCB = new PCB(stackSize, timeSlice, this);
}

void dispatch() {
	System::dispatch();
}

void Thread::start() {
	myPCB->start();
}

void Thread::waitToComplete() {
	myPCB->waitToComplete();
}

Thread::~Thread() {
	waitToComplete();
	delete myPCB;
}

ID Thread::getId() {
	return myPCB->getId();
}

ID Thread::getRunningId() {
	return ((PCB*) System::runningPcb)->getId();
}

Thread * Thread::getThreadById(ID id) {
	lock

	Thread* requestedThread = nullptr;

	for (Iterator<PCB*> it_pcb = System::pcbs.iterStart(); it_pcb != System::pcbs.iterEnd(); it_pcb++) {
		PCB* currentPcb = it_pcb.data();
		if (currentPcb->id == id) {
			requestedThread = currentPcb->thread;
			break;
		}
	}

	unlock
	return requestedThread;
}
