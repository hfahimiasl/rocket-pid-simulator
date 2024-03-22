import time
import turtle

from rocket import Rocket
from pid import PID
from plotter import Plotter


class SimulationConfig:
    ScreenWidth = 402
    ScreenHeight = 720
    Setpoint = 0
    DT = None


class RocketConfig:
    Mass = 1
    MarkerSize = 20


class PIDConfig:
    Ku = 1.675
    Tu = 30

    ## Tuning
    # Kp = Ku
    # Ki = 0
    # Kd = 0

    ## Orginal
    Kp = 0.335
    Ki = 0.018853
    Kd = 0.79

    ## Classic PID
    # Kp = Ku * 0.6
    # Ki = Ku * 1.2 / Tu
    # Kd = Ku * 0.075 * Tu

    ## Pessen Integral Rule
    # Kp = Ku * 0.7
    # Ki = Ku * 1.75 / Tu
    # Kd = Ku * 0.105 * Tu

    ## Some Overshoot
    # Kp = Ku * 0.33
    # Ki = Ku * 0.66 / Tu
    # Kd = Ku * 0.11 * Tu

    ## No Overshoot
    # Kp = Ku * 0.2
    # Ki = Ku * 0.4 / Tu
    # Kd = Ku * 0.066 * Tu

    Max = 15


class Simulation:
    def __init__(self):
        self.__screen = turtle.Screen()
        self.__screen._root.protocol("WM_DELETE_WINDOW", self.__quit)
        self.__screen.setup(SimulationConfig.ScreenWidth, SimulationConfig.ScreenHeight)
        self.__turtle = turtle.Turtle()

        self.__rocket = Rocket(
            RocketConfig.Mass,
            RocketConfig.MarkerSize - (SimulationConfig.ScreenHeight / 2),
        )

        self.__pid = PID(
            PIDConfig.Kp,
            PIDConfig.Ki,
            PIDConfig.Kd,
            PIDConfig.Max,
        )

        self.__plotter = Plotter(
            Plotter.Item("Acceleration (m/s^2)", "tab:blue"),
            Plotter.Item("Velocity (m/s)", "tab:orange"),
            Plotter.Item("Altitude (m)", "tab:green"),
            Plotter.Item("Thrust (N)", "tab:red"),
        )

        self.__setpoint()

    def __quit(self):
        self.__running = False
        self.__screen._root.after(100, self.__screen._root.destroy)

    def __setpoint(self, space=10):
        self.__turtle.hideturtle()
        self.__turtle.penup()
        self.__turtle.goto(
            -int(self.__screen.window_width() / 2), SimulationConfig.Setpoint
        )
        self.__turtle.color("red")

        for _ in range(0, self.__screen.window_width(), space * 2):
            self.__turtle.penup()
            self.__turtle.forward(space)
            self.__turtle.pendown()
            self.__turtle.forward(space)

    def __render(self, dt):
        thrust = self.__pid.compute(
            self.__rocket.altitude, SimulationConfig.Setpoint, dt
        )
        self.__rocket.update(thrust, dt)
        self.__plotter.append(
            self.__rocket.acceleration,
            self.__rocket.velocity,
            self.__rocket.altitude,
            thrust,
        )

    def run(self):
        last = time.time()
        self.__running = True

        while self.__running:
            now = time.time()
            self.__render(SimulationConfig.DT if SimulationConfig.DT else now - last)
            last = now

        self.__screen.mainloop()
        self.__plotter.draw()


sim = Simulation()
sim.run()
