# Name: Elliott Hartmann Ulriksen
# Email: elulr26@student.sdu.dk

import time

from stepper_motor import StepperMotor



# ---------------- SETTINGS - change these ----------------
TEST = 4  # which test to run (see list below) bhjmk
MICROSTEPS = 8  # microsteps per full step, used in tests 4 and 6
MOTOR_PWM = 0.65  # PWM for motor tests (start at 0.5, raise if weak)
# ---------------------------------------------------------

# 1  LEDs  full step forward/backward + total_steps
# 2  LEDs  continuous rotation (stop with Ctrl+C)
# 3  LEDs  half step at 25 / 50 / 100 %      -> VIDEO 1
# 4  LEDs  generated microstep sequence      -> VIDEO 2
# 5  MOTOR half step, one full rotation      -> VIDEO 3
# 6  MOTOR microstep, one full rotation      -> VIDEO 4
# 7  LEDs  mode switching + invalid microsteps (self-check)

if TEST == 5 or TEST == 6:
    motor = StepperMotor([0, 1, 2, 3], pwm_pct=MOTOR_PWM)  # motor

else:
    motor = StepperMotor([16, 17, 18, 19], pwm_pct=0.5)  # LEDs

try:
    if TEST == 1:
        """print("TEST 1: full step on LEDs")
        motor.set_step_mode("full")
        motor.move_stepper(200, "forward", delay=0.3)
        print("total_steps after forward:", motor.total_steps)    # 8
        motor.move_stepper(200, "backward", delay=0.3)
        print("total_steps after backward:", motor.total_steps)   # 0"""

        motor.set_step_mode("full")
        motor.move_stepper(200, "forward", delay=0.01)
        print("total_steps after forward:", motor.total_steps)

    elif TEST == 2:
        print("TEST 2: continuous rotation on LEDs")
        motor.set_step_mode("full")
        motor.rotate_continuous("forward", delay=0.2)

    elif TEST == 3:
        print("TEST 3: half step at 25 / 50 / 100 % on LEDs")
        motor.set_step_mode("half")
        for pct in [0.25, 0.5, 1.0]:
            motor.pwm_pct = pct
            print("PWM =", pct * 100, "%")
            print("  forward")
            motor.move_stepper(8, "forward", delay=0.4)
            print("  total_steps:", motor.total_steps)
            print("  backward")
            motor.move_stepper(8, "backward", delay=0.4)
            print("  total_steps:", motor.total_steps)
            time.sleep(1)

    elif TEST == 4:
        print("TEST 4: microstep sequence on LEDs, microsteps =", MICROSTEPS)
        motor.set_step_mode("micro", MICROSTEPS)
        for state in motor.sequence:
            print(state)
        steps = 4 * MICROSTEPS  # one electrical cycle
        print("forward")
        motor.move_stepper(steps, "forward", delay=0.1)
        print("  total_steps:", motor.total_steps)
        print("backward")
        motor.move_stepper(steps, "backward", delay=0.1)
        print("  total_steps:", motor.total_steps)

    elif TEST == 5:
        print("TEST 5: MOTOR half step, one full rotation")
        motor.set_step_mode("half")
        motor.move_stepper(400, "forward", delay=0.01)  # 400 half steps = 360 deg
        print("total_steps:", motor.total_steps)

    elif TEST == 6:
        print("TEST 6: MOTOR microstep, one full rotation, microsteps =", MICROSTEPS)
        motor.set_step_mode("micro", MICROSTEPS)
        steps = 200 * MICROSTEPS  # 200 full steps = 360 deg
        motor.move_stepper(steps, "forward", delay=0.002)
        print("total_steps:", motor.total_steps)

    elif TEST == 7:
        print("TEST 7: mode switching and invalid values")
        motor.set_step_mode("full")
        motor.move_stepper(4, "forward", delay=0.3)
        print("full  -> total_steps:", motor.total_steps)  # 4
        motor.set_step_mode("half")
        motor.move_stepper(8, "forward", delay=0.3)
        print("half  -> total_steps:", motor.total_steps)  # 12
        motor.set_step_mode("micro", 4)
        motor.move_stepper(16, "backward", delay=0.1)
        print("micro -> total_steps:", motor.total_steps)  # -4

        for bad in [0, -3, 2.5]:
            try:
                motor.generate_microstep_sequence(bad)
                print(bad, "was NOT rejected")
            except ValueError:
                print(bad, "was rejected")

    else:
        print("Unknown TEST number")

finally:
    motor.stop()
    print("All outputs off.")
