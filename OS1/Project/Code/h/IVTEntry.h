#ifndef _ivt_entry_h_
#define _ivt_entry_h_

#include "aconst.h"
#include "asystem.h"

typedef unsigned char IVTNo;

class KernelEv;

class IVTEntry {
public:
	IVTEntry(IVTNo ivtNo, interruptFunc interruptFunc);
	~IVTEntry();

	void runPreviousInterrupt();
	void signal();

private:
	friend class KernelEv;

	IVTNo myIvtNo;
	interruptFunc previousInterruptFunc;

	KernelEv *myEvent;
};

#endif
