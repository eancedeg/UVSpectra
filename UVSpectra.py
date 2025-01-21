#! /usr/bin/env python

import cclib
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QHeaderView, QTableWidgetItem
from PyQt5.QtWidgets import QApplication, QVBoxLayout
from PyQt5.QtCore import Qt
from ui.uvspectra import Ui_UVSpectra
import sys
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure
import numpy as np
from openpyxl import Workbook


class UVSpectraMainGUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, parent=None)

        self.ui = Ui_UVSpectra()
        self.ui.setupUi(self)
        self.resize(1000, 800)

        # Matplotlib integration
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self)

        mpllayout = QVBoxLayout(self.ui.mplwidget)
        mpllayout.addWidget(self.toolbar)
        mpllayout.addWidget(self.canvas)

        # Matplotlib personalization
        self.ax.set_title('UV Spectra')
        self.ax.set_ylabel('Intensity')
        self.ax.set_xlabel('Wavelength (nm)')
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        self.ax.set_xlim(180, 700)

        # Transitions table
        self.ui.transitiontable.setColumnCount(5)
        self.ui.transitiontable.setHorizontalHeaderLabels(['#', 'Transition', 'Oscillator Strength', '%',
                                                           'Wavelength (nm)'])

        header = self.ui.transitiontable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        self.data = ''

        # Events
        self.ui.actionOpen_Output.triggered.connect(self.outputopen)
        self.ui.peakwidth.valueChanged.connect(self.update_plot)
        self.ui.transnumber.valueChanged.connect(self.update_transitions)
        self.ui.savetransitions.clicked.connect(self.save_to_excel)

    def outputopen(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', "", 'All Files (*)')
        if filename:
            parser = cclib.io.ccopen(filename)
            self.data = parser.parse()
            self.update_plot()
            self.update_transitions()

    def update_plot(self):
        f = self.data.etoscs
        energies = 10000000 / self.data.etenergies
        wavelengths = np.linspace(np.min(energies) - 20, np.max(energies) + 20, 2000)
        width = self.ui.peakwidth.value()
        self.ui.peaklabel.setText(f'{width}')

        spectra = np.zeros_like(wavelengths)

        for energy, oscstr in zip(energies, f):
            spectra += self.gaussian(wavelengths, energy, width, oscstr)

        self.ax.clear()
        self.ax.plot(wavelengths, spectra, label='UV Spectra', color='blue')
        self.ax.vlines(energies, 0, f, color='red', label='f')
        self.ax.set_xlabel("Wavelength (nm)")
        self.ax.set_ylabel("Intensity")
        self.ax.set_title("UV Spectra")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

    def update_transitions(self):
        peaknumber = self.ui.transnumber.value()
        fosc = self.data.etoscs
        oscpeaksindexes = np.argsort(fosc)[-peaknumber::][::-1]
        energies = 10000000 / self.data.etenergies
        etsecs = self.data.etsecs
        homo = self.data.homos[0]

        transdata = []
        for osc in oscpeaksindexes:
            for orb in etsecs[osc]:
                if orb[2] > 0.1:

                    transdata.append((osc + 1,
                                      f'{self.orbital_name(orb[0][0], homo)} \u27F6 {self.orbital_name(orb[1][0], 
                                                                                                       homo)}',
                                      fosc[osc], round(orb[2] * 100, 2), round(energies[osc], 1)))

        self.ui.transitiontable.setRowCount(len(transdata))
        for transition in range(len(transdata)):
            for row, row_data in enumerate(transdata):
                for column, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                    self.ui.transitiontable.setItem(row, column, item)


    @staticmethod
    def gaussian(x, mu, sigma, amp):
        return amp * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

    @staticmethod
    def orbital_name(orbital, homo):
        if orbital == homo:
            return 'HOMO'
        elif orbital < homo:
            return f'HOMO - {homo - orbital}'
        elif orbital == homo + 1:
            return 'LUMO'
        else:
            return f'LUMO + {orbital - homo - 1}'

    def save_to_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Excel Files (*.xlsx)')

        if file_path:
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = 'Transitions'

            headers = [self.ui.transitiontable.horizontalHeaderItem(i).text()
                       for i in range(self.ui.transitiontable.columnCount())]
            sheet.append(headers)

            for row in range(self.ui.transitiontable.rowCount()):
                row_data = [
                    self.ui.transitiontable.item(row, column).text() if self.ui.transitiontable.item(row, column) else
                    "" for column in range(self.ui.transitiontable.columnCount())
                ]
                sheet.append(row_data)
            filename = file_path if file_path.endswith('.xlsx') else f'{file_path}.xlsx'
            workbook.save(filename)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    spectra = UVSpectraMainGUI()
    spectra.show()
    sys.exit(app.exec_())
