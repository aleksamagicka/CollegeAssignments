#ifndef _kernel_event_h_
#define _kernel_event_h_

#include "aconst.h"
#include "event.h"

class PCB;

class KernelEv {
public:
    KernelEv(IVTNo ivtNo);
    ~KernelEv();

    void wait();
    void signal();

private:
    IVTNo myIvtNo;
    PCB *owner;
};

#endif
