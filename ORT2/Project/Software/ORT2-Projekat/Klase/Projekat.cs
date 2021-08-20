using System;
using System.Collections.Generic;
using System.Linq;

namespace ORT2_Projekat.Klase
{
    class Projekat
    {
        public string Kod { get; set; }
        public List<Korak> Koraci { get; set; } = new List<Korak>();
        public List<Uslov> Uslovi { get; set; } = new List<Uslov>();

        public List<GenerisaniKorak> GenerisaniKoraci { get; set; } = new List<GenerisaniKorak>();

        // Info o koracima
        public string RedosledInstrukcija { get; set; }
        // TODO: Rasponi i brojevi uslova da idu ovde


        public int NoviRedniBrojKoraka()
        {
            if (Koraci?.Count == 0)
                return 0;

            return Koraci.Max(k => k.RedniBroj) + 1;
        }

        private int NoviRedniBrojUslova()
        {
            if (Uslovi?.Count == 0)
                return 2;

            return Uslovi.Max(k => k.RedniBroj) + 1;
        }

        public void GenerisiUslove()
        {
            Uslovi = new List<Uslov>
            {
                new Uslov {RedniBroj = 0, Sadrzaj = "(sledeci)"},
                new Uslov {RedniBroj = 1, Sadrzaj = "bruncnd"}
            };

            var uslovi = Koraci.Select(k => k.Uslov).Where(u => !string.IsNullOrWhiteSpace(u)).Distinct().ToList();
            foreach (var uslov in uslovi)
            {
                Uslovi.Add(new Uslov() {RedniBroj = NoviRedniBrojUslova(), Sadrzaj = uslov});
            }
        }

        List<string> NadjiSveInstrukcije()
        {
            return Koraci.SelectMany(k => k.GetSpisakKomandi().Split(new []{',', ' '}, StringSplitOptions.RemoveEmptyEntries)).Distinct().ToList();
        }

        public void GenerisiHexKorake()
        {
            GenerisaniKoraci?.Clear();

            int maxDuzinaKorakDela = Koraci.Max(k => Convert.ToString(k.RedniBroj, 2).Length);
            int maxDuzinaCCdela = Uslovi.Max(u => Convert.ToString(u.RedniBroj, 2).Length);

            var sveInstrukcije = NadjiSveInstrukcije();
            sveInstrukcije.Reverse();

            foreach (var korak in Koraci)
            {
                var listaBitova = new List<int>();

                // Dodavanje pokazivaca ka nekom skoku
                // TODO: Pedovanje nulama?
                if (korak.RedniBrojSkoka != "-1")
                {
                    string binarnoRedniBrojKoraka = Convert.ToString(Convert.ToInt64(korak.RedniBrojSkoka, 16), 2).PadLeft(maxDuzinaKorakDela);
                    foreach (var binarnaCifra in binarnoRedniBrojKoraka)
                    {
                        listaBitova.Add(binarnaCifra == '1' ? 1 : 0);
                    }
                }

                // Dodavanje uslova

                if (!string.IsNullOrWhiteSpace(korak.Uslov))
                {
                    // Ima uslov i verovatno ce negde da skace
                    // (Pedovati nulama do max duzine)

                    int redniBrojUslova = Uslovi.Find(u => u.Sadrzaj == korak.Uslov).RedniBroj;

                    string binarnoUslov = Convert.ToString(redniBrojUslova, 2).PadLeft(maxDuzinaCCdela, '0');
                    foreach (var binarnaCifra in binarnoUslov)
                    {
                        listaBitova.Add(binarnaCifra == '1' ? 1 : 0);
                    }
                }
                else
                {
                    // Uslova nema, dodati dovoljno nula koje ga prebacuju dalje
                    for (int i = 0; i < maxDuzinaCCdela; i++)
                        listaBitova.Add(0);
                }

                // Dodavanje instrukcija
                foreach (var t in sveInstrukcije)
                {
                    listaBitova.Add(korak.ImaInstrukciju(t) ? 1 : 0);
                }

                var generisaniKorak = new GenerisaniKorak();
                generisaniKorak.PocetakUslova = sveInstrukcije.Count - 1;
                generisaniKorak.PocetakSkocnogKoraka = generisaniKorak.PocetakUslova + maxDuzinaCCdela + 1;


                // TODO: Optimizovati
                var fdfk = listaBitova.Select(b => b.ToString()).ToList();
                string s = fdfk.Aggregate((a, b) => a + b); // TODO: string.Join ne radi nesto

                string hexBroj = Convert.ToInt32(s, 2).ToString("X");

                generisaniKorak.Binarno = s;
                generisaniKorak.Hex = hexBroj.PadLeft(6, '0');
                generisaniKorak.HexRb = korak.HexRedniBroj;

                GenerisaniKoraci.Add(generisaniKorak);

                RedosledInstrukcija = string.Join(", ", sveInstrukcije);

                
                
            }
        }
    }
}
