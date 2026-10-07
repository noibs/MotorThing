# Name: Elliott Hartmann Ulriksen
# Email: elulr26@student.sdu.dk

from stepper_motor import StepperMotor

motor = StepperMotor([0, 1, 2, 3], pwm_pct=0.5, frequency=18_000)

try:
    # Half step: 400 half steps = one full turn forward
    motor.set_step_mode("half")
    motor.move_stepper(400, "forward", delay=0.01)
    print("After half step:", motor.total_steps)

    # Microstep with 8 microsteps per full step: 1600 steps = one full turn back
    motor.set_step_mode("micro", 8)
    motor.move_stepper(1600, "backward", delay=0.002)
    print("After microstep:", motor.total_steps)

    # Full step: 200 full steps = one full turn forward
    motor.set_step_mode("full")
    motor.move_stepper(200, "forward", delay=0.01)
    print("After full step:", motor.total_steps)

    # Continuous rotation until Ctrl+C
    motor.rotate_continuous("forward", delay=0.01)

finally:
    motor.stop()
