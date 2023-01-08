# -*- coding: utf-8 -*-
"""
________________TITLE________________
PHYS20161 - Assignment 1 - Bouncy Ball
-------------------------------------
This python script calculates the number of bounces above a certain height and
the time it takes for these bounces.
The average speed and distance travelled by the ball can also be found if the
user wishes. The function requires three initial conditions:

1) Initial height the ball is dropped from.
2) Minimum height the ball should bounce above.
3) efficiency

If one of these initial conditions provided is not physical an error meassage
will be printed.

Last Updated: 24/10/2020
@author: J. Sharma UID: 10304831
"""
# CONSTANTS

ACCELERATION = 9.81  # m/s^2

# FUNCTIONS


def total_time(initial_height, minimum_height, efficiency):
    """
    Calculates the total time elapsed for a falling bouncy ball above a
    specified minimum height. Heights are in meters. The time is returned in s.

    Args:
        initial_height : FLOAT
        minimum_height : FLOAT
        efficiency : FLOAT
    Returns:
        time: [FLOAT]

    J.Sharma 24/10/2020
    """

    time = ((2 * initial_height / ACCELERATION) ** 0.5)

    while initial_height > minimum_height:
        initial_height *= efficiency

        if initial_height > minimum_height:
            time = time + ((2 * initial_height / ACCELERATION) ** 0.5) * 2

    return time


def total_distance(initial_height, minimum_height, efficiency):
    """
    Calculates the total distance travelled for a falling bouncy ball above a
    specified minimum height. Heights are in meters. The distance is returned
    in m.

    Args:
        initial_height : FLOAT
        minimum_height : FLOAT
        efficiency : FLOAT
    Returns:
        distance: [FLOAT]

    J.Sharma 24/10/2020
    """
    distance = initial_height

    while initial_height > minimum_height:
        initial_height *= efficiency

        if initial_height > minimum_height:
            distance += 2 * initial_height

    return distance


def total_bounces(initial_height, minimum_height, efficiency):
    """
    Calculates the total number of bounces for a falling bouncy ball above a
    specified minimum height. Heights are in meters.

    Args:
        initial_height : FLOAT
        minimum_height : FLOAT
        efficiency : FLOAT
    Returns:
        bounces: [int]

    J.Sharma 24/10/2020
    """
    bounces = 0

    while initial_height > minimum_height:
        initial_height *= efficiency

        if initial_height > minimum_height:
            bounces += 1

    return bounces


def average_speed(time, distance):
    """
    Calculates the average speed. Distance is in metres and the time is in s.
    The average speed is retuned in m/s.

    Args:
        time : FLOAT
        distance : FLOAT
    Returns:
        distance/time : [FLOAT]

    J.Sharma 24/10/2020
    """
    return distance/time


def bouncy_ball(initial_height, minimum_height, efficiency):
    """
    If the number of bounces is greater than zero the user is asked if they
    would like to see the total distance and average speed of the bouncy ball.
    If the user types yes to both of these questions their values will be
    printed to 2.D.P. The time elapsed and number of bounces is also printed.

    Args:
        initial_height : FLOAT
        minimum_height : FLOAT
        efficiency : FLOAT
    Returns:

    J.Sharma 24/10/2020
    """

    time = total_time(initial_height, minimum_height, efficiency)

    distance = total_distance(initial_height, minimum_height, efficiency)

    bounces = total_bounces(initial_height, minimum_height, efficiency)

    speed = average_speed(time, distance)

    if bounces > 0:
        speed_question = input('Do you want to calculate the average speed the\
                           ball has traveled? (YES or NO) ').upper()
        distance_question = input('Do you want to calculate the total distance\
                                  the ball traveled? (YES or NO) ').upper()

        if distance_question == 'YES':
            print('The distance the\
 ball travelled is: {0:0.2f} m'.format(distance))

        if speed_question == 'YES':
            print('The average speed: {0:0.2f} m/s'.format(speed))
            print('The time it took for', bounces,
                  'bounces: {0:0.2f} s'.format(time))
            print('The number of bounces is', bounces)

    else:
        print('There were 0 bounces')


def initial_conditions_checker(initial_height, minimum_height, efficiency):
    """
    Checks the conditions of initial height, minimum height and efficiency are
    usable. If they are not an error message will be printed.

    The boundary conditions:
        1) initial_height >= minimum height
        2) 0 < efficiency <= 1

    Args:
        initial_height : FLOAT
        minimum_height : FLOAT
        efficiency : FLOAT

    J.Sharma 24/10/2020
    """

    if initial_height >= minimum_height and 0 < efficiency <= 1:

        if initial_height == minimum_height:
            print('The ball will not bounce')

        elif efficiency == 1:
            print('The ball will bounce forever')

        else:
            bouncy_ball(initial_height, minimum_height, efficiency)

    elif initial_height < minimum_height and \
            (efficiency >= 1 or efficiency <= 0):
        print('None of the boundary conditions are met')

    elif efficiency >= 1 or efficiency <= 0:
        print('The efficiency doesnt satisfy the boundary conditions.')

    else:
        print('The heights do not satisfy the boundary conditions.')

# MAIN CODE


INITIAL_HEIGHT = float(input('What is the intial height in m? '))


MINIMUM_HEIGHT = float(input('What is the minimum height in m? '))


EFFICIENCY = float(input('What is the efficiency? '))


initial_conditions_checker(INITIAL_HEIGHT, MINIMUM_HEIGHT, EFFICIENCY)



