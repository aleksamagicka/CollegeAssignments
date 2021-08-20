
namespace ORT2_Projekat
{
    partial class GlavnaForma
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.dgvKoraci = new System.Windows.Forms.DataGridView();
            this.gbKoraci = new System.Windows.Forms.GroupBox();
            this.btnGenerisiUslove = new System.Windows.Forms.Button();
            this.btnUkloniKorak = new System.Windows.Forms.Button();
            this.btnDodajKorak = new System.Windows.Forms.Button();
            this.gbAlgoritam = new System.Windows.Forms.GroupBox();
            this.btnOcistiSve = new System.Windows.Forms.Button();
            this.btnOcistiSveSemKoda = new System.Windows.Forms.Button();
            this.btnProcesirajKod = new System.Windows.Forms.Button();
            this.rtbKodAlgoritma = new System.Windows.Forms.RichTextBox();
            this.trakaMenija = new System.Windows.Forms.MenuStrip();
            this.algoritamToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.otvoriToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.snimiToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.pomoćToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.taboviTabele = new System.Windows.Forms.TabControl();
            this.tabPage1 = new System.Windows.Forms.TabPage();
            this.dgvUslovi = new System.Windows.Forms.DataGridView();
            this.tabPage2 = new System.Windows.Forms.TabPage();
            this.snimiProjekatDijalog = new System.Windows.Forms.SaveFileDialog();
            this.otvoriProjekatDialog = new System.Windows.Forms.OpenFileDialog();
            this.traka = new System.Windows.Forms.ToolStrip();
            this.tslLog = new System.Windows.Forms.ToolStripLabel();
            this.dgvGenerisaniKoraci = new System.Windows.Forms.DataGridView();
            this.btnGenerisiKorake = new System.Windows.Forms.Button();
            this.tabPage3 = new System.Windows.Forms.TabPage();
            this.label1 = new System.Windows.Forms.Label();
            this.lbRasporedInstrukcija = new System.Windows.Forms.Label();
            this.btnKopirajHexKoraka = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.dgvKoraci)).BeginInit();
            this.gbKoraci.SuspendLayout();
            this.gbAlgoritam.SuspendLayout();
            this.trakaMenija.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.taboviTabele.SuspendLayout();
            this.tabPage1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dgvUslovi)).BeginInit();
            this.tabPage2.SuspendLayout();
            this.traka.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dgvGenerisaniKoraci)).BeginInit();
            this.tabPage3.SuspendLayout();
            this.SuspendLayout();
            // 
            // dgvKoraci
            // 
            this.dgvKoraci.AllowUserToAddRows = false;
            this.dgvKoraci.AllowUserToDeleteRows = false;
            this.dgvKoraci.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.AllCells;
            this.dgvKoraci.AutoSizeRowsMode = System.Windows.Forms.DataGridViewAutoSizeRowsMode.AllCells;
            this.dgvKoraci.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgvKoraci.Location = new System.Drawing.Point(6, 19);
            this.dgvKoraci.Name = "dgvKoraci";
            this.dgvKoraci.Size = new System.Drawing.Size(764, 579);
            this.dgvKoraci.TabIndex = 0;
            // 
            // gbKoraci
            // 
            this.gbKoraci.Controls.Add(this.btnKopirajHexKoraka);
            this.gbKoraci.Controls.Add(this.btnGenerisiKorake);
            this.gbKoraci.Controls.Add(this.btnGenerisiUslove);
            this.gbKoraci.Controls.Add(this.btnUkloniKorak);
            this.gbKoraci.Controls.Add(this.btnDodajKorak);
            this.gbKoraci.Controls.Add(this.dgvKoraci);
            this.gbKoraci.Location = new System.Drawing.Point(12, 36);
            this.gbKoraci.Name = "gbKoraci";
            this.gbKoraci.Size = new System.Drawing.Size(919, 609);
            this.gbKoraci.TabIndex = 1;
            this.gbKoraci.TabStop = false;
            this.gbKoraci.Text = "Koraci";
            // 
            // btnGenerisiUslove
            // 
            this.btnGenerisiUslove.Location = new System.Drawing.Point(791, 123);
            this.btnGenerisiUslove.Name = "btnGenerisiUslove";
            this.btnGenerisiUslove.Size = new System.Drawing.Size(120, 33);
            this.btnGenerisiUslove.TabIndex = 3;
            this.btnGenerisiUslove.Text = "Generiši uslove";
            this.btnGenerisiUslove.UseVisualStyleBackColor = true;
            this.btnGenerisiUslove.Click += new System.EventHandler(this.btnGenerisiUslove_Click);
            // 
            // btnUkloniKorak
            // 
            this.btnUkloniKorak.Location = new System.Drawing.Point(791, 58);
            this.btnUkloniKorak.Name = "btnUkloniKorak";
            this.btnUkloniKorak.Size = new System.Drawing.Size(120, 33);
            this.btnUkloniKorak.TabIndex = 2;
            this.btnUkloniKorak.Text = "Ukloni korak";
            this.btnUkloniKorak.UseVisualStyleBackColor = true;
            this.btnUkloniKorak.Click += new System.EventHandler(this.btnUkloniKorak_Click);
            // 
            // btnDodajKorak
            // 
            this.btnDodajKorak.Location = new System.Drawing.Point(791, 19);
            this.btnDodajKorak.Name = "btnDodajKorak";
            this.btnDodajKorak.Size = new System.Drawing.Size(120, 33);
            this.btnDodajKorak.TabIndex = 1;
            this.btnDodajKorak.Text = "Dodaj korak";
            this.btnDodajKorak.UseVisualStyleBackColor = true;
            this.btnDodajKorak.Click += new System.EventHandler(this.btnDodajKorak_Click);
            // 
            // gbAlgoritam
            // 
            this.gbAlgoritam.Controls.Add(this.btnOcistiSve);
            this.gbAlgoritam.Controls.Add(this.btnOcistiSveSemKoda);
            this.gbAlgoritam.Controls.Add(this.btnProcesirajKod);
            this.gbAlgoritam.Controls.Add(this.rtbKodAlgoritma);
            this.gbAlgoritam.Location = new System.Drawing.Point(947, 36);
            this.gbAlgoritam.Name = "gbAlgoritam";
            this.gbAlgoritam.Size = new System.Drawing.Size(321, 609);
            this.gbAlgoritam.TabIndex = 2;
            this.gbAlgoritam.TabStop = false;
            this.gbAlgoritam.Text = "Algoritam";
            // 
            // btnOcistiSve
            // 
            this.btnOcistiSve.Location = new System.Drawing.Point(144, 560);
            this.btnOcistiSve.Name = "btnOcistiSve";
            this.btnOcistiSve.Size = new System.Drawing.Size(160, 38);
            this.btnOcistiSve.TabIndex = 3;
            this.btnOcistiSve.Text = "Resetuj sve";
            this.btnOcistiSve.UseVisualStyleBackColor = true;
            // 
            // btnOcistiSveSemKoda
            // 
            this.btnOcistiSveSemKoda.Location = new System.Drawing.Point(6, 560);
            this.btnOcistiSveSemKoda.Name = "btnOcistiSveSemKoda";
            this.btnOcistiSveSemKoda.Size = new System.Drawing.Size(132, 38);
            this.btnOcistiSveSemKoda.TabIndex = 2;
            this.btnOcistiSveSemKoda.Text = "Resetuj sve sem koda";
            this.btnOcistiSveSemKoda.UseVisualStyleBackColor = true;
            // 
            // btnProcesirajKod
            // 
            this.btnProcesirajKod.Location = new System.Drawing.Point(6, 511);
            this.btnProcesirajKod.Name = "btnProcesirajKod";
            this.btnProcesirajKod.Size = new System.Drawing.Size(298, 38);
            this.btnProcesirajKod.TabIndex = 1;
            this.btnProcesirajKod.Text = "Procesiraj kod";
            this.btnProcesirajKod.UseVisualStyleBackColor = true;
            // 
            // rtbKodAlgoritma
            // 
            this.rtbKodAlgoritma.Location = new System.Drawing.Point(12, 19);
            this.rtbKodAlgoritma.Name = "rtbKodAlgoritma";
            this.rtbKodAlgoritma.Size = new System.Drawing.Size(292, 486);
            this.rtbKodAlgoritma.TabIndex = 0;
            this.rtbKodAlgoritma.Text = "";
            // 
            // trakaMenija
            // 
            this.trakaMenija.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.algoritamToolStripMenuItem,
            this.pomoćToolStripMenuItem});
            this.trakaMenija.Location = new System.Drawing.Point(0, 0);
            this.trakaMenija.Name = "trakaMenija";
            this.trakaMenija.Size = new System.Drawing.Size(1279, 24);
            this.trakaMenija.TabIndex = 3;
            // 
            // algoritamToolStripMenuItem
            // 
            this.algoritamToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.otvoriToolStripMenuItem,
            this.snimiToolStripMenuItem});
            this.algoritamToolStripMenuItem.Name = "algoritamToolStripMenuItem";
            this.algoritamToolStripMenuItem.Size = new System.Drawing.Size(62, 20);
            this.algoritamToolStripMenuItem.Text = "Projekat";
            // 
            // otvoriToolStripMenuItem
            // 
            this.otvoriToolStripMenuItem.Name = "otvoriToolStripMenuItem";
            this.otvoriToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.O)));
            this.otvoriToolStripMenuItem.Size = new System.Drawing.Size(150, 22);
            this.otvoriToolStripMenuItem.Text = "Otvori";
            this.otvoriToolStripMenuItem.Click += new System.EventHandler(this.otvoriToolStripMenuItem_Click);
            // 
            // snimiToolStripMenuItem
            // 
            this.snimiToolStripMenuItem.Name = "snimiToolStripMenuItem";
            this.snimiToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.S)));
            this.snimiToolStripMenuItem.Size = new System.Drawing.Size(150, 22);
            this.snimiToolStripMenuItem.Text = "Snimi";
            this.snimiToolStripMenuItem.Click += new System.EventHandler(this.snimiToolStripMenuItem_Click);
            // 
            // pomoćToolStripMenuItem
            // 
            this.pomoćToolStripMenuItem.Name = "pomoćToolStripMenuItem";
            this.pomoćToolStripMenuItem.Size = new System.Drawing.Size(57, 20);
            this.pomoćToolStripMenuItem.Text = "Pomoć";
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.taboviTabele);
            this.groupBox1.Location = new System.Drawing.Point(18, 651);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(1249, 363);
            this.groupBox1.TabIndex = 4;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Generisane tabele";
            // 
            // taboviTabele
            // 
            this.taboviTabele.Controls.Add(this.tabPage1);
            this.taboviTabele.Controls.Add(this.tabPage2);
            this.taboviTabele.Controls.Add(this.tabPage3);
            this.taboviTabele.Location = new System.Drawing.Point(6, 19);
            this.taboviTabele.Name = "taboviTabele";
            this.taboviTabele.SelectedIndex = 0;
            this.taboviTabele.Size = new System.Drawing.Size(1227, 338);
            this.taboviTabele.TabIndex = 0;
            // 
            // tabPage1
            // 
            this.tabPage1.Controls.Add(this.dgvUslovi);
            this.tabPage1.Location = new System.Drawing.Point(4, 22);
            this.tabPage1.Name = "tabPage1";
            this.tabPage1.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage1.Size = new System.Drawing.Size(1219, 312);
            this.tabPage1.TabIndex = 0;
            this.tabPage1.Text = "Uslovi";
            this.tabPage1.UseVisualStyleBackColor = true;
            // 
            // dgvUslovi
            // 
            this.dgvUslovi.AllowUserToAddRows = false;
            this.dgvUslovi.AllowUserToDeleteRows = false;
            this.dgvUslovi.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.AllCells;
            this.dgvUslovi.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgvUslovi.Location = new System.Drawing.Point(6, 6);
            this.dgvUslovi.Name = "dgvUslovi";
            this.dgvUslovi.Size = new System.Drawing.Size(1207, 300);
            this.dgvUslovi.TabIndex = 0;
            // 
            // tabPage2
            // 
            this.tabPage2.Controls.Add(this.dgvGenerisaniKoraci);
            this.tabPage2.Location = new System.Drawing.Point(4, 22);
            this.tabPage2.Name = "tabPage2";
            this.tabPage2.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage2.Size = new System.Drawing.Size(1219, 312);
            this.tabPage2.TabIndex = 1;
            this.tabPage2.Text = "Generisani koraci";
            this.tabPage2.UseVisualStyleBackColor = true;
            // 
            // snimiProjekatDijalog
            // 
            this.snimiProjekatDijalog.DefaultExt = "json";
            this.snimiProjekatDijalog.Title = "Snimi projekat...";
            this.snimiProjekatDijalog.FileOk += new System.ComponentModel.CancelEventHandler(this.snimiProjekatDijalog_FileOk);
            // 
            // otvoriProjekatDialog
            // 
            this.otvoriProjekatDialog.Title = "Otvori projekat...";
            this.otvoriProjekatDialog.FileOk += new System.ComponentModel.CancelEventHandler(this.otvoriProjekatDialog_FileOk);
            // 
            // traka
            // 
            this.traka.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.traka.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.tslLog});
            this.traka.Location = new System.Drawing.Point(0, 1026);
            this.traka.Name = "traka";
            this.traka.Size = new System.Drawing.Size(1279, 25);
            this.traka.TabIndex = 5;
            // 
            // tslLog
            // 
            this.tslLog.Name = "tslLog";
            this.tslLog.Size = new System.Drawing.Size(36, 22);
            this.tslLog.Text = "Log...";
            this.tslLog.ToolTipText = "Log...";
            // 
            // dgvGenerisaniKoraci
            // 
            this.dgvGenerisaniKoraci.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.AllCells;
            this.dgvGenerisaniKoraci.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgvGenerisaniKoraci.Location = new System.Drawing.Point(6, 6);
            this.dgvGenerisaniKoraci.Name = "dgvGenerisaniKoraci";
            this.dgvGenerisaniKoraci.Size = new System.Drawing.Size(1207, 300);
            this.dgvGenerisaniKoraci.TabIndex = 0;
            // 
            // btnGenerisiKorake
            // 
            this.btnGenerisiKorake.Location = new System.Drawing.Point(791, 162);
            this.btnGenerisiKorake.Name = "btnGenerisiKorake";
            this.btnGenerisiKorake.Size = new System.Drawing.Size(120, 33);
            this.btnGenerisiKorake.TabIndex = 4;
            this.btnGenerisiKorake.Text = "Generiši korake";
            this.btnGenerisiKorake.UseVisualStyleBackColor = true;
            this.btnGenerisiKorake.Click += new System.EventHandler(this.btnGenerisiKorake_Click);
            // 
            // tabPage3
            // 
            this.tabPage3.Controls.Add(this.lbRasporedInstrukcija);
            this.tabPage3.Controls.Add(this.label1);
            this.tabPage3.Location = new System.Drawing.Point(4, 22);
            this.tabPage3.Name = "tabPage3";
            this.tabPage3.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage3.Size = new System.Drawing.Size(1219, 312);
            this.tabPage3.TabIndex = 2;
            this.tabPage3.Text = "Info";
            this.tabPage3.UseVisualStyleBackColor = true;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(16, 13);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(106, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Raspored instrukcija:";
            // 
            // lbRasporedInstrukcija
            // 
            this.lbRasporedInstrukcija.AutoSize = true;
            this.lbRasporedInstrukcija.Location = new System.Drawing.Point(128, 13);
            this.lbRasporedInstrukcija.Name = "lbRasporedInstrukcija";
            this.lbRasporedInstrukcija.Size = new System.Drawing.Size(16, 13);
            this.lbRasporedInstrukcija.TabIndex = 1;
            this.lbRasporedInstrukcija.Text = "...";
            // 
            // btnKopirajHexKoraka
            // 
            this.btnKopirajHexKoraka.Location = new System.Drawing.Point(791, 234);
            this.btnKopirajHexKoraka.Name = "btnKopirajHexKoraka";
            this.btnKopirajHexKoraka.Size = new System.Drawing.Size(120, 33);
            this.btnKopirajHexKoraka.TabIndex = 4;
            this.btnKopirajHexKoraka.Text = "Kopiraj hex koraka";
            this.btnKopirajHexKoraka.UseVisualStyleBackColor = true;
            this.btnKopirajHexKoraka.Click += new System.EventHandler(this.btnKopirajHexKoraka_Click);
            // 
            // GlavnaForma
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1279, 1051);
            this.Controls.Add(this.traka);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.gbAlgoritam);
            this.Controls.Add(this.gbKoraci);
            this.Controls.Add(this.trakaMenija);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MainMenuStrip = this.trakaMenija;
            this.MaximizeBox = false;
            this.Name = "GlavnaForma";
            this.Text = "ORT2 projekat";
            this.Load += new System.EventHandler(this.GlavnaForma_Load);
            ((System.ComponentModel.ISupportInitialize)(this.dgvKoraci)).EndInit();
            this.gbKoraci.ResumeLayout(false);
            this.gbAlgoritam.ResumeLayout(false);
            this.trakaMenija.ResumeLayout(false);
            this.trakaMenija.PerformLayout();
            this.groupBox1.ResumeLayout(false);
            this.taboviTabele.ResumeLayout(false);
            this.tabPage1.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.dgvUslovi)).EndInit();
            this.tabPage2.ResumeLayout(false);
            this.traka.ResumeLayout(false);
            this.traka.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dgvGenerisaniKoraci)).EndInit();
            this.tabPage3.ResumeLayout(false);
            this.tabPage3.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.DataGridView dgvKoraci;
        private System.Windows.Forms.GroupBox gbKoraci;
        private System.Windows.Forms.GroupBox gbAlgoritam;
        private System.Windows.Forms.MenuStrip trakaMenija;
        private System.Windows.Forms.ToolStripMenuItem algoritamToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem otvoriToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem snimiToolStripMenuItem;
        private System.Windows.Forms.RichTextBox rtbKodAlgoritma;
        private System.Windows.Forms.Button btnProcesirajKod;
        private System.Windows.Forms.ToolStripMenuItem pomoćToolStripMenuItem;
        private System.Windows.Forms.Button btnOcistiSve;
        private System.Windows.Forms.Button btnOcistiSveSemKoda;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.TabControl taboviTabele;
        private System.Windows.Forms.TabPage tabPage1;
        private System.Windows.Forms.TabPage tabPage2;
        private System.Windows.Forms.Button btnDodajKorak;
        private System.Windows.Forms.SaveFileDialog snimiProjekatDijalog;
        private System.Windows.Forms.OpenFileDialog otvoriProjekatDialog;
        private System.Windows.Forms.Button btnUkloniKorak;
        private System.Windows.Forms.Button btnGenerisiUslove;
        private System.Windows.Forms.DataGridView dgvUslovi;
        private System.Windows.Forms.ToolStrip traka;
        private System.Windows.Forms.ToolStripLabel tslLog;
        private System.Windows.Forms.DataGridView dgvGenerisaniKoraci;
        private System.Windows.Forms.Button btnGenerisiKorake;
        private System.Windows.Forms.TabPage tabPage3;
        private System.Windows.Forms.Label lbRasporedInstrukcija;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button btnKopirajHexKoraka;
    }
}

