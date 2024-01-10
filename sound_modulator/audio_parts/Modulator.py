class Modulator:

    def __init__(self, mode, function, gain, frequency, enabled):
        self.modulationMode = mode
        self.function = function
        self.frequency = frequency
        self.enabled = False
        self.gain = gain

    def value(self, frequency, n):
        if self.enabled:
            return self.modulationMode(frequency, self.function, self.gain, self.frequency, n)
        return frequency(n)
