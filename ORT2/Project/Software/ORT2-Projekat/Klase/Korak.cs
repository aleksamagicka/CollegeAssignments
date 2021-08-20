using System;
using System.Linq;

namespace ORT2_Projekat.Klase
{
    class Korak
    {
        public int RedniBroj { get; set; }
        public string HexRedniBroj { get; set; }

        public string SpisakKomandi { get; set; }

        public string Uslov { get; set; }
        public string RedniBrojSkoka { get; set; } = "-1";
        public string Komentar { get; set; }

        string HeksadekadniPrikaz()
        {
            return null;
        }

        public bool ImaInstrukciju(string instrukcija)
        {
            if (SpisakKomandi == null)
                return false;

            return SpisakKomandi.Split(new[] {',', ' '}, StringSplitOptions.RemoveEmptyEntries).Select(t => t.ToLower())
                .Contains(instrukcija.ToLower());
        }

        // TODO: Popraviti!
        public string GetSpisakKomandi()
        {
            return SpisakKomandi ?? string.Empty;
        }
    }
}
