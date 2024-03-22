class PID:
    def __init__(self, kp, ki, kd, max):
        self.__kp = kp
        self.__ki = ki
        self.__kd = kd
        self.__max = max
        self.__integral = 0
        self.__last_error = 0

    def compute(self, actual, setpoint, dt):
        error = setpoint - actual
        derivative = (error - self.__last_error) / dt
        self.__last_error = error

        output = (
            (self.__kp * error)
            + (self.__ki * self.__integral)
            + (self.__kd * derivative)
        )

        if abs(output) > self.__max and (
            (error > 0 and self.__integral > 0) or (error < 0 and self.__integral < 0)
        ):
            self.__integral = self.__integral
        else:
            self.__integral += error * dt

        return output if output < self.__max else self.__max
