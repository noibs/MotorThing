from stepper_motor import StepperMotor


def main():
    motor = StepperMotor([16, 17, 18, 19], pwm_pct=0.15, frequency=18_000)
    motor.set_step_mode("half")
    motor.move_stepper(50, "forward", delay=1)
    motor.stop()

if __name__ == "__main__":
    main()
