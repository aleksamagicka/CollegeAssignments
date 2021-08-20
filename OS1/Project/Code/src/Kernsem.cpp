#include "kernsem.h"

#include "asystem.h"

KernelSem::KernelSem(int init, Semaphore *initSemph) :
		count(init), semph(initSemph) {
	System::semaphores.add(this);
}

KernelSem::~KernelSem() {
	while (count < 0)
		signal();
}

int KernelSem::val() const {
	return count;
}

int KernelSem::wait(Time maxTimeToWait) {
	lock
	if (count-- > 0) {
		unlock
		return 1;
	}

	System::runningPcb->state = PCB::BLOCKED;
	if (maxTimeToWait == 0) {
		// Cisto blokiranje do nekog signal()-a
		blockedThreads.add((PCB*) System::runningPcb);
	} else {
		// Vremensko blokiranje, novi SemaphoredThread se ubacuje na pravo mesto u nizu tako da poredak vremena budjenja ostane rastuci

		SemaphoredThread st = SemaphoredThread((PCB*) System::runningPcb,
				System::bootTimeDelta + maxTimeToWait);

		if (timeBlocked.empty()) {
			// Nema sta da se pretrazuje
			timeBlocked.add(st);
		} else {
			Iterator<SemaphoredThread> t = timeBlocked.iterStart(), rightPlace = timeBlocked.iterEnd();
			while (t != timeBlocked.iterEnd()
					&& st.futureWakeupTime < t.current->data.futureWakeupTime) {
				rightPlace = t;
				t++;
			}

			if (rightPlace != timeBlocked.iterEnd()) {
				// Nadjena je vrednost posle koje treba ubaciti ovu novu
				timeBlocked.insert(rightPlace, st);
			} else {
				// rightPlace je ostao kraj niza, znaci da nema onog elementa POSLE koga bi ovo trebalo ubaciti
				// To znaci da su svi VECI od ovog novog, i on onda ide pre svih njih
				timeBlocked.addToFront(st);
			}
		}
	}

	unlock
	dispatch();

	// Mozda je isteklo vreme?
	if (!System::runningPcb->semphTimeExceeded) {
		System::runningPcb->semphTimeExceeded = false;
		return 0;
	}

	return 1;
}

void KernelSem::releaseBlocked() {
	PCB *pcb = blockedThreads.front();
	blockedThreads.popFront();

	pcb->state = PCB::READY;
	pcb->semphTimeExceeded = true; //?

	Scheduler::put(pcb);
}

void KernelSem::releaseTimed() {
	PCB *pcb = timeBlocked.front().myPCB;
	timeBlocked.popFront();

	pcb->state = PCB::READY;
	pcb->semphTimeExceeded = true;

	Scheduler::put(pcb);
}

void KernelSem::signal() {
	lock

	if (count++ < 0) {
		if (!blockedThreads.empty()) {
			releaseBlocked();
		} else if (!timeBlocked.empty()) {
			releaseTimed();
		}
	}

	unlock
}

void KernelSem::timerCleanup() {
	lock

	while (!timeBlocked.empty()) {
		if (timeBlocked.front().futureWakeupTime > System::bootTimeDelta)
			break;

		PCB *pcb = timeBlocked.front().myPCB;
		timeBlocked.popFront();

		pcb->state = PCB::READY;
		pcb->semphTimeExceeded = false;

		Scheduler::put(pcb);
	}

	unlock
}
