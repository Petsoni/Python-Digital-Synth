class Oscillator:

    def __init__(self, function, gain, frequency, enabled):
        self.function = function
        self.gain = gain
        self.frequency = frequency
        self.enabled = False

    def value(self, n):
        if self.enabled:
            return self.gain * self.function(self.frequency, n)
        return 0

