#include "asystem.h"
#include "pcb.h"
#include "schedule.h"
#include "kernsem.h"
#include "idlethrd.h"

#include "iostream.h"
#include "dos.h"

// Main Thread
Time System::mainPcbTimeSlice = 2;
volatile Thread* System::mainThread;

// Trenutni PCB
volatile PCB* System::runningPcb = nullptr;
Time System::runningPcbTimeSlice = System::mainPcbTimeSlice;

// Idle Thread
volatile bool System::isIdleRunning = true;
PCB* System::idleThreadPcb = nullptr;

// IVT tabela
IVTEntry *System::ivts[256] = { nullptr };

// timer()-ove promenljive
bool System::contextSwitchWanted = false;
volatile bool System::isLocked = false;

// Za semafore
volatile long long System::bootTimeDelta = 0L;

// Globalne liste
List<PCB*> System::pcbs;
List<KernelSem*> System::semaphores;

interruptFunc oldInterrupt;

void tick();

void interrupt timer(...)
{
	if (!System::contextSwitchWanted) {
		// Timer je okinut, ali se ne trazi nasilno menjanje niti

		tick();

		for (Iterator<KernelSem*> it_ks = System::semaphores.iterStart();
				it_ks != System::semaphores.iterEnd(); it_ks++) {
			it_ks.data()->timerCleanup();
		}

		System::bootTimeDelta++;

		if (!System::runningPcb->unlimited) {
			System::runningPcbTimeSlice--;
		}
	}

	if ((System::runningPcbTimeSlice == 0 && !System::runningPcb->unlimited)
			|| System::contextSwitchWanted) {
		// Menja se kontekst, tj. prebacuje se rad na drugu nit
		// Zasto: Isteklo vreme trenutnoj niti i nije beskonacna (jer onda se ne menja dok ne zavrsi sama)
		//		  ||
		//        je jednostavno zahtevana promena konteksta nasilno

		if (System::isLocked) {
			// Sistem je zakljucan i nema nikakve promene niti, cak iako je zatrazena ili je doslo vreme
			// Ne moze se nista uraditi sem da se opet markira da se trazi promena konteksta i u sledecem okidanju
			// Opet mora da se stavi na true zato sto mozda nije bilo isto ovako eksplicitno zatrazeno, nego je mozda zbog isteka vremena

			System::contextSwitchWanted = true;
		} else {
			// Kontekst se menja na drugu nit. Prvo se snima progres postojece, i sledeca uzima iz rasporedjivaca
			System::runningPcb->SS = _SS;
			System::runningPcb->SP = _SP;
			System::runningPcb->BP = _BP;

			if (System::runningPcb->state != PCB::BLOCKED
					&& System::runningPcb->state != PCB::FINISHED
					&& System::runningPcb != System::idleThreadPcb) {
				// Nit nije blokirana niti je zavrsila
				// Markira se kao spremna i vraca u rasporedjivac za kasnije (ili odmah)
				System::runningPcb->state = PCB::READY;
				Scheduler::put((PCB*) System::runningPcb);
			}

			// Trazi se nova nit iz rasporedjivaca i postavlja kao tekuca
			x: System::runningPcb = Scheduler::get();
			if (System::runningPcb == nullptr) {
				/*lock;
				 cout << "stavljam idle" << endl;
				 unlock;*/
				System::runningPcb = System::idleThreadPcb;
			} else if (System::runningPcb->state == PCB::BLOCKED) {
				goto x;
			}

			/*lock;
			 cout << "novi running: " << System::runningPcb->id << endl;
			 unlock;*/

			System::runningPcb->state = PCB::RUNNING;
			_SP = System::runningPcb->SP;
			_SS = System::runningPcb->SS;
			_BP = System::runningPcb->BP;
			System::runningPcbTimeSlice = System::runningPcb->timeSlice;

			// Upravo je resen, stoga ide na false
			System::contextSwitchWanted = false;
		}
	}

	// Ako je ovo bilo redovno okidanje tajmera, moraju da se odrade rezijske default operacije
	if (!System::contextSwitchWanted) {
		oldInterrupt();
	}
}

void System::initialize() {
	asm cli;
	oldInterrupt = getvect(0x8);
	setvect(0x8, timer);

	idleThreadPcb = (new IdleThread())->myPCB;
	idleThreadPcb->start();

	mainThread = new Thread(65536, 1);
	mainThread->myPCB->state = PCB::RUNNING;

	// PRVOBITNA VERZIJA
	//mainPcb.SS = _SS;
	//mainPcb.SP = _SP;
	//mainPcb.BP = _BP;
	//mainPcb.state = PCB::RUNNING;

	runningPcb = mainThread->myPCB;

	asm sti;
}

void System::finalize() {
	if (System::runningPcb != System::mainThread->myPCB) {
		cout << "nisu isti" << endl;
		return;
	}

	for (Iterator<PCB*> it_pcbs = pcbs.iterStart(); it_pcbs != pcbs.iterEnd(); it_pcbs++) {
		delete it_pcbs.data();
	}

	// Vraca se stari interrupt
	asm cli;
	setvect(0x8, oldInterrupt);
	asm sti;
}

// Sinhrono menjanje niti
void System::dispatch() {
	asm cli;
	contextSwitchWanted = true;
	timer();
	asm sti;
}
