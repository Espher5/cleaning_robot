import mock.GPIO as GPIO
from CleaningRobotError import CleaningRobotError


class CleaningRobot:
    BATTERY_PIN = 11  # IBS pin
    RECHARGE_LED_PIN = 12
    CLEANING_SYSTEM_PIN = 13
    INFRARED_PIN = 15

    # Wheel motor pins
    PWMA = 16
    AIN2 = 18
    AIN1 = 22
    # Rotation motor pins
    BIN1 = 29
    BIN2 = 31
    PWMB = 32
    STBY = 33

    N = 'N'
    S = 'S'
    E = 'E'
    W = 'W'

    LEFT = 'l'
    RIGHT = 'r'
    FORWARD = 'f'

    def __init__(self, room_x: int, room_y: int):
        """
        Constructor
        :param room_x: the x size of the room (i.e., how many cells are on the x-axis of the grid)
        :parma room_y: the y size of the room (i.e., how many cells are on the y-axis of the grid)
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.INFRARED_PIN, GPIO.IN)
        GPIO.setup(self.BATTERY_PIN, GPIO.IN)
        GPIO.setup(self.RECHARGE_LED_PIN, GPIO.OUT)
        GPIO.setup(self.CLEANING_SYSTEM_PIN, GPIO.OUT)

        GPIO.setup(self.PWMA, GPIO.OUT)
        GPIO.setup(self.AIN2, GPIO.OUT)
        GPIO.setup(self.AIN1, GPIO.OUT)
        GPIO.setup(self.PWMB, GPIO.OUT)
        GPIO.setup(self.BIN2, GPIO.OUT)
        GPIO.setup(self.BIN1, GPIO.OUT)
        GPIO.setup(self.STBY, GPIO.OUT)

        self.room_x = room_x
        self.room_y = room_y
        self.obstacle = None
        self.pos_x = None
        self.pos_y = None
        self.facing = None

        self.battery_led_on = False
        self.cleaning_system_on = False

    def initialize_robot(self) -> None:
        """
        Initializes the robot in the starting position (0,0,N)
        """
        pass

    def robot_status(self) -> str:
        """
        Returns the current status of the robot, as well as any obstacle encountered
        :return: the status of the robot as a string
        """
        pass

    def execute_command(self, command: str) -> str:
        """
        It makes the robot move inside the room according to a command string received by the RMS.
        The return string contains the new position of the robot, its direction, and the obstacles it has
        encountered while moving in the room (if any).
        :param command: the string containing the command corresponding to the action the robot needs to perform.
            The command can be:
            - f for moving forward one cell in the room.
            - r for turning right 90 degrees.
            - l for turning left 90 degrees.
        :return: The string that contains the updated position and direction of the
            robot, and the obstacle the rover has encountered while moving inside the room (if any).
            The return string (without white spaces) has the following format:
            "(x,y,dir)(o_x,o_y)".
            x and y define the new position of the rover while dir represents its direction (i.e., N, S, W, or E).
            Finally, o_x and o_y are the coordinates of the encountered obstacle.
        """
        pass

    def obstacle_found(self) -> bool:
        """
        Checks whether the infrared distance sensor has detected an obstacle in front of it.
        :return: True if the infrared sensor detects something, False otherwise.
        """

    def manage_battery(self) -> None:
        """
        It  checks how much battery is left by querying the IBS.
        If the capacity returned by the IBS is equal to or less than 10%,
        the robot turns on the recharging led and shuts off the cleaning system.
        Otherwise, the robot turns on the cleaning system and turns off the recharge LED.
        """
        pass

    def activate_wheel_motor(self) -> None:
        """
        Makes the robot move forward by activating its wheel motor
        """
        # Drive the motor clockwise
        GPIO.output(self.AIN1, GPIO.HIGH)
        GPIO.output(self.AIN2, GPIO.LOW)
        # Set the motor speed
        GPIO.output(self.PWMA, GPIO.HIGH)
        # Disable STBY
        GPIO.output(self.STBY, GPIO.HIGH)

        # Usually you would wait for the motor to actually move
        # For the sake of testing keep this commented
        # time.sleep(5)

        # Stop the motor
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.PWMA, GPIO.LOW)
        GPIO.output(self.STBY, GPIO.LOW)

    def activate_rotation_motor(self, direction) -> None:
        """
        Makes the body of the robot rotate in the direction corresponding to the received parameter
        :param direction: "l" to turn left, "r" to turn right
        """
        if direction == self.LEFT:
            GPIO.output(self.BIN1, GPIO.HIGH)
            GPIO.output(self.BIN2, GPIO.LOW)
        elif direction == self.RIGHT:
            GPIO.output(self.BIN1, GPIO.LOW)
            GPIO.output(self.BIN2, GPIO.HIGH)

        GPIO.output(self.PWMB, GPIO.HIGH)
        GPIO.output(self.STBY, GPIO.HIGH)

        # Usually you would wait for the motor to actually move
        # For the sake of testing keep this commented
        # time.sleep(5)

        # Stop the motor
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)
        GPIO.output(self.PWMB, GPIO.LOW)
        GPIO.output(self.STBY, GPIO.LOW)