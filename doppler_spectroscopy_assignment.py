# -*- coding: utf-8 -*-
"""
________________TITLE__________________________
PHYS20161 - Assignment 2 - Doppler Spectroscopy
-----------------------------------------------
This python script reads in two seperate data files and combines them. The star
velocity (Vs) is then found. Outliers are removed. A minimisation of the chi
squared is performed and values of speed of the star (V0), angular speed (w)
and phase are found. From these values the planets distance from the star (r),
the velocity of the planet (Vp) and the mass of the planet (Mp) can also be
found. All values have a calculated uncertainty. Plots of the raw data, fitted
data and a contour plot are produced.

Last Updated: 16/12/2020
@author: J. Sharma UID: 10304831
"""
# IMPORT STATEMENTS

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import scipy.constants as pc
from scipy.optimize import fmin

# CONSTANTS


DATA_FILE_1 = 'doppler_data_1.csv'
DATA_FILE_2 = 'doppler_data_2.csv'
SPEED_OF_LIGHT_VACUMN = pc.speed_of_light  # m/s
EMITTED_WAVELENGHT = 656.281 * 10**-9  # m
GRAVITATIONAL_CONSTANT = pc.G  # Nm^2/kg^2
MASS_OF_STAR = 2.78 * 1.989 * 10**30  # Kg
PHASE_START = 3  # rad
SPEED_STAR_START = 50  # m/s
ANGULAR_SPEED_START = 3 * 10**-8  # rad/s
X_VALUES_SHIFT_CONTOUR_PLOT = 3  # m/s
Y_VALUES_SHIFT_CONTOUR_PLOT = 1 * 10**-9  # rad/s
NUMBER_OF_POINTS_CONTOUR_PLOT = 500
MINIMUM_CHI_SQUARED_OFFSET_1 = 1
MINIMUM_CHI_SQUARED_OFFSET_2 = 2.3
MINIMUM_CHI_SQUARED_OFFSET_3 = 5.99
MINIMUM_CHI_SQUARED_OFFSET_4 = 9.21
YEARS_TO_SECONDS_CONVERSION = 3.154 * 10**7
NANOMETERS_TO_METERS_CONVERSION = 10**-9
METERS_TO_AU_CONVERSION = pc.au
KILOGRAMS_TO_JOVIAN_MASS_CONVERSION = 1.8986 * 10**27

# FUNCTIONS


def is_float(entry):
    """
    Checks if the entry is a float.

    Parameters
    ----------
    entry : float

    Returns
    -------
    bool


    """
    try:
        float(entry)
        return True
    except ValueError:
        return False


def file_check(filename):
    """
    Checks if file is in directory.

    Parameters
    ----------
    filename : string

    Returns
    -------
    bool
    """
    try:
        file = open(filename, 'r')
        file.close()
        return True
    except FileNotFoundError:
        print("'{0:s}' not found. Please check directory.".format(filename))
        return False


def read_data(filename):
    """
    Reads in date file, removing non-numeric values, and outputs data in
    arrays.

    Parameters
    ----------
    filename : string

    Returns
    -------
    data_array : numpy array
    """
    data_array = np.genfromtxt(filename, delimiter=',')
    data_array = data_array[~np.isnan(data_array).any(axis=1)]
    data_array = data_array[data_array[:, 2] != 0, :]

    return data_array


def star_velocity_calculator(observed_wavelenght):
    """
    Calculates the star velocity given the observed wavelenght.

    Parameters
    ----------
    observed_wavelenght : float
        meters.

    Returns
    -------
    star velocity: float
        meters / second

    """
    return SPEED_OF_LIGHT_VACUMN * (((observed_wavelenght) /
                                     (EMITTED_WAVELENGHT)) - 1)


def star_velocity(speed_star, angular_speed, phase, time):
    """
    Calculates the star velocity given the magnitude of the star velocity,
    angular speed, phase and time.

    Parameters
    ----------
    speed_star : float
        meters / second
    angular_speed : float
        rad / second
    phase : float
        rad
    time : float
        seconds

    Returns
    -------
    star velocity: float
        meters / second

    """
    return speed_star * np.sin((angular_speed * time) + phase)


def planet_distance_from_star_calculator(angular_speed):
    """
    Calculates the planets distance from the star given the angular speed.

    Parameters
    ----------
    angular_speed : float
        rad / second

    Returns
    -------
    planets distance from the star : float
        meters

    """
    return np.cbrt((GRAVITATIONAL_CONSTANT * MASS_OF_STAR) /
                   (angular_speed**2))


def velocity_of_planet_calculator(planet_distance):
    """
    Calculates the velocity of the planet given the planets distance from the
    star.

    Parameters
    ----------
    planet_distance : float
        meters

    Returns
    -------
    velocity of the planet : float
        meters / second

    """
    return np.sqrt((GRAVITATIONAL_CONSTANT * MASS_OF_STAR) / (planet_distance))


def mass_of_planet_calculator(speed_star, velocity_of_planet):
    """
    Calculates the mass of the planet given the magnitue of the star velocity
    and the velocity of the planet.

    Parameters
    ----------
    speed_star : float
        meters / second
    velocity_of_planet : float
        meters / second

    Returns
    -------
    mass of the planet : float
        kilograms

    """
    return (MASS_OF_STAR * speed_star) / velocity_of_planet


def minimisation(data, number_of_variables, phase=None):
    """
    Minimises the chi-squared of the star velocity with respect to two or
    three variables.

    Parameters
    ----------
    data : list
    number_of_variables : int
        Use 2 or 3 to minimise with respect to two or three variables
        respectively.
    phase : float
        The default is None.

    Returns
    -------
    fit : tuple

    """
    if number_of_variables == 3:
        fit = fmin(lambda x: chi_squared_calculator(star_velocity(
            x[0], x[1], x[2], data[0]), data[1], data[2]),
                   [SPEED_STAR_START,
                    ANGULAR_SPEED_START,
                    PHASE_START], full_output=True)

    if number_of_variables == 2:
        fit = fmin(lambda x: chi_squared_calculator(star_velocity(
            x[0], x[1], phase, data[0]), data[1], data[2]),
                   [SPEED_STAR_START,
                    ANGULAR_SPEED_START], full_output=True)

    return fit


def remove_outliers_1(data, number_of_standard_deviations):
    """
    Removes outliers from some data set that are more than a number of standard
    deviations away from the mean.

    Parameters
    ----------
    data : numpy array of floats
    number_of_standard_deviations : int
        sets the tolerance

    Returns
    -------
    data_first_cleaning : numpy array

    """
    index = 0
    idx = []
    means = np.mean(data, 0)[1]
    standard_deviation = np.std(data, 0)[1]
    for line in data[:, 1]:
        if line < means - (number_of_standard_deviations *
                           standard_deviation) or\
                line > means + (number_of_standard_deviations *
                                standard_deviation):
            idx.append(index)
        index += 1
    data_first_cleaning = np.delete(data, idx, axis=0)

    return data_first_cleaning


def remove_outliers_2(data, number_of_standard_deviations,
                      speed_star, angular_speed, phase):
    """
    Removes data points that are far away from the line of best fit. This must
    be run after points that are far away from the mean are removed.

    Parameters
    ----------
    data : numpy array of floats
    number_of_standard_deviations : int
        sets the tolerance
    speed_star : numpy float64
    angular_speed : numpy float64
    phase : numpy float64

    Returns
    -------
    data_second_cleaning : numpy array

    """

    standard_deviation = np.std(data[:, 1], ddof=1)
    rows_with_errors = []

    for line in range(len(data[:])):

        if (abs(data[:, 1][line] - star_velocity(speed_star,
                                                 angular_speed,
                                                 phase,
                                                 data[:, 0][line])) >
                (number_of_standard_deviations * standard_deviation)):
            rows_with_errors.append(line)
    data_second_cleaning = np.delete(data, rows_with_errors, 0)
    if rows_with_errors == []:
        print('No data was removed')

    return data_second_cleaning


def plot_raw_data(data, name_of_saved_file):
    """
    Plots the raw data. Allows the user to choose a name for the saved plot.

    Parameters
    ----------
    data : numpy array of floats
    name_of_saved_file : string

    Returns
    -------
    plt.show()
        shows the plot of the data

    """
    raw_data_figure = plt.figure(figsize=(10, 4))
    raw_data_plot = raw_data_figure.add_subplot(111)
    raw_data_plot.set_title('Raw data - wavelenght against time',
                            fontname='Times New Roman', fontsize=20)
    raw_data_plot.set_xlabel('Time (years)', fontname='Times New Roman',
                             fontsize=15)
    raw_data_plot.set_ylabel('Wavelenght (nm)', fontname='Times New Roman',
                             fontsize=15)
    raw_data_plot.errorbar(data[:, 0], data[:, 1],
                           yerr=data[:, 2], fmt='o',
                           label='Raw data points')
    raw_data_plot.yaxis.\
        set_major_formatter(mtick.FormatStrFormatter('%.7e'))
    raw_data_plot.xaxis.\
        set_major_formatter(mtick.FormatStrFormatter('%.1f'))
    plt.legend(loc=4)
    plt.tight_layout()
    plt.savefig(name_of_saved_file, dpi=300)
    return plt.show()


def plot_fitted_data(name_of_saved_file, fitted_parameters,
                     minimum_chi_squared, data, phase):
    """
    Plots the data with the minimum chi squared value
    dispalyed.

    Parameters
    ----------
    name_of_saved_file : string
    fitted_parameters : numpy array
    minimum_chi_squared : float
    data : numpy array
    phase : float
        rad

    Returns
    -------
    plt.show()
        shows the plot of the data

    """
    fitted_data_figure = plt.figure(figsize=(11, 4))
    fitted_data_plot = fitted_data_figure.add_subplot(111)

    fitted_data_plot.set_title((r'Fitted data. '
                                ' Magnitude of star velocity / $v_0$ (m/s)'
                                ' = {0:3.2f},'
                                r' Angular speed / $\omega$ (rad/s)'
                                ' = {1:3.3e}.').
                               format(fitted_parameters[0],
                                      fitted_parameters[1]) +
                               r' $\chi^2_{{\mathrm{{red.}}}} = $ {0:3.2f}'.
                               format(minimum_chi_squared /
                                      (len(data) - 2)),
                               fontname='Times New Roman', fontsize=17)
    fitted_data_plot.set_xlabel('Time/ t (s)', fontname='Times New Roman',
                                fontsize=15)
    fitted_data_plot.set_ylabel('Star velocity /$v_s$ (m/s)',
                                fontname='Times New Roman', fontsize=17)

    fitted_data_plot.plot(data[:, 0],
                          star_velocity(fitted_parameters[0],
                                        fitted_parameters[1],
                                        phase,
                                        data[:, 0]),
                          label='Line of best fit')
    fitted_data_plot.errorbar(data[:, 0],
                              data[:, 1],
                              yerr=data[:, 2], fmt='o',
                              label='data points')
    fitted_data_plot.yaxis.\
        set_major_formatter(mtick.FormatStrFormatter('%.1f'))
    fitted_data_plot.xaxis.\
        set_major_formatter(mtick.FormatStrFormatter('%.2e'))
    plt.legend(loc=4)
    plt.tight_layout()
    plt.savefig(name_of_saved_file, dpi=450)
    return plt.show()


def chi_squared_calculator(prediction, data, uncertainty):
    """
    Returns chi squared.

    Parameters
    ----------
    prediction : numpy array
    data : numpy array 
    uncertainty : numpy array 

    Returns
    -------
    chi_squared : float
    """
    chi_squared = np.sum(((prediction - data) / uncertainty)**2)
    return chi_squared


def chi_squared_for_plot(a_parameter, b_parameter, data, phase):
    """
    Returns chi squared for a pre defined function depenedent on one
    variable, x, with two parameters, a & b.
    Data is a 2D array composed of rows of [x values, f(x) values and
    uncertainties]

    Parameters
    ----------
    a_parameter : (float)
    b_parameter : (float)
    data : ([float, float, float])
    phase : float
        rad

    Returns
    -------
    chi_square : numpy array

    """
    chi_square = 0
    for entry in data:
        chi_square += (((star_velocity(a_parameter, b_parameter, phase,
                                       entry[0])
                         - entry[1]) / entry[2])**2)
    return chi_square


def mesh_arrays(x_array, y_array):
    """
    Returns two meshed arrays of size len(x_array)

    Parameters
    ----------
    x_array : array[floats]
    y_array : array[floats]

    Returns
    -------
    x_array_mesh : numpy array
    y_array_mesh : numpy array

    """

    x_array_mesh = np.empty((0, len(x_array)))

    for dummy in range(len(y_array)):
        x_array_mesh = np.vstack((x_array_mesh, x_array))

    y_array_mesh = np.empty((0, len(y_array)))

    for dummy in range(len(x_array)):
        y_array_mesh = np.vstack((y_array_mesh, y_array))

    y_array_mesh = np.transpose(y_array_mesh)

    return x_array_mesh, y_array_mesh


def contour_plot_function(fitted_parameters, data, minimum_chi_squared, phase):
    """
    Generates a contour plot of the minimum chi squared along with the minimum
    chi squared +1, +2.3, +5.99, +9.21. The minimum chi squared +1 is also
    produced seperately saved in the same file.

    Parameters
    ----------
    fitted_parameters : numpy array
    data : numpy array
    minimum_chi_squared : float
    phase : float
        rad

    Returns
    -------
    plt.show()
        shows the plot of the data
    parameters_contour_plot : numpy array
    """

    x_values = np.linspace(fitted_parameters[0] - X_VALUES_SHIFT_CONTOUR_PLOT,
                           fitted_parameters[0] + X_VALUES_SHIFT_CONTOUR_PLOT,
                           NUMBER_OF_POINTS_CONTOUR_PLOT)
    y_values = np.linspace(fitted_parameters[1] - Y_VALUES_SHIFT_CONTOUR_PLOT,
                           fitted_parameters[1] + Y_VALUES_SHIFT_CONTOUR_PLOT,
                           NUMBER_OF_POINTS_CONTOUR_PLOT)

    x_mesh, y_mesh = mesh_arrays(x_values, y_values)

    parameters_contour_figure = plt.figure(figsize=(7.9, 7.2))

    parameters_contour_plot = parameters_contour_figure.add_subplot(212)

    parameters_contour_plot.set_title(r'$\chi^2$ contours against parameters.',
                                      fontsize=14)
    parameters_contour_plot.set_xlabel(('Magnitude of star velocity / $v_0$'
                                        ' (m/s)'), fontsize=14)
    parameters_contour_plot.set_ylabel(r'Angular speed / $\omega$ (rad/s)',
                                       fontsize=14)
    parameters_contour_plot.yaxis.set_major_formatter(mtick.
                                                      FormatStrFormatter
                                                      ('%.3e'))

    parameters_contour_plot.scatter(fitted_parameters[0], fitted_parameters[1],
                                    label='Minimum')

    parameters_contour_plot.\
        contour(x_mesh,
                y_mesh,
                chi_squared_for_plot(x_mesh,
                                     y_mesh,
                                     data, phase),
                levels=[minimum_chi_squared + MINIMUM_CHI_SQUARED_OFFSET_1],
                linestyles='dashed',
                colors='k')

    chi_squared_levels = (minimum_chi_squared + MINIMUM_CHI_SQUARED_OFFSET_2,
                          minimum_chi_squared + MINIMUM_CHI_SQUARED_OFFSET_3,
                          minimum_chi_squared + MINIMUM_CHI_SQUARED_OFFSET_4)

    contour_plot = parameters_contour_plot.\
        contour(x_mesh,
                y_mesh,
                chi_squared_for_plot(x_mesh,
                                     y_mesh,
                                     data, phase),
                levels=chi_squared_levels)
    labels = ['Minimum', r'$\chi^2_{{\mathrm{{min.}}}}+1.00$',
              r'$\chi^2_{{\mathrm{{min.}}}}+2.30$',
              r'$\chi^2_{{\mathrm{{min.}}}}+5.99$',
              r'$\chi^2_{{\mathrm{{min.}}}}+9.21$']

    parameters_contour_plot.clabel(contour_plot)

    box = parameters_contour_plot.get_position()
    parameters_contour_plot.set_position([box.x0, box.y0, box.width,
                                          box.height])

    for index, label in enumerate(labels):
        parameters_contour_plot.collections[index].set_label(label)
    parameters_contour_plot.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                                   fontsize=14)

    # Chi squared plot for minimum chi squared + 1

    parameters_contour_plot = parameters_contour_figure.add_subplot(211)

    parameters_contour_plot.set_title(
        r'$\chi^2 + 1$ contour against parameters.',
        fontsize=14)
    parameters_contour_plot.set_xlabel(('Magnitude of star velocity'
                                        '/ $v_0$ (m/s)'), fontsize=14)
    parameters_contour_plot.set_ylabel((r'Angular speed/ $\omega$ (rad/s)'),
                                       fontsize=14)
    parameters_contour_plot.yaxis.set_major_formatter(mtick.
                                                      FormatStrFormatter
                                                      ('%.3e'))

    parameters_contour_plot.scatter(fitted_parameters[0], fitted_parameters[1],
                                    label='Minimum')

    parameters_contour_plot.\
        contour(x_mesh,
                y_mesh,
                chi_squared_for_plot(x_mesh,
                                     y_mesh,
                                     data, phase),
                levels=[minimum_chi_squared + MINIMUM_CHI_SQUARED_OFFSET_1],
                linestyles='dashed',
                colors='k')

    parameters_contour_plot.clabel(contour_plot)

    box = parameters_contour_plot.get_position()
    parameters_contour_plot.set_position([box.x0, box.y0, box.width,
                                          box.height])

    plt.tight_layout()
    plt.savefig('contour_plot.png', dpi=300)

    return plt.show(), parameters_contour_plot


def uncertainty_propagation(function, variable_1, variable_2,
                            variable_1_uncertainty):
    """
    Finds the uncertainty for the star velocity, planets distance from the
    star, velocity of planet and the mass of the planet.

    Parameters
    ----------
    function : function
    variable_1 : numpy float64
    variable_2 : numpy float64
    variable_1_uncertainty : numpy float64

    Returns
    -------
    function uncertainty : numpy float64

    """
    if function is star_velocity_calculator:
        return np.abs(((SPEED_OF_LIGHT_VACUMN/EMITTED_WAVELENGHT) *
                       variable_1_uncertainty))

    if function is planet_distance_from_star_calculator:
        return np.abs((-2/3) * ((GRAVITATIONAL_CONSTANT * MASS_OF_STAR)**(1/3))
                      * variable_1**(-5/3) *
                      variable_1_uncertainty)

    if function is velocity_of_planet_calculator:
        return np.abs(((-1/2) * (((GRAVITATIONAL_CONSTANT * MASS_OF_STAR) /
                                  (variable_1))**(-1/2)) *
                       ((GRAVITATIONAL_CONSTANT * MASS_OF_STAR) /
                        (variable_1**2))) * variable_1_uncertainty)
    return np.abs(np.sqrt((((MASS_OF_STAR * variable_1) /
                            (variable_2)**2)**2) +
                          ((MASS_OF_STAR/variable_2) *
                           variable_1_uncertainty)**2))


def uncertainty_from_contour_plot(parrameters_contour_plot):
    """
    Calculates the uncertainty of the fitted variables in a contour plot.

    Parameters
    ----------
    parrameters_contour_plot : matplotlib axes_subplots AxesSubplot

    Returns
    -------
    speed_star_uncertaintys : numpy float64
        meters / second
    angular_speed_uncertaintys : numpy float64
        rad / s

    """
    axis_values_array = parrameters_contour_plot.collections[1].get_paths()[0]
    axis_values_numpy_array = axis_values_array.vertices
    speed_star_data = axis_values_numpy_array[:, 0]
    angular_speed_data = axis_values_numpy_array[:, 1]
    minimum_speed_star = np.min(speed_star_data)
    maximum_speed_star = np.max(speed_star_data)
    minimum_angular_speed = np.min(angular_speed_data)
    maximum_angular_speed = np.max(angular_speed_data)
    speed_star_uncertaintys = (maximum_speed_star -
                               minimum_speed_star
                               ) / 2
    angular_speed_uncertaintys = (maximum_angular_speed -
                                  minimum_angular_speed) / 2

    return speed_star_uncertaintys, angular_speed_uncertaintys


def main():
    """
    Main code for program.
    """
    # Read in data
    if file_check(DATA_FILE_1) and file_check(DATA_FILE_2):

        data_file_3 = remove_outliers_1(np.vstack([read_data(DATA_FILE_1),
                                                   read_data(DATA_FILE_2)]), 3)
        data_file_3 = data_file_3[np.argsort(data_file_3[:, 0])]
        time, wavelenght, wavelenght_uncertainty = (data_file_3[:, 0],
                                                    data_file_3[:, 1],
                                                    data_file_3[:, 2])

        plot_raw_data(data_file_3, 'Raw_data_plot.png')
        # Convert to s from years and to m from nm
        time *= YEARS_TO_SECONDS_CONVERSION
        wavelenght *= NANOMETERS_TO_METERS_CONVERSION
        wavelenght_uncertainty *= NANOMETERS_TO_METERS_CONVERSION
        star_velocity_data = [time, star_velocity_calculator(wavelenght),
                              uncertainty_propagation(star_velocity_calculator,
                                                      wavelenght, 0,
                                                      wavelenght_uncertainty)]
        star_velocity_data_numpy_array = np.array(star_velocity_data).T
        # create an initial fit and remove data points that are far away from
        # the best fit.
        initial_fit = minimisation(star_velocity_data, 3)
        speed_star, angular_speed, phase = (initial_fit[0][0],
                                            initial_fit[0][1],
                                            initial_fit[0][2])
        cleaned_star_velocity_data = remove_outliers_2(
            star_velocity_data_numpy_array, 1, speed_star,
            angular_speed, phase)
        cleaned_star_velocity_data_list = [cleaned_star_velocity_data[:, 0],
                                           cleaned_star_velocity_data[:, 1],
                                           cleaned_star_velocity_data[:, 2]]
        # find the phase
        fit_1 = minimisation(cleaned_star_velocity_data_list, 3)
        phase = fit_1[0][2]
        # Find speed of star and angular speed using the found value
        # of phase
        fit_2 = minimisation(cleaned_star_velocity_data_list, 2, phase)
        fitted_parameters = fit_2[0]
        minimum_chi_squared = fit_2[1]
        reduced_chi_squared = minimum_chi_squared /\
            (len(cleaned_star_velocity_data) - 2)
        speed_star = fit_2[0][0]
        angular_speed = fit_2[0][1]
        # Plot fitted data and contour plot
        plot_fitted_data('plot_of_velocity_against_time_without_outliers.png',
                         fitted_parameters, minimum_chi_squared,
                         cleaned_star_velocity_data,
                         phase)
        parameters_contour_plot = contour_plot_function(
            fitted_parameters,
            cleaned_star_velocity_data,
            minimum_chi_squared,
            phase)[1]
        # Uncertaintys on speed of star and angular speed
        speed_star_uncertainty, angular_speed_uncertainty\
            = uncertainty_from_contour_plot(parameters_contour_plot)
        # Calculation of other physical values
        planet_distance_from_star = planet_distance_from_star_calculator(
            angular_speed)
        planet_distance_from_star_au = planet_distance_from_star /\
            METERS_TO_AU_CONVERSION
        velocity_of_planet = velocity_of_planet_calculator(
            planet_distance_from_star)
        mass_of_planet = mass_of_planet_calculator(
            speed_star, velocity_of_planet)
        mass_of_planet_jovian_mass = mass_of_planet /\
            KILOGRAMS_TO_JOVIAN_MASS_CONVERSION
        # Now find uncertainty on these values
        planet_distance_from_star_uncertainty = uncertainty_propagation(
            planet_distance_from_star_calculator,
            angular_speed,
            0,
            angular_speed_uncertainty)
        planet_distance_from_star_uncertainty_au =\
            planet_distance_from_star_uncertainty / METERS_TO_AU_CONVERSION
        velocity_of_planet_uncertainty =\
            uncertainty_propagation(velocity_of_planet_calculator,
                                    planet_distance_from_star,
                                    0,
                                    planet_distance_from_star_uncertainty)
        mass_of_planet_uncertainty =\
            uncertainty_propagation(mass_of_planet_calculator,
                                    speed_star,
                                    velocity_of_planet,
                                    speed_star_uncertainty)
        mass_of_planet_uncertainty_jovian_mass = mass_of_planet_uncertainty /\
            (KILOGRAMS_TO_JOVIAN_MASS_CONVERSION)
        print('The reduced chi squared value is: {0:.3g}'.
              format(reduced_chi_squared))
        print(r'The phase is: {0:.4g} rad '.
              format(phase))
        print(('The magnitude of the star velocity (V0) is: '
               '({0:.4g} +/- {1:.2f}) m/s').
              format(speed_star,
                     speed_star_uncertainty))
        print(('The angular speed is (w): '
               '({0:.4g} +/- {1:.2g}) rad/s').
              format(angular_speed, angular_speed_uncertainty))
        print(('The planets distance from the star (r) is: '
               '({0:.4g} +/- {1:.3g}) AU').
              format(planet_distance_from_star_au,
                     planet_distance_from_star_uncertainty_au))
        print(('The velocity of the planet (Vp) is: '
               '({0:.4g} +/- {1:.4g}) m/s').
              format(velocity_of_planet,
                     velocity_of_planet_uncertainty))
        print(('The mass of the planet (Mp) is: '
               '({0:.4g} +/- {1:.3g}) Jovian masses').format
              (mass_of_planet_jovian_mass,
               mass_of_planet_uncertainty_jovian_mass))
    return 0


main()
