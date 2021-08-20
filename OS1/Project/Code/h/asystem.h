#ifndef _system_h_
#define _system_h_

#include "thread.h"
#include "aconst.h"
#include "List.h"
#include "semaphor.h"
#include "schedule.h"

#define lock System::isLocked = 1;

#define unlock \
System::isLocked = 0;\
if (System::contextSwitchWanted) dispatch();

class PCB;
class KernelSem;
class IVTEntry;

void interrupt timer(...);

class System {
public:
	// Main thread
	static volatile Thread* mainThread;
	static Time mainPcbTimeSlice;

	// Trenutni PCB
	static volatile PCB* runningPcb;
	static Time runningPcbTimeSlice;

	// Idle thread
	static PCB* idleThreadPcb;
	static volatile bool isIdleRunning;

	// timer()-ove promenljive, kao na labu
	static bool contextSwitchWanted;
	static volatile bool isLocked;

	// Za semafore
	static volatile long long bootTimeDelta;

	// IVT tabela
	static IVTEntry *ivts[256];

	static void initialize();
	static void finalize();
	static void dispatch();

	// Globalne liste
	static List<PCB*> pcbs;
	static List<KernelSem*> semaphores;

private:
	friend interrupt void timer(...);
};

#endif
