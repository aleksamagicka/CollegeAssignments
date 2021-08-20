#include "TrieStablo.h"
#include "Pomocno.h"

#include <queue>
#include <string>
#include <locale>

TrieStablo::TrieCvor::TrieCvor(TrieCvor* roditelj)
	: m_roditelj(roditelj),
	  m_brojPodstabala(0)
{
	for (int i = 0; i < 255; i++)
		m_niz_pokazivaca[i] = nullptr;
}

TrieStablo::TrieCvor::~TrieCvor()
{
	for (auto& i : m_niz_pokazivaca)
		delete i;
}

TrieStablo::TrieCvor* TrieStablo::TrieCvor::pronadjiPodstablo(char deoKljuca)
{
	return m_niz_pokazivaca[deoKljuca];
}

void TrieStablo::TrieCvor::dodajPodstablo(char deoKljuca, TrieCvor* cvor)
{
	if (!m_niz_pokazivaca[deoKljuca])
	{
		m_niz_pokazivaca[deoKljuca] = cvor;
		m_brojPodstabala++;
	}
}

void TrieStablo::TrieCvor::ukloniPodstablo(char deoKljuca)
{
	if (m_niz_pokazivaca[deoKljuca])
	{
		m_niz_pokazivaca[deoKljuca] = nullptr;
		m_brojPodstabala--;
	}
}

void TrieStablo::TrieCvor::postaviInfo(int broj)
{
	m_info = broj;
}

int TrieStablo::TrieCvor::dohvatiInfo()
{
	return this == nullptr ? -1 : m_info;
}

void TrieStablo::TrieCvor::poseti(ostream& it, int maxNivo = -1, int nivo = 0)
{
	if (maxNivo != -1 && nivo > maxNivo)
		return;

	if (m_info)
		it << dohvatiKljuc() << " (" << dohvatiInfo() << ")" << endl;

	for (int i = 0; i < 255; i++)
		if (m_niz_pokazivaca[i])
			m_niz_pokazivaca[i]->poseti(it, maxNivo, nivo + 1);
}

//---------------------------------------------------------------


TrieStablo::TrieCvor* TrieStablo::pronadjiCvor(const char* kljuc, stack<TrieCvor*>* stack = nullptr)
{
	if (!m_koren)
		return nullptr;

	TrieCvor* tek = m_koren;

	for (int i = 0; i < strlen(kljuc) && tek; i++)
	{
		tek = tek->pronadjiPodstablo(kljuc[i]);
		if (!tek)
			continue;

		if (stack != nullptr)
			stack->push(tek);
	}

	return tek;
}

TrieStablo::TrieStablo()
	: m_koren(nullptr)
{
}

TrieStablo::~TrieStablo()
{
	delete m_koren;
}

bool TrieStablo::umetni(const char* kljuc)
{
	if (string(kljuc).empty())
		return false;

	if (!m_koren)
	{
		m_koren = new TrieCvor(nullptr);
		m_brCvorova++;
	}

	TrieCvor* tek = m_koren;
	TrieCvor* sledeci = nullptr;

	for (int i = 0; i < strlen(kljuc); i++)
	{
		sledeci = tek->pronadjiPodstablo(kljuc[i]);

		if (!sledeci)
		{
			sledeci = new TrieCvor(tek);
			tek->dodajPodstablo(kljuc[i], sledeci);
			m_brCvorova++;
		}

		tek = sledeci;
	}

	bool prvoUmetanje = true; // ako je kljuc prvi put umetnut, onda true
	if (sledeci->dohvatiInfo())
		prvoUmetanje = false;
	else
		m_brKljuceva++;

	if (prvoUmetanje)
	{
		sledeci->postaviInfo(1);
	}
	else
	{
		const int novi = sledeci->dohvatiInfo() + 1;
		sledeci->postaviInfo(novi);
	}

	sledeci->postaviKljuc(kljuc);

	return prvoUmetanje;
}

string TrieStablo::TrieCvor::dohvatiKljuc()
{
	return kljuc;
}

void TrieStablo::TrieCvor::postaviKljuc(const char* kljuc1)
{
	kljuc = string(kljuc1);
}

bool TrieStablo::obrisi(const char* kljuc)
{
	if (!m_koren)
		return false;

	TrieCvor* tek = pronadjiCvor(kljuc);
	if (!tek)
		return false;

	tek->postaviInfo(-1);
	int i = strlen(kljuc) - 1;

	while (i >= 0 && tek && tek->brojPodstabala() == 0 && !tek->dohvatiInfo())
	{
		TrieCvor* roditelj = tek->roditelj();

		delete tek;
		m_brCvorova--;

		if (roditelj)
			roditelj->ukloniPodstablo(kljuc[i--]);
		else
			m_koren = nullptr;
		tek = roditelj;
	}

	m_brKljuceva--;
	return true;
}

void TrieStablo::obidji(ostream& it)
{
	if (m_koren)
		m_koren->poseti(it);
	else
		it << "Stablo je prazno." << endl;
}

int TrieStablo::dohvatiInfo(const char* kljuc)
{
	TrieCvor* cvor = pronadjiCvor(kljuc);

	if (cvor)
		return cvor->dohvatiInfo();

	return -1;
}

TrieStablo::TrieCvor* TrieStablo::TrieCvor::jedinoPodstablo()
{
	for (auto& i : m_niz_pokazivaca)
		if (i != nullptr)
			return i;

	return nullptr;
}

std::locale loc1("C");

void TrieStablo::nadjiPredlozene(TrieCvor* cvor, string trenutniPrefiks, vector<TrieCvor*>& spisak)
{
	if (cvor == nullptr || trenutniPrefiks.empty())
		return;

	if (cvor->dohvatiInfo() != 0)
		spisak.push_back(cvor);

	for (int i = 0; i < 255; i++)
	{
		char noviChar = static_cast<char>(i);
		if (!isalpha(noviChar, loc1))
			continue;

		TrieCvor* noviCvor = cvor->pronadjiPodstablo(i);
		if (noviCvor != nullptr)
		{
			trenutniPrefiks.push_back(noviChar);
			nadjiPredlozene(noviCvor, trenutniPrefiks, spisak);
			trenutniPrefiks.pop_back();
		}
	}
}

vector<pair<int, string>> TrieStablo::top3Predikcije(const vector<string>& spisak)
{
	priority_queue<pair<int, string>> pq;
	vector<pair<int, string>> predikcije;
	
	for (const string& permutacija : spisak)
	{
		auto* frekvencijaPermutacije = pronadjiCvor(permutacija.c_str());
		if (frekvencijaPermutacije != nullptr && frekvencijaPermutacije->dohvatiInfo() != -1)
			pq.push(pair(frekvencijaPermutacije->dohvatiInfo(), permutacija));
	}

	int top3 = 3;

	while (!pq.empty() && top3 != 0)
	{
		auto stavka = pq.top();
		pq.pop();

		predikcije.push_back(stavka);

		top3--;
	}

	return predikcije;
}

void TrieStablo::stampanjePredikcija(vector<pair<int, string>> predikcije)
{
	for (auto stavka : predikcije)
	{
		cout << stavka.second << " (" << stavka.first << ")" << endl;
	}

	cout << endl;
}

void TrieStablo::ispisIspravljenih(string kljuc)
{
	cout << "Ispravljamo greske..." << endl;

	cout << endl;

	vector<string> prva = Pomocno::prvaPermutacija(kljuc);
	vector<string> druga = Pomocno::drugaPermutacija(kljuc);
	vector<string> treca = Pomocno::trecaPermutacija(kljuc);

	cout << "Jedno slovo ispravljeno: " << endl;
	auto prviSpisak = top3Predikcije(prva);
	stampanjePredikcija(prviSpisak);

	cout << "Dva slova ispravljena: " << endl;
	auto drugiSpisak = top3Predikcije(druga);
	stampanjePredikcija(drugiSpisak);

	cout << "Tri slova ispravljena: " << endl;
	auto treciSpisak = top3Predikcije(treca);
	stampanjePredikcija(treciSpisak);

	// Sad ih spajamo da vidimo sta ce da bude

	vector<string> spojeni;
	spojeni.reserve(prva.size() + druga.size() + treca.size());
	spojeni.insert(spojeni.end(), prva.begin(), prva.end());
	spojeni.insert(spojeni.end(), druga.begin(), druga.end());
	spojeni.insert(spojeni.end(), treca.begin(), treca.end());

	auto top3IzSpojenih = top3Predikcije(spojeni);
	cout << endl << endl << "Top 3 iz spojenih, ispravljenih:" << endl;
	stampanjePredikcija(top3IzSpojenih);	
}

vector<pair<int, string>> TrieStablo::nadjiPredikcije(string kljuc)
{
	auto* stek = new stack<TrieCvor*>;

	TrieCvor* cvor = pronadjiCvor(kljuc.c_str(), stek);
	vector<pair<int, string>> predikcije;

	bool kljucPostoji = cvor != nullptr;

	ispisIspravljenih(kljuc);
	cout << endl;

	if (!kljucPostoji)
	{
		// Kljuc ne postoji cak ni kao prefiks
		// Gleda se da se isprave greske i da se tako nadju neki potencijalni kljucevi

		//ispisIspravljenih(kljuc);

		cout << endl;
	}
	else if (kljucPostoji && cvor->dohvatiInfo() == 0 && cvor->brojPodstabala() != 0)
	{
		cout << "Kljuc postoji kao prefiks..." << endl << endl;

		// Kljuc postoji kao prefiks
		// Ispisati tri najveca kljuca iz svih njegovih podstabala
		vector<TrieCvor*> spisak;

		nadjiPredlozene(cvor, kljuc, spisak);

		sort(spisak.begin(), spisak.end(), [](const TrieCvor* lhs, const TrieCvor* rhs)
		{
			return lhs->brojPonavljanja() > rhs->brojPonavljanja();
		});

		if (spisak.size() >= 1)
			predikcije.push_back(pair(spisak[0]->dohvatiInfo(), spisak[0]->dohvatiKljuc()));
		if (spisak.size() >= 2)
			predikcije.push_back(pair(spisak[1]->dohvatiInfo(), spisak[1]->dohvatiKljuc()));
		if (spisak.size() >= 3)
			predikcije.push_back(pair(spisak[2]->dohvatiInfo(), spisak[2]->dohvatiKljuc()));

		stampanjePredikcija(predikcije);
	}
	else
	{
		cout << "Postoji kljuc takav kakav je..." << endl << endl;

		// Kljuc postoji takav kakav je
		predikcije.push_back(pair(cvor->dohvatiInfo(), kljuc));

		stampanjePredikcija(predikcije);
	}

	
}
