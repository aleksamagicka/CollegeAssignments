using System;
using System.Collections.Generic;
using System.IO;
using System.Windows.Forms;
using Newtonsoft.Json;
using ORT2_Projekat.Klase;

namespace ORT2_Projekat
{
    public partial class GlavnaForma : Form
    {
        public GlavnaForma()
        {
            InitializeComponent();
        }

        private Projekat projekat;
        private BindingSource _korakBindingSource;
        private BindingSource _usloviBindingSource;
        private BindingSource _generisaniKoraciBindingSource;

        private void btnDodajKorak_Click(object sender, EventArgs e)
        {
            _korakBindingSource.Add(new Korak
            {
                RedniBroj = projekat.NoviRedniBrojKoraka(),
                HexRedniBroj = projekat.NoviRedniBrojKoraka().ToString("X")
            });
        }

        void PostaviLogTekst(string tekst)
        {
            tslLog.Text = tekst;
        }

        private void GlavnaForma_Load(object sender, EventArgs e)
        {
            projekat = new Projekat();

            PostaviBindingSource();

            PostaviLogTekst("Program učitan...");
        }

        void PostaviBindingSource()
        {
            PostaviKorakBindingSource();
            PostaviUsloviBindingSource();
        }

        private void PostaviUsloviBindingSource()
        {
            _usloviBindingSource = new BindingSource(projekat.Uslovi, null);
            dgvUslovi.DataSource = _usloviBindingSource;
        }

        private void PostaviKorakBindingSource()
        {
            _korakBindingSource = new BindingSource(projekat.Koraci, null);
            dgvKoraci.DataSource = _korakBindingSource;
        }

        private void PostaviGenerisaniKoraciBindingSource()
        {
            _generisaniKoraciBindingSource = new BindingSource(projekat.GenerisaniKoraci, null);
            dgvGenerisaniKoraci.DataSource = _generisaniKoraciBindingSource;
        }

        private void otvoriToolStripMenuItem_Click(object sender, EventArgs e)
        {
            otvoriProjekatDialog.ShowDialog();
        }

        private void snimiToolStripMenuItem_Click(object sender, EventArgs e)
        {
            snimiProjekatDijalog.ShowDialog();
        }

        private void snimiProjekatDijalog_FileOk(object sender, System.ComponentModel.CancelEventArgs e)
        {
            File.WriteAllText(snimiProjekatDijalog.FileName, JsonConvert.SerializeObject(projekat));
            PostaviLogTekst("Projekat snimljen!");
        }

        private void otvoriProjekatDialog_FileOk(object sender, System.ComponentModel.CancelEventArgs e)
        {
            projekat = JsonConvert.DeserializeObject<Projekat>(File.ReadAllText(otvoriProjekatDialog.FileName));
            PostaviBindingSource();

            PostaviLogTekst("Projekat učitan!");
        }

        private void btnUkloniKorak_Click(object sender, EventArgs e)
        {
            if (dgvKoraci.CurrentRow != null)
                dgvKoraci.Rows.RemoveAt(dgvKoraci.CurrentRow.Index);

            PostaviLogTekst("Korak uklonjen!");
        }

        private void btnGenerisiUslove_Click(object sender, EventArgs e)
        {
            projekat.GenerisiUslove();
            PostaviUsloviBindingSource();

            PostaviLogTekst("Uslovi generisani!");
        }

        private void btnGenerisiKorake_Click(object sender, EventArgs e)
        {
            projekat.GenerisiHexKorake();
            PostaviGenerisaniKoraciBindingSource();

            lbRasporedInstrukcija.Text = projekat.RedosledInstrukcija;

            PostaviLogTekst("Generisani koraci!");
        }

        private void btnKopirajHexKoraka_Click(object sender, EventArgs e)
        {
            List<string> heksovi = new List<string>();
            foreach (var generisaniKorak in projekat.GenerisaniKoraci)
            {
                heksovi.Add(generisaniKorak.Hex);
            }

            Clipboard.SetText(string.Join(" ", heksovi));
            PostaviLogTekst("Heksovi kopirani!");
        }
    }
}
