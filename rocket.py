import scipy
import turtle


class Rocket:
    def __init__(self, mass, ground):
        self.__mass = mass
        self.__altitude = ground
        self.__acceleration = 0
        self.__velocity = 0
        self.__turtle = turtle.Turtle()
        self.__turtle.hideturtle()
        self.__turtle.color("black")
        self.__turtle.left(90)
        self.__turtle.penup()
        self.__turtle.speed(0)
        self.__turtle.sety(ground)
        self.__turtle.showturtle()

    def update(self, thrust, dt):
        self.__acceleration = (thrust / self.__mass) - scipy.constants.g
        self.__velocity += self.__acceleration * dt
        self.__altitude += self.__velocity * dt
        self.__turtle.sety(self.__altitude)

    @property
    def acceleration(self):
        return self.__acceleration

    @property
    def velocity(self):
        return self.__velocity

    @property
    def altitude(self):
        return self.__turtle.ycor()
