#include "IVTEntry.h"
#include "krnlevnt.h"
#include "dos.h"

IVTEntry::IVTEntry(IVTNo ivtNo, interruptFunc interruptFunc) :
		myIvtNo(ivtNo), myEvent(nullptr) {
	lock
	previousInterruptFunc = getvect(ivtNo);
	setvect(ivtNo, interruptFunc);
	System::ivts[ivtNo] = this;
	unlock
}

IVTEntry::~IVTEntry() {
	lock
	setvect(myIvtNo, previousInterruptFunc);
	System::ivts[myIvtNo] = nullptr;
	unlock
}

void IVTEntry::runPreviousInterrupt() {
	previousInterruptFunc();
}

// Ovo su prakticno binarni semafori
void IVTEntry::signal() {
	if (myEvent != nullptr) {
		myEvent->signal();
	}
}
