# Name: Elliott Hartmann Ulriksen
# Email: elulr26@student.sdu.dk

from stepper_motor import StepperMotor

ledPins = [16, 17, 18, 19]
motorPins = [0, 1, 2, 3]

motor = StepperMotor(ledPins, pwm_pct=0.65, frequency=18_000)

try:
    # Half step: 400 half steps. full turn
    motor.set_step_mode("half")
    motor.move_stepper(400, "forward", delay=0.02)
    print("After half step:", motor.total_steps)

    # Microstep. 1600 step.  full turn
    motor.set_step_mode("micro", 8)
    motor.move_stepper(1600, "backward", delay=0.002)
    print("After microstep:", motor.total_steps)

    # Full step: 200 full steps. full turn
    motor.set_step_mode("full")
    motor.move_stepper(200, "forward", delay=0.01)
    print("After full step:", motor.total_steps)

    # Continuous rotation
    motor.rotate_continuous("forward", delay=0.01)

finally:
    motor.stop()
