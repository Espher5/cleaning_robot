import mock.GPIO as GPIO
from CleaningRobotError import CleaningRobotError


class CleaningRobot:
    INFRARED_PIN =11
    BATTERY_PIN = 12
    RECHARGE_LED_PIN = 13
    CLEANING_SYSTEM_PIN = 15

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
        self.obstacles = []
        self.pos_x = None
        self.pos_y = None
        self.facing = None

        self.battery_led_on = False
        self.cleaning_system_on = False

    def robot_status(self) -> str:
        """
        Returns the current status of the robot, as well as any obstacle encountered
        :return: the status of the robot as a string
        """
        status_string = '(' + str(self.pos_x) + ',' + str(self.pos_y) + ',' + self.facing + ')'
        if len(self.obstacles) > 0:
            for ob in self.obstacles:
                status_string += ob

        return status_string

    def add_obstacle(self, ob_x: int, ob_y: int) -> None:
        """
        Adds an obstacles to the list of encountered obstacles
        :param ob_x: the x coordinate of the obstacle
        :param ob_y: the y coordinate of the obstacle
        """
        self.obstacles.append('(' + str(ob_x) + ',' + str(ob_y) + ')')

    def initialize_robot(self) -> None:
        """
        Initializes the robot in the starting position (0,0,N)
        """
        pass

    def execute_command(self, command_string: str) -> str:
        """
        It makes the robot move inside the room according to a command string received by the RMS.
        The return string contains the new position of the rover, its direction, and the obstacles it has
         encountered while moving in the planet (if any).
        :param command_string: the string containing the list of commands to be performed by the robot.
            The commands can be:
            - f for moving forward one cell in the room.
            - r for turning right 90 degrees.
            - l for turning left 90 degrees.
        :return: The return string that contains the updated position and direction of the
            rover, and the obstacles the rover has encountered while moving inside the room (if any).
            The return string (without white spaces) has the following format:
            "(x,y,dir)(o1_x,o1_y)(o2_x,o2_y)...(on_x,on_y)".
            x and y define the new position of the rover while dir represents its direction (i.e., N, S, W, or E).
            Finally, oi_x and oi_y are the coordinates of the i-th encountered obstacle.
        """
        pass

    def obstacle_found(self) -> bool:
        """
        Checks whether the infrared distance sensor detects an obstacle in front of it.
        :return: True if the infrared sensor detects something, False otherwise.
        """

    def manage_battery(self) -> None:
        """
        User story 2: When the robot is turned on, it first checks how much battery is left by querying the IBS.
        If the capacity returned by the IBS is equal to or less than 10%, the robot turns on the recharging led.
        Otherwise, the robot turns on the cleaning system and sends its status to the RMS.

        User story 5: When the robot enters a cell, it checks how much battery is left by querying the IBS.
        When the capacity returned by the IBS is equal to or less than 10%, the robot shuts down the cleaning system,
        turns on the recharging led, and stands still.
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