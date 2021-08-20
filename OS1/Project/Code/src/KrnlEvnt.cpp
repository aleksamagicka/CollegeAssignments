#include "krnlevnt.h"

#include "pcb.h"
#include "asystem.h"

KernelEv::KernelEv(IVTNo ivtNo) :
		myIvtNo(ivtNo) {
	lock
	System::ivts[ivtNo]->myEvent = this;
	owner = (PCB*) System::runningPcb;
	unlock
}

KernelEv::~KernelEv() {
	lock
	System::ivts[myIvtNo]->myEvent = nullptr;
	unlock
}

void KernelEv::wait() {
	lock
	if (owner == System::runningPcb) {
		owner->state = PCB::BLOCKED;
		unlock

		dispatch();
	} else {
		unlock
	}
}

// Binarni semafor, pa se samo oslobadja blokade
void KernelEv::signal() {
	lock

	owner->state = PCB::READY;
	Scheduler::put(owner);

	unlock
}
