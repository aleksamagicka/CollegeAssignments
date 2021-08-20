#ifndef _event_h_
#define _event_h_

#include "asystem.h"
#include "IVTEntry.h"

typedef unsigned char IVTNo;

class KernelEv;

class Event {
public:
	Event(IVTNo ivtNo);

	~Event();

	void wait();

protected:
	friend class KernelEv;

	void signal(); // can call KernelEv

private:
	KernelEv * myImpl;
};

#define PREPAREENTRY(ivtNo, shouldRunPreviousInterruptFunc) \
void interrupt gInterrupt_##ivtNo(...); \
IVTEntry gIvtEntry##ivtNo(ivtNo, gInterrupt_##ivtNo); \
void interrupt gInterrupt_##ivtNo(...) { \
    gIvtEntry##ivtNo.signal(); \
    if (shouldRunPreviousInterruptFunc) { \
    	gIvtEntry##ivtNo.runPreviousInterrupt(); \
    } \
}

#endif
