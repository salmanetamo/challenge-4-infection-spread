from person import *
from disease import *
from aluLib import *
from random import *

# Constants for drawing
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 500
BAR_HEIGHT = 80
BAR_Y_COORD = 300
LEGEND_SIZE = 30
LEGEND_OFFSET = 250
LEGEND_TEXT_OFFSET = 210

# Setting up the population
# The values here are provided as a demo to the visualization, you will want to replace them by
# user input in your final solution.
original_population_size = 800  # This should start coming from user input.
immune_count = 50  # This should start coming from user input.
infected_count = 50  # This should start coming from user input.
deceased_count = 50  # This should start at 0 in your final result.
susceptible_count = original_population_size - immune_count - infected_count - deceased_count

CONTACT_NUMBER = 10  # Constant for how many people each Person meets a day.

# Keep track of how many days it's been
day_count = 0
target_duration = 100  # This should start coming from user input.

# You will have to update this list with the right kind of Person objects.
population = []


# You won't need to change this function, it will display a visual summary of each population
def draw_status():
    clear()
    set_font_size(24)
    draw_text("Total population is: " + str(immune_count + infected_count + susceptible_count), 10, 30)

    draw_text("Simulation has been running for " + str(day_count) + " days", 10, 75)

    # Figure out how large we should make each population
    susceptible_width = (susceptible_count / original_population_size) * WINDOW_WIDTH
    infected_width = (infected_count / original_population_size) * WINDOW_WIDTH
    immune_width = (immune_count / original_population_size) * WINDOW_WIDTH
    dead_width = (deceased_count / original_population_size) * WINDOW_WIDTH

    # Start with susceptible
    set_fill_color(0, 1, 0)
    # Draw the bar
    if susceptible_count != 0:
        draw_rectangle(0, BAR_Y_COORD, susceptible_width, BAR_HEIGHT)
    # Draw the legend:
    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 30, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Susceptible', WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 60)

    # Draw infected
    set_fill_color(1, 0, 0)
    if infected_count != 0:
        draw_rectangle(susceptible_width, BAR_Y_COORD, infected_width, BAR_HEIGHT)

    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 75, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Infected', WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 105)

    # Draw immune
    set_fill_color(0, 0, 1)
    if immune_count != 0:
        draw_rectangle(susceptible_width + infected_width, BAR_Y_COORD, immune_width, BAR_HEIGHT)

    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 120, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Immune', WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 150)

    # Draw diseased
    set_fill_color(0.2, 0.7, 0.7)
    if deceased_count != 0:
        draw_rectangle(susceptible_width + infected_width + immune_width, BAR_Y_COORD, dead_width, BAR_HEIGHT)

    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 165, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Dead', WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 195)


def check_the_infected():
    # Go over your population and check on each infected person
    # Did they get better today? Did they pass away?
    pass


def check_the_susceptible():
    # Go over your population and check on each susceptible person
    # Who did they meet today? Did they get infected from anyone?
    pass


def write_csv():
    # Each cycle, you should write down the values of each population into a csv file, so that we can export our data
    # to a spreadsheet and share it with others.
    pass


def generate_final_report():
    # Once your simulation is done, you must print out the following:
    # What percentage of the population survived?
    # What is R0?
    # Does that mean we've suffered an epidemic?
    pass


def main():
    global day_count
    # Draws the visual representation
    draw_status()

    # Loop over the infected population to determine if they could recover or pass away
    check_the_infected()

    # Loop over the healthy population to determine if they can catch the disease
    check_the_susceptible()

    # Update our output CSV
    write_csv()

    day_count += 1

    # End the simulation once we reach the set target.
    if day_count == target_duration:
        generate_final_report()
        cs1_quit()


start_graphics(main, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, framerate=1)
