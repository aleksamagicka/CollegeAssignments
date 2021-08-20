#include "dos.h"
#include "schedule.h"
#include "pcb.h"
#include "iostream.h"
#include "asystem.h"

// Globalni ID PCB-ova krece od 0
ID PCB::latestID = 0;

PCB::PCB(StackSize stackSize, Time timeSlice, Thread *thread) {
	this->stackSize = stackSize;
	this->timeSlice = timeSlice;
	this->thread = thread;

	this->state = PCB::NEW;
	this->id = latestID++;
	this->unlimited = timeSlice == 0;

	lock

	// Stvaranje steka, adaptirano sa laba
	stackSize = stackSize / sizeof(unsigned);
	stackPointer = new unsigned[stackSize];
	stackPointer[stackSize - 1] = 0x200; // Setovan I fleg u pocetnom PSW-u za nit
	stackPointer[stackSize - 2] = FP_SEG(PCB::wrapper);
	stackPointer[stackSize - 3] = FP_OFF(PCB::wrapper);

	SS = FP_SEG(stackPointer + stackSize - 12);
	SP = BP = FP_OFF(stackPointer + stackSize - 12);

	// Dodaje se u globalnu listu ovde
	System::pcbs.add(this);

	unlock
}

PCB::~PCB() {
	lock
	if (this->stackPointer)
		delete[] stackPointer;

	System::pcbs.remove(this);
	unlock
}

void PCB::start() {
	lock

	if (state == PCB::NEW) {
		state = PCB::READY;
		Scheduler::put(this);
	}

	unlock
}

void PCB::waitToComplete() {
	lock

	if (state != FINISHED) { //  && this->id != System::runningPcb->id
		System::runningPcb->state = PCB::BLOCKED;
		waitedPcbs.add((PCB*) System::runningPcb);

		unlock
		System::dispatch();
		return;
	}

	unlock
}

ID PCB::getId() const {
	return id;
}

void PCB::wrapper() {
	System::runningPcb->thread->run();

	lock

	System::runningPcb->state = PCB::FINISHED;

	for (Iterator<PCB*> it =
			((PCB*) System::runningPcb)->waitedPcbs.iterStart();
			it != ((PCB*) System::runningPcb)->waitedPcbs.iterEnd(); it++) {

		it.data()->state = PCB::READY;
		Scheduler::put(it.data());

		System::runningPcb->waitedPcbs.remove((PCB*)it.data());
	}

	unlock

	System::dispatch();
}
