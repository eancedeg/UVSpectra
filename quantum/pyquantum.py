import cclib
import numpy as np

class QuantumData(object):
    def __init__(self, calc_file: str):
        self.calc_file = calc_file

        parser = cclib.io.ccopen(self.calc_file)
        self.data = parser.parse()
        self.f = self.data.etoscs
        self.energies = 10000000 / self.data.etenergies
        self.wavelengths = np.linspace(np.min(self.energies) - 20, np.max(self.energies) + 20, 2000)
        self.etsecs = self.data.etsecs
        self.homo = self.data.homos[0]
