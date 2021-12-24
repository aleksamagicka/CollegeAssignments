package com.aleksasavic;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.EventQueue;
import java.awt.Frame;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import javax.swing.JComboBox;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.Timer;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.table.DefaultTableModel;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.axis.NumberTickUnit;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

import com.ireasoning.protocol.snmp.SnmpConst;
import com.ireasoning.protocol.snmp.SnmpSession;
import com.ireasoning.protocol.snmp.SnmpTableModel;
import com.ireasoning.protocol.snmp.SnmpVarBind;

public class RM2Projekat extends Frame {
	private Timer timer;

	public static String[] routerHostnames = { "192.168.10.1", "192.168.20.1", "192.168.30.1" };
	public static int snmpPort = 161;
	public static int snmpVersion = SnmpConst.SNMPV2;
	public static String snmpCommunity = "si2019";

	DefaultTableModel model;
	private List<RouterInterface> interfaces;

	GrafikPanel graph;
	RouterInterface selectedInf = null;
	JComboBox<String> cb;

	JTable table;
	int lastSelectedRow = 0;

	public RM2Projekat(final String title) {
		super(title);

		interfaces = new ArrayList<>();

		setupGUI();
		setupTimer();
		setupSNMP();
	}

	private void setupSNMP() {
		SnmpSession.loadMib2();

		for (String hostname : routerHostnames) {
			try {
				SnmpSession session = new SnmpSession(hostname, snmpPort, snmpCommunity, snmpCommunity,
						snmpVersion);

				session.setTimeout(5000);

				SnmpTableModel tm = session.snmpGetTable("ifTable");
				tm.setTranslateValue(true);

				System.out.println("OBRADJUJEM HOSTNAME: " + hostname);

				/*
				 * Za svaki interfejs: Broj: 0, ifIndex Broj: 1, ifDescr Broj: 2, ifType Broj:
				 * 9, ifInOctets Broj: 10, ifInUcastPkts Broj: 11, ifInNUcastPkts Broj: 15,
				 * ifOutOctets Broj: 16, ifOutUcastPkts Broj: 17, ifOutNUcastPkts
				 */

				for (int i = 0; i < tm.getRowCount(); i++) {
					SnmpVarBind[] cr = tm.getRow(i); // currentRow

					RouterInterface newIf = new RouterInterface();
					newIf.ID = Integer.parseInt(cr[0].getValue().toString());
					newIf.Name = cr[1].getValue().toString();
					newIf.Type = cr[2].getValue().toString();
					newIf.InOctets.add(Integer.parseInt(cr[9].getValue().toString()));
					newIf.InUniPkts.add(Integer.parseInt(cr[10].getValue().toString()));
					newIf.InNUniPkts.add(Integer.parseInt(cr[11].getValue().toString()));
					newIf.OutOctets.add(Integer.parseInt(cr[15].getValue().toString()));
					newIf.OutUniPkts.add(Integer.parseInt(cr[16].getValue().toString()));
					newIf.OutNUniPkts.add(Integer.parseInt(cr[17].getValue().toString()));

					newIf.Hostname = hostname;

					interfaces.add(newIf);
					model.addRow(newIf.GetRow());
				}

			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	private void setupTimer() {
		timer = new Timer(10 * 1000, new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				model.setRowCount(0);

				for (String host : routerHostnames) {
					SnmpSession session;
					try {
						session = new SnmpSession(host, snmpPort, snmpCommunity, snmpCommunity, snmpVersion);

						session.setTimeout(5000);

						SnmpTableModel tm = session.snmpGetTable("ifTable");
						tm.setTranslateValue(true);

						for (int i = 0; i < tm.getRowCount(); i++) {
							SnmpVarBind[] cr = tm.getRow(i); // currentRow

							RouterInterface newIf = null;
							for (var inf : interfaces) {
								if (inf.ID == Integer.parseInt(cr[0].getValue().toString())
										&& inf.Hostname.equals(host)) {
									newIf = inf;
									break;
								}
							}

							newIf.InOctets.add(Integer.parseInt(cr[9].getValue().toString()));
							newIf.InUniPkts.add(Integer.parseInt(cr[10].getValue().toString()));
							newIf.InNUniPkts.add(Integer.parseInt(cr[11].getValue().toString()));
							newIf.OutOctets.add(Integer.parseInt(cr[15].getValue().toString()));
							newIf.OutUniPkts.add(Integer.parseInt(cr[16].getValue().toString()));
							newIf.OutNUniPkts.add(Integer.parseInt(cr[17].getValue().toString()));

							newIf.getProtok(newIf.InOctets, newIf.PInOctets);
							newIf.getProtok(newIf.InUniPkts, newIf.PInUniPkts);
							newIf.getProtok(newIf.InNUniPkts, newIf.PInNUniPkts);
							newIf.getProtok(newIf.OutOctets, newIf.POutOctets);
							newIf.getProtok(newIf.OutUniPkts, newIf.POutUniPkts);
							newIf.getProtok(newIf.OutNUniPkts, newIf.POutNUniPkts);

							model.addRow(newIf.GetRow());
						}

					} catch (IOException e1) {
						e1.printStackTrace();
					}

					model.fireTableDataChanged();
					// table.repaint();
					// table.setRowSelectionInterval(lastSelectedRow, lastSelectedRow);

					updateGraph(cb);
				}
			}
		});
	}

	class GrafikPanel extends JPanel {

		JFreeChart myChart;
		ChartPanel chartPanel;
		XYSeriesCollection myDataset;

		private GrafikPanel() {
			setLayout(new GridLayout());
			XYSeries myData = new XYSeries("Podaci");
			myDataset = new XYSeriesCollection();
			myDataset.addSeries(myData);
			myChart = ChartFactory.createXYLineChart("Grafik", "Vreme [10s]", "Vrednost", myDataset, PlotOrientation.VERTICAL,
					true, true, false);
			chartPanel = new ChartPanel(myChart);
			
			XYPlot plot = (XYPlot) myChart.getPlot();
			NumberAxis xAxis = (NumberAxis) plot.getDomainAxis();
			xAxis.setTickUnit(new NumberTickUnit(1));
			
			this.add(chartPanel);
		}

		@Override
		public Dimension getPreferredSize() {
			return new Dimension(512, 256);
		}
	}

	private void updateGraph(JComboBox cb) {
		String selected = (String) cb.getSelectedItem();

		if (selected.equals("None"))
			return;

		ArrayList<Integer> values = null;

		switch (selected) {
		case "InOctets":
			values = selectedInf.InOctets;
			break;
		case "P-InOctets":
			values = selectedInf.PInOctets;
			break;
		case "InUCastPkts":
			values = selectedInf.InUniPkts;
			break;
		case "P-InUCastPkts":
			values = selectedInf.PInUniPkts;
			break;
		case "InNUCastPkts":
			values = selectedInf.InNUniPkts;
			break;
		case "P-InNUCastPkts":
			values = selectedInf.PInNUniPkts;
			break;
		case "OutOctets":
			values = selectedInf.OutOctets;
			break;
		case "P-OutOctets":
			values = selectedInf.POutOctets;
			break;
		case "OutUCastPkts":
			values = selectedInf.OutUniPkts;
			break;
		case "P-OutUCastPkts":
			values = selectedInf.POutUniPkts;
			break;
		case "OutNUCastPkts":
			values = selectedInf.OutNUniPkts;
			break;
		case "P-OutNUCastPkts":
			values = selectedInf.POutNUniPkts;
			break;
		}

		float[] f = new float[values.size()];
		for (int j = 0; j < f.length; j++)
			f[j] = (float) values.get(j);

		graph.myDataset.removeAllSeries();

		XYSeries myData = new XYSeries(selectedInf.Hostname + ", " + selectedInf.Name + ", " + selected);
		myData.add(0, 0);
		for (int i = 0; i < values.size(); i++)
			myData.add(i, values.get(i));

		graph.myDataset.addSeries(myData);
	}

	private void setupGUI() {
		graph = new GrafikPanel();
		this.add(graph, BorderLayout.CENTER);

		addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				dispose();
			}
		});

		String[] choices = { "None", "InOctets", "P-InOctets", "InUCastPkts", "P-InUCastPkts", "InNUCastPkts",
				"P-InNUCastPkts", "OutOctets", "P-OutOctets", "OutUCastPkts", "P-OutUCastPkts", "OutNUCastPkts",
				"P-OutNUCastPkts" };

		cb = new JComboBox<String>(choices);
		this.add(cb, BorderLayout.SOUTH);

		cb.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				updateGraph((JComboBox) e.getSource());
			}
		});

		String[] columnNames = { "Hostname", "ID", "Descr.", "Type", "InOctets", "P-InOctets", "InUCastPkts",
				"P-InUCastPkts", "InNUcastPkts", "P-InNUcastPkts", "OutOctets", "P-OutOctets", "OutUCastPkts",
				"P-OutUCastPkts", "OutNUCastPkts", "P-OutNUCastPkts" };
		model = new DefaultTableModel(columnNames, 0);

		table = new JTable(model);
		table.getSelectionModel().addListSelectionListener(new ListSelectionListener() {

			@Override
			public void valueChanged(ListSelectionEvent e) {
				if (!e.getValueIsAdjusting() && table.getSelectedRow() != -1) {
					lastSelectedRow = table.getSelectedRow();
					int id = Integer.parseInt(table.getValueAt(lastSelectedRow, 1).toString());
					String host = table.getValueAt(lastSelectedRow, 0).toString();
					for (var inf : interfaces) {
						if (inf.ID == id && inf.Hostname.equals(host)) {
							selectedInf = inf;
							break;
						}
					}

					updateGraph(cb);
				}
			}
		});

		JScrollPane scrollPane = new JScrollPane(table);
		table.setFillsViewportHeight(true);
		this.add(scrollPane, BorderLayout.NORTH);
	}

	public void start() {
		timer.start();
	}

	public static void main(final String[] args) {
		EventQueue.invokeLater(new Runnable() {
			@Override
			public void run() {
				RM2Projekat mainFrame = new RM2Projekat("RM2: Grafik protoka - Aleksa Savic (595/19)");
				mainFrame.pack();
				mainFrame.setSize(1500, 2000);
				mainFrame.setVisible(true);
				mainFrame.start();
			}
		});
	}
}