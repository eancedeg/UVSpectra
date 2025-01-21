#! /usr/bin/env python

import cclib
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QHeaderView, QTableWidgetItem, QMessageBox
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
import pandas as pd
from openpyxl import Workbook
from quantum import QuantumData


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
        self.ax.set_xlim(170, 700)

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
        self.outputfile = ''
        self.experimental = ''

        # Events
        self.ui.actionOpen_Output.triggered.connect(self.outputopen)
        self.ui.peakwidth.valueChanged.connect(self.update_plot)
        self.ui.transnumber.valueChanged.connect(self.update_transitions)
        self.ui.savetransitions.clicked.connect(self.save_to_excel)
        self.ui.show_gaussian.stateChanged.connect(self.update_gaussian)
        self.ui.add_experiment_data.triggered.connect(self.add_experimental)

    def add_experimental(self):
        if self.ui.show_gaussian.isChecked():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Gaussian warning')
            msg.setText('Uncheck "Show Gaussians" checkbox to show experimental spectra')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            filter_files = 'Excel Files (*.xlsx);;Text Files (*.txt);;CSV Files (*.csv)'
            filename, _ = QFileDialog.getOpenFileName(self, 'Open File', "", filter_files)
            if filename:
                self.experimental = pd.read_excel(filename)
                self.ax.clear()
                self.ax.set_ylabel('Absorbance', color='black')
                self.ax.tick_params(axis='y', labelcolor='black')

                wavelengths = self.experimental.iloc[:, 0]
                absorbance = self.experimental.iloc[:, 1]
                self.ax.plot(wavelengths, absorbance, label='Experimental', color='blue')
                self.ax.plot([], [], color='red', label='Osc. strength')

                # Pasar los osciladores al eje derecho
                self.ax_exp = self.ax.twinx()
                self.ax_exp.set_ylabel("Oscillator Strength", color='black')
                self.ax_exp.tick_params(axis='y', labelcolor='black')
                self.ax_exp.vlines(self.data.energies, 0, self.data.f, color='red', label='Oscillator Strength')
                self.ax.grid()
                self.ax.set_title('UV Spectra')
                self.ax.legend()
                self.canvas.draw()


    def outputopen(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', "", 'All Files (*)')
        if filename:
            self.outputfile = filename
            self.data = QuantumData(self.outputfile)
            self.update_plot()
            self.update_transitions()

    def update_gaussian(self):
        if self.ui.show_gaussian.isChecked():
            self.update_plot()
        else:
            self.ax.clear()
            self.ax.vlines(self.data.energies, 0, self.data.f, color='red', label='Osc. Strength')
            self.ax.legend()
            self.ax.grid()
            self.ax.set_title('Oscillator Strength')
            self.ax.set_ylabel('Osc. strength')
            self.ax.set_xlabel('Wavelength (nm)')
            self.canvas.draw()

    def update_plot(self):
        wavelengths = np.linspace(np.min(self.data.energies) - 20, np.max(self.data.energies) + 20, 2000)
        width = self.ui.peakwidth.value()
        self.ui.peaklabel.setText(f'{width}')

        spectra = np.zeros_like(wavelengths)

        for energy, oscstr in zip(self.data.energies, self.data.f):
            spectra += self.gaussian(wavelengths, energy, width, oscstr)

        self.ax.clear()
        self.ax.plot(wavelengths, spectra, label='UV Spectra', color='blue')
        self.ax.vlines(self.data.energies, 0, self.data.f, color='red', label='Osc. Strength')

        self.ax.legend()
        self.ax.grid()
        self.ax.set_title('UV Spectra')
        self.ax.set_ylabel('Intensity')
        self.ax.set_xlabel('Wavelength (nm)')
        self.canvas.draw()

        # if isinstance(self.experimental, pd.DataFrame) and not self.ui.show_gaussian.isChecked():
        #     self.ax.set_ylabel('Absorbance', color='black')
        #     self.ax.tick_params(axis='y', labelcolor='black')
        #
        #     wavelengths = self.experimental.iloc[:, 0]
        #     absorbance = self.experimental.iloc[:, 1]
        #     self.ax.plot(wavelengths, absorbance, label='Experimental', color='blue')
        #
        #     # Pasar los osciladores al eje derecho
        #     self.ax_exp = self.ax.twinx()
        #     self.ax_exp.set_ylabel("Oscillator Strength", color='red')
        #     self.ax_exp.tick_params(axis='y', labelcolor='red')
        #     self.ax_exp.vlines(energies, 0, f, color='red', label='Oscillator Strength')
        #
        # if self.ui.show_gaussian.isChecked():
        #     spectra = np.zeros_like(wavelengths)
        #
        #     for energy, oscstr in zip(energies, f):
        #         spectra += self.gaussian(wavelengths, energy, width, oscstr)
        #
        #     self.ax.plot(wavelengths, spectra, label='UV Spectra', color='blue')
        #     self.ax.vlines(energies, 0, f, color='red', label='Osc. Strength')
        #
        #     self.ax.set_ylabel('Intensity')
        #     self.ax.legend()
        #
        #     if hasattr(self, 'ax_exp'):
        #         self.ax_exp.clear()
        # else:
        #     self.ax.vlines(energies, 0, f, color='red', label='Osc. Strength')
        #     self.ax.set_ylabel('Osc. Strength')
        #     self.ax.legend()
        #
        #
        #     if hasattr(self, 'ax_exp'):
        #         self.ax_exp.clear()
        #
        # self.ax.set_xlabel("Wavelength (nm)")
        # self.ax.set_title("UV Spectra")
        #
        # # self.ax_exp.grid(True)
        # # self.ax.legend()
        # # self.ax_exp.legend()
        # self.ax.grid()
        # self.canvas.draw()

    def update_transitions(self):
        peaknumber = self.ui.transnumber.value()
        oscpeaksindexes = np.argsort(self.data.f)[-peaknumber::][::-1]
        energies = self.data.energies
        etsecs = self.data.etsecs
        homo = self.data.homo

        transdata = []
        for osc in oscpeaksindexes:
            for orb in etsecs[osc]:
                if orb[2] > 0.1:

                    transdata.append((osc + 1,
                                      f'{self.orbital_name(orb[0][0], homo)} \u27F6 {self.orbital_name(orb[1][0], 
                                                                                                       homo)}',
                                      self.data.f[osc], round(orb[2] * 100, 2), round(energies[osc], 1)))

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
