#ifndef _idle_h_
#define _idle_h

#include "thread.h"

class IdleThread: public Thread {
public:
	IdleThread();

	virtual void run();
};

#endif
