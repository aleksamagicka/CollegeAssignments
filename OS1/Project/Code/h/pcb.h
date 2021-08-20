#ifndef _pcb_h_
#define _pcb_h_

#include "List.h"
#include "thread.h"

class PCB
{
public:
	enum State { READY = 0, RUNNING = 1, BLOCKED = 3, FINISHED = 4, NEW = 5 };

	PCB(StackSize stackSize, Time timeSlice, Thread *thread);
	~PCB();

	// Metodi iz Thread
	void start();
	void waitToComplete();
	ID getId() const;

	static void wrapper();

private:
	friend void interrupt timer(...);
	friend class Thread;
	friend class KernelEv;
	friend class System;
	friend class KernelSem;

	ID id;
	Thread *thread;
	State state;

	// Gde se nalazi
	unsigned *stackPointer;
	unsigned SS;
	unsigned SP;
	unsigned BP;

	static ID latestID;
	StackSize stackSize;

	bool semphTimeExceeded;

	bool unlimited;
	Time timeSlice;

	// Liste
	List<PCB*> waitedPcbs;
};

#endif
