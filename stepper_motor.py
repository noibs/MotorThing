# Name: Elliott Hartmann Ulriksen
# Email: elulr26@student.sdu.dk

import math
import time

from machine import PWM, Pin


class StepperMotor:
    MIN_DELAY = 0.002

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

        # order: [A+, B+, A-, B-]
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

        # Default settings
        self.mode = "full"
        self.sequence = self.sequences["full"]
        self.total_steps = 0
        self.index = 0  # the row in sequence we are on

        self.stop()  # make sure everything is off at start

    def set_step(self, state):
        """Apply one sequence state to the four outputs."""
        for output, level in zip(self.outputs, state):
            # Here we multiply with pwm to get the right number
            output.duty_u16(int(level * self.pwm_pct * 65535))

    def stop(self):
        """Switch all four outputs off."""
        for output in self.outputs:
            # We set all outputs to 0 to turn motor off
            output.duty_u16(0)

    # Made this its own function because it was duplicated code
    def direction_to_sign(self, direction):
        """Turn "forward" into 1 and "backward" into -1."""
        if direction == "forward":
            return 1
        elif direction == "backward":
            return -1
        else:
            raise ValueError("direction must be 'forward' or 'backward'")

    def one_step(self, sign):
        """Move one row forward or backward"""
        self.index += sign

        # Wrap around at end of sequence
        if self.index >= len(self.sequence):
            self.index = 0
        if self.index < 0:
            self.index = len(self.sequence) - 1

        self.set_step(self.sequence[self.index])
        self.total_steps += sign

    def generate_microstep_sequence(self, microsteps):
        """Generate and return a complete microstep sequence.

        microsteps = number of microsteps per full step.
        The sequence has 4 * microsteps states
        One full motor turn = 200 * microsteps steps.

        """

        # We make sure microsteps is valid number
        if not isinstance(microsteps, int) or microsteps < 1:
            raise ValueError("microsteps must be 0 or positive integer")

        sequence = []
        n = 4 * microsteps

        for k in range(n):
            angle = 2 * math.pi * k / n

            a = round(math.cos(angle), 4)
            b = round(math.sin(angle), 4)

            # Coil A:
            # positive: A+ output. negative: A- output
            if a >= 0:
                a_pos = a
                a_neg = 0
            else:
                a_pos = 0
                a_neg = -a

            # Coil B:
            # positive: B+ output. negative: B- output
            if b >= 0:
                b_pos = b
                b_neg = 0
            else:
                b_pos = 0
                b_neg = -b

            sequence.append([a_pos, b_pos, a_neg, b_neg])  # A+, B+, A-, B-

        return sequence

    def set_step_mode(self, mode, microsteps=None):
        """Select which stored sequence move_stepper() will use."""

        if mode == "micro":
            if microsteps is None:
                raise ValueError("micro needs microstep value")
            name = "micro_" + str(microsteps)
            self.sequences[name] = self.generate_microstep_sequence(microsteps)
            mode = name

        if mode not in self.sequences:
            # Errors if user specified an unknown mode
            raise ValueError("Unknown mode: " + str(mode))

        self.mode = mode
        self.sequence = self.sequences[mode]
        self.index = 0

    def move_stepper(self, steps, direction, delay=0.001):
        """Move a number of steps. One step is one row of sequence"""
        # We convert direction to sign
        sign = self.direction_to_sign(direction)

        # We check steps is positive integer (to make sure no negative number reverse direction)
        if not isinstance(steps, int) or steps < 0:
            raise ValueError("steps must be 0 or positive integer")

        # We make sure specified delay does not go under 0.002
        delay = max(delay, self.MIN_DELAY)

        try:
            for i in range(steps):
                self.one_step(sign)
                time.sleep(delay)
        finally:
            self.stop()

    def rotate_continuous(self, direction, delay=0.01):
        """Rotates on direction until stopped"""
        sign = self.direction_to_sign(direction)

        delay = max(delay, self.MIN_DELAY)

        print("Rotating", direction)
        try:
            while True:
                self.one_step(sign)
                time.sleep(delay)
        except KeyboardInterrupt:
            print("Stopped total_steps =", self.total_steps)
        finally:
            self.stop()
