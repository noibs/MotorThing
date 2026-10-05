# Name: Elliott Hartmann Ulriksen
# Email: elulr26@student.sdu.dk

from stepper_motor import StepperMotor

motor = StepperMotor([16, 17, 18, 19], pwm_pct=0.5)
motor.set_step_mode("full")

"""Move stepper test"""
motor.move_stepper(8, "forward", delay=0.3)
print("total_steps:", motor.total_steps)    # expect 8

motor.move_stepper(8, "backward", delay=0.3)
print("total_steps:", motor.total_steps)    # expect 0


"""Continuous test
motor.rotate_continuous("forward", delay=0.2)
print("After continuous:", motor.total_steps)
"""

"""Half step test
motor = StepperMotor([16, 17, 18, 19], pwm_pct=0.5)
motor.set_step_mode("half")

try:
    for pct in [0.25, 0.5, 1.0]:
        motor.pwm_pct = pct
        print("PWM =", int(pct * 100), "%")

        print("  forward")
        motor.move_stepper(8, "forward", delay=0.4)      # all 8 states
        print("  total_steps:", motor.total_steps)

        print("  backward")
        motor.move_stepper(8, "backward", delay=0.4)     # all 8 in reverse
        print("  total_steps:", motor.total_steps)

        time.sleep(1)    # pause between settings
finally:
    motor.stop()
"""

"""Switch between full/half test
motor.set_step_mode("full")
motor.move_stepper(4, "forward", delay=0.4)
motor.set_step_mode("half")
motor.move_stepper(8, "forward", delay=0.4)
print(motor.total_steps)    # 4 + 8 = 12 more than beforeL
"""

motor.stop()
