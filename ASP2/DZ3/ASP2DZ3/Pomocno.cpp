#include "Pomocno.h"

#include <algorithm>
#include <map>

vector<string> Pomocno::prvaPermutacija(string rec)
{
	vector<string> spisak;
	for (int i = 0; i < rec.length(); i++)
	{
		for (char novoSlovo : okolnaSlova(rec[i]))
		{
			string novaRec = rec;
			novaRec[i] = novoSlovo;

			spisak.push_back(novaRec);
		}
	}

	return spisak;
}

vector<string> Pomocno::drugaPermutacija(string rec)
{
	vector<string> spisak;

	if (rec.length() >= 2)
	{
		vector<int> permutacije(rec.length());
		permutacije[0] = permutacije[1] = 1;
		sort(permutacije.begin(), permutacije.end());

		do
		{
			// Izvuci gde su dve jedinice i krenuti odatle
			int i1 = -1, i2 = -1;
			for (int i = 0; i < permutacije.size(); i++)
			{
				if (permutacije[i] != 1)
					continue;

				if (i1 == -1)
					i1 = i;
				else if (i2 == -1)
				{
					i2 = i;
					break;
				}
			}

			vector<char> slovaZaPrvo = okolnaSlova(rec[i1]);
			vector<char> slovaZaDrugo = okolnaSlova(rec[i2]);

			for (char i : slovaZaPrvo)
			{
				string novaRec = rec;
				novaRec[i1] = i;

				// Sad ide cuclanje ovog drugog slova sa ovim prvim fiksiranim

				for (char j : slovaZaDrugo)
				{
					string novaRec2 = novaRec;
					novaRec2[i2] = j;

					spisak.push_back(novaRec2);
				}
			}
		}
		while (next_permutation(permutacije.begin(), permutacije.end()));
	}

	return spisak;
}

vector<string> Pomocno::trecaPermutacija(string rec)
{
	vector<string> spisak;

	if (rec.length() >= 3)
	{
		vector<int> permutacije(rec.length());
		permutacije[0] = permutacije[1] = permutacije[2] = 1;
		sort(permutacije.begin(), permutacije.end());

		do
		{
			// Izvuci gde su dve jedinice i krenuti odatle
			int i1 = -1, i2 = -1, i3 = -1;
			for (int i = 0; i < permutacije.size(); i++)
			{
				if (permutacije[i] != 1)
					continue;

				if (i1 == -1)
					i1 = i;
				else if (i2 == -1)
					i2 = i;
				else if (i3 == -1)
				{
					i3 = i;
					break;
				}
			}

			vector<char> slovaZaPrvo = okolnaSlova(rec[i1]);
			vector<char> slovaZaDrugo = okolnaSlova(rec[i2]);
			vector<char> slovaZaTrece = okolnaSlova(rec[i3]);

			for (char i : slovaZaPrvo)
			{
				string novaRec = rec;
				novaRec[i1] = i;

				// Sad ide cuclanje ovog drugog slova sa ovim prvim fiksiranim

				for (char j : slovaZaDrugo)
				{
					string novaRec2 = novaRec;
					novaRec2[i2] = j;

					// Sad ide cuclanje ovog treceg slova sa ovim prvim + drugim fiksiranim

					for (char k : slovaZaTrece)
					{
						string novaRec3 = novaRec2;
						novaRec3[i3] = k;

						spisak.push_back(novaRec3);
					}
				}
			}
		}
		while (next_permutation(permutacije.begin(), permutacije.end()));
	}

	return spisak;
}

vector<char> Pomocno::okolnaSlova(char slovo)
{
	switch (slovo)
	{
	case 'q':
		return {'v', 'a'};
	case 'w':
		return {'q', 'e', 'a', 's'};
	case 'e':
		return {'w', 'r', 's', 'd'};
	case 'r':
		return {'e', 't', 'd', 'f'};
	case 't':
		return {'r', 'y', 'f', 'g'};
	case 'y':
		return {'t', 'u', 'g', 'h'};
	case 'u':
		return {'y', 'i', 'h', 'j'};
	case 'i':
		return {'u', 'o', 'j', 'k'};
	case 'o':
		return {'i', 'p', 'k', 'l'};
	case 'p':
		return {'o', 'l'};
	case 'a':
		return {'q', 'w', 's', 'z'};
	case 's':
		return {'w', 'e', 'd', 'a', 'z', 'x'};
	case 'd':
		return {'e', 'r', 'f', 'c', 'x', 's', 'z'};
	case 'f':
		return {'r', 't', 'g', 'v', 'c', 'd', 'x'};
	case 'g':
		return {'t', 'y', 'h', 'b', 'v', 'c', 'f'};
	case 'h':
		return {'y', 'u', 'j', 'n', 'b', 'v', 'g'};
	case 'j':
		return {'u', 'i', 'k', 'm', 'n', 'h', 'b'};
	case 'k':
		return {'i', 'o', 'l', 'm', 'n', 'j'};
	case 'l':
		return {'o', 'p', 'k', 'm'};
	case 'z':
		return {'a', 's', 'd', 'x'};
	case 'x':
		return {'z', 's', 'd', 'f', 'c'};
	case 'c':
		return {'x', 'd', 'f', 'g', 'v'};
	case 'v':
		return {'c', 'f', 'g', 'h', 'b'};
	case 'b':
		return {'v', 'g', 'h', 'j', 'n'};
	case 'n':
		return {'b', 'h', 'j', 'k', 'm'};
	case 'm':
		return {'n', 'j', 'k', 'l'};
	}
}
