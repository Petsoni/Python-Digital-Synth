import sys

from PyQt5 import QtWidgets, uic

import Audio
import Signals
from audio_effects import Filters
from audio_parts.Modulator import Modulator
from audio_parts.Oscillator import Oscillator

sampling_frequency = 44100
second = sampling_frequency


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self, parent=None)
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Digital Synthetizer')
        self.statusbar.showMessage('Sampling Frequency: ' + str(sampling_frequency) + ' Hz')

        # UI Signals
        self.osc1Type.addItems(list(Signals.oscillators.keys()))
        self.osc2Type.addItems(list(Signals.oscillators.keys()))

        self.mod1Mode.addItems(list(Signals.modulation_modes.keys()))
        self.mod1Type.addItems(list(Signals.modulators.keys()))
        self.mod2Mode.addItems(list(Signals.modulation_modes.keys()))
        self.mod2Type.addItems(list(Signals.modulators.keys()))

        self.osc1Enable.stateChanged.connect(self.update_modules)
        self.osc2Enable.stateChanged.connect(self.update_modules)
        self.mod1Enable.stateChanged.connect(self.update_modules)
        self.mod2Enable.stateChanged.connect(self.update_modules)

        self.osc1Type.currentIndexChanged.connect(self.update_modules)
        self.osc2Type.currentIndexChanged.connect(self.update_modules)

        self.mod1Type.currentIndexChanged.connect(self.update_modules)
        self.mod2Type.currentIndexChanged.connect(self.update_modules)
        self.mod1Mode.currentIndexChanged.connect(self.update_modules)
        self.mod2Mode.currentIndexChanged.connect(self.update_modules)

        controls = [self.osc1Gain, self.osc1Freq, self.osc2Gain, self.osc2Freq,
                    self.mod1Gain, self.mod1Freq, self.mod2Gain, self.mod2Freq,
                    self.masterGain]
        for c in controls:
            c.valueChanged.connect(self.update_values)

        self.osc1 = Oscillator(None, 0, 0, False)
        self.osc2 = Oscillator(None, 0, 0, False)

        self.mod1 = Modulator(None, None, 0, 0, False)
        self.mod2 = Modulator(None, None, 0, 0, False)
        self.update_modules()

    def update_values(self):
        self.osc1GainLabel.setText('Gain: ' + str(self.osc1Gain.value() / 100 * 0.5))
        self.osc2GainLabel.setText('Gain: ' + str(self.osc2Gain.value() / 100 * 0.5))
        self.osc1FreqLabel.setText('Frequency: ' + str(self.osc1Freq.value() / 200 * 4000) + ' Hz')
        self.osc2FreqLabel.setText('Frequency: ' + str(self.osc2Freq.value() / 200 * 4000) + ' Hz')
        self.mod1GainLabel.setText('Gain: ' + str(self.mod1Gain.value() / 200))
        self.mod2GainLabel.setText('Gain: ' + str(self.mod2Gain.value() / 200))
        self.mod1FreqLabel.setText('Frequency: ' + str(self.mod1Freq.value() / 8) + 'Hz')
        self.mod2FreqLabel.setText('Frequency:' + str(self.mod2Freq.value() / 8) + 'Hz')

        self.masterGainLabel.setText('Master Volume: ' + str(self.masterGain.value() / 2) + '%')
        self.update_modules()

    def update_modules(self):
        self.osc1.function = Signals.oscillators[self.osc1Type.currentText()]
        self.osc1.gain = self.osc1Gain.value() / 200
        self.osc1.frequency = self.osc1Freq.value() / 200 * 4000
        self.osc1.enabled = self.osc1Enable.isChecked()

        self.osc2.function = Signals.oscillators[self.osc2Type.currentText()]
        self.osc2.gain = self.osc2Gain.value() / 200
        self.osc2.frequency = self.osc2Freq.value() / 200 * 4000
        self.osc2.enabled = self.osc2Enable.isChecked()

        self.mod1.modulationMode = Signals.modulation_modes[self.mod1Mode.currentText()]
        self.mod1.function = Signals.modulators[self.mod1Type.currentText()]
        self.mod1.gain = self.mod1Gain.value() / 200
        self.mod1.frequency = self.mod1Freq.value() / 8
        self.mod1.enabled = self.mod1Enable.isChecked()

        self.mod2.modulationMode = Signals.modulation_modes[self.mod2Mode.currentText()]
        self.mod2.function = Signals.modulators[self.mod2Type.currentText()]
        self.mod2.gain = self.mod2Gain.value() / 200
        self.mod2.frequency = self.mod2Freq.value() / 8
        self.mod2.enabled = self.mod2Enable.isChecked()

    def get_audio_function(self, n):

        oscillator_signal = lambda n: self.osc1.value(n) + self.osc2.value(n)

        modulated_signal = lambda n: self.mod2.value(lambda n: self.mod1.value(oscillator_signal, n), n)

        # Low pass filter
        f1 = modulated_signal
        if self.lowPassFilterEnable.isChecked():
            f1 = lambda n: Filters.low_pass_filter(modulated_signal, self.lowPassFilterGain.value() / 200,
                                                   self.lowPassFilterFreq.value() / 200, n)

        # High pass filter
        f2 = f1
        if self.highPassFilterEnable.isChecked():
            f2 = lambda n: Filters.high_pass_filter(f1, self.highPassFilterGain.value() / 200,
                                                    self.highPassFilterFreq.value() / 200, n)

        y = self.masterGain.value() / 200 * f2(n)
        if y < -1:
            return -1
        if y > 1:
            return 1
        return y


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    Audio.start()
    Audio.audioFunction = lambda n: window.get_audio_function(n)
    Audio.stop()
    Audio.terminate()
    sys.exit(app.exec_())
