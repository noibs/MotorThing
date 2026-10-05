from time import sleep

from machine import PWM, Pin


class StepperMotor:
    def __init__(self, pins, pwm_pct=0.5, frequency=16_000):
        # Configure the four PWM outputs
        self.outputs = [PWM(Pin(pin, Pin.OUT)) for pin in pins]
        for output in self.outputs:
            output.freq(frequency)

        # PWM duty cycle when an output is active
        val = pwm_pct
        # Store each step sequence under a separate mode name.
        self.modes = {
            "full": [
                [val, val, 0,   0  ],  # Step 0
                [0,   val, val, 0  ],  # Step 1
                [0,   0,   val, val],  # Step 2
                [val, 0,   0,   val],  # Step 3
            ],
            "half": [
                [val, 0,   0,   0  ],
                [val, val, 0,   0  ],
                [0,   val, 0,   0  ],
                [0,   val, val, 0  ],
                [0,   0,   val, 0  ],
                [0,   0,   val, val],
                [0,   0,   0,   val],
                [val, 0,   0,   val],
                ],
        }
        # Keep track of the currently selected mode.
        self.mode = "full"

    def set_step(self, step):
        """Apply one step to the selected PWM outputs."""
        for output, duty_cycle in zip(self.outputs, step):
            output.duty_u16(int(duty_cycle * 65535))

    def stop(self):
        """Set the PWM duty cycle of all outputs to zero."""
        for output in self.outputs:
            output.duty_u16(0)

    def set_step_mode(self, mode, microsteps=None):
        """Select full, half, or generated microstepping."""
        if mode not in self.modes:
            raise ValueError("Unknown mode: " + mode)
        self.mode = mode

    def move_stepper(self, steps, direction="forward", delay=0.01):
        """Move a number of steps forward or backward in the selected mode."""
        sequence = self.modes[self.mode]
        if direction == "backward":
            sequence = sequence[::-1]

        try:
            for i in range(steps):
                print("test")
                self.set_step(sequence[i % len(sequence)])
                sleep(delay)
        finally:
            self.stop()
