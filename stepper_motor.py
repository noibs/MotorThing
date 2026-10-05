# Name: Elliott Hartmann Ulriksen
# Email: elulr26@student.sdu.dk

import time

from machine import PWM, Pin


class StepperMotor:
    def __init__(self, pins, pwm_pct=0.15, frequency=18_000):
        if len(pins) != 4:
            # Error if there is more or less than 4 pins specified
            raise ValueError("pins must contain exactly 4 GPIO numbers")

        self.pwm_pct = pwm_pct
        self.frequency = frequency

        # We set up the four PWM outputs
        self.outputs = []
        for pin in pins:
            pwm = PWM(Pin(pin, Pin.OUT))
            pwm.freq(frequency)
            self.outputs.append(pwm)

        # Sequences are stored as levels 0..1; pwm_pct scales them in set_step().
        # Column order: [A+, B+, A-, B-]
        # I put 0 and 1s for more readability, i multiply with pwm later
        self.sequences = {
            "full": [
                [1, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 1],
                [1, 0, 0, 1],
            ],
            "half": [
                [1, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 0, 1],
                [1, 0, 0, 1],
            ],
        }

        self.mode = "full"
        self.sequence = self.sequences["full"]
        self.total_steps = 0
        self.index = 0      # the row in sequence we on

        self.stop()   # make sure everything if off at start

    def set_step(self, state):
        """Apply one sequence state to the four outputs."""
        for output, level in zip(self.outputs, state):
            # Here we multiply with pwm to get the right number
            output.duty_u16(int(level * self.pwm_pct * 65535))

    def stop(self):
        """Switch all four outputs off."""
        for output in self.outputs:
            output.duty_u16(0)

    def set_step_mode(self, mode, microsteps=None):
        """Select which stored sequence move_stepper() will use."""
        if mode not in self.sequences:
            # Errors if user specified an unknown mode
            raise ValueError("Unknown mode: " + str(mode))
        self.mode = mode
        self.sequence = self.sequences[mode]
        self.index = 0

    MIN_DELAY = 0.002

    def move_stepper(self, steps, direction, delay=0.001):
        """Move a number of steps. One step is one row of sequence"""
        # We check direction
        if direction == "forward":
            dir = 1
        elif direction == "backward":
            dir = -1
        else:
            raise ValueError("direction must be forward or backward")

        # We check steps is positive integer (to make sure no negative number reverse direction)
        if not isinstance(steps, int) or steps < 0:
            raise ValueError("steps must be positive integer")

        # Check min delay
        if delay < self.MIN_DELAY:
            delay = self.MIN_DELAY

        # Step through sequence
        n = len(self.sequence)
        try:
            for _ in range(steps):
                self.index = (self.index + dir) % n
                self.set_step(self.sequence[self.index])
                self.total_steps += dir
                time.sleep(delay)
        finally:    # We ensure outputs always turn off, no matter what error we get
            self.stop()

    def rotate_continuous(self, direction, delay=0.01):
        """Rotates on direction until stopped"""
        # We check direction
        if direction == "forward":
            dir = 1
        elif direction == "backward":
            dir = -1
        else:
            raise ValueError("direction must be forward or backward")

        if delay < self.MIN_DELAY:
            delay = self.MIN_DELAY

        n = len(self.sequence)
        print("Rotating", direction)
        try:
            while True:
                self.index = (self.index + dir) % n
                self.set_step(self.sequence[self.index])
                self.total_steps += dir
                time.sleep(delay)
        except KeyboardInterrupt:
            print("Stopped. total_steps =", self.total_steps)
        finally:
            self.stop()
