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

# Setting up the disease, prompting the user to enter the necessary information
name = input('Enter the name of the disease to be simulated: ')
infection_rate = float(input('What is the % chance that the disease transmits if two people are in contact? '))
recovery_rate = float(input('What is the % chance that someone recovers each day? '))
lethality_rate = float(input('What is the % chance that someone dies on a given day? '))

# Initializing a disease object with the provided values
disease = Disease(name, infection_rate, recovery_rate, lethality_rate)

# Setting up the population, prompting the user to enter the necessary information
original_population_size = int(input('How many people are we simulating? '))
immune_count = int(input('How many people are naturally immune or vaccine from the disease? '))
infected_count = int(input('How many people initially infected by the disease? '))
deceased_count = 0  # No deceased people at the beginning of the simulation
susceptible_count = original_population_size - immune_count - infected_count - deceased_count

# Initial number of infected people
initial_infected = infected_count

CONTACT_NUMBER = 10  # Constant for how many people each Person meets a day.

# Keep track of how many days it's been
day_count = 0
target_duration = int(input('For how many days should we run this simulation for? '))

# Creating our Person objects and populating our list
population = []

for index in range(0, original_population_size):
    person = Person(disease)
    if 0 <= index < immune_count:  # Creating the initially immune people
        person.state = 'Immune'
    elif immune_count <= index < infected_count + immune_count:  # Creating the initially infected people
        person.state = 'Infected'

    # Adding the person to our list. A person is by default susceptible, and no one starts dead
    population.append(person)

# Creating our CSV report file
csv_report_file = open('Report.csv', 'a')
csv_report_file.write('Total population, Susceptible, Infected, Immune, Dead\n')

# Initializing the value of r0
r0 = 0


# This function will display a visual summary of each population
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


# This function checks if our infected people recover from the disease or die from it,
# then update our categories accordingly
def check_the_infected():
    # Globals that need to be updated each day
    global infected_count, immune_count, deceased_count, population

    # This goes over the population and check on each infected person
    for i in range(0, len(population)):
        if population[i].state == 'Infected':
            if population[i].recovers():  # In case the person recovers
                # Decrement the number of infected and increment the number of immune/recovered people
                infected_count -= 1
                immune_count += 1  #
            elif population[i].dies():  # In case the person dies
                # Decrement the number of infected and increment the number of deceased people
                infected_count -= 1
                deceased_count += 1


# This function returns a list with length CONTACT_NUMBER containing random indices
# for the contacts a person makes each day
def get_random_indices(person_index):
    # This list contains our random indices
    daily_encounter = []

    # This loop should run until we have the required number of indices which is CONTACT_NUMBER
    while len(daily_encounter) != CONTACT_NUMBER:
        # Generate a random index
        random_index = randint(0, len(population) - 1)

        # Making sure we do not pick the person himself
        if random_index != person_index:
            daily_encounter.append(random_index)

    return daily_encounter


# This function checks if each of the susceptible people gets sick given the people they meet,
# then update the number of infected people if need be
def check_the_susceptible():
    # Our number of infected people that may need to be updated
    global infected_count, population, susceptible_count

    # This checks each susceptible person
    for i in range(0, len(population)):
        if population[i].state == 'Susceptible':
            # Getting our random encounters throughout the day
            daily_encounter = get_random_indices(i)

            # This person is initially healthy
            gets_sick = False

            # This goes through each of our encounters, and checks if any of them gives the person the disease
            for j in range(0, len(daily_encounter)):
                # At least, one of the encounters has made them sick
                if population[i].gets_sick(population[daily_encounter[j]]):
                    gets_sick = True

            if gets_sick:  # Now this person is sick, updating our number of infected people
                infected_count += 1
                susceptible_count -= 1


# This function adds a new line in our csv file each day with the values of each category
def write_csv():
    # Adding a line to the file with the values of our globals

    csv_report_file.write(str(len(population) - deceased_count) + ',' + str(susceptible_count) +
                          ',' + str(immune_count) + ',' + str(deceased_count)+'\n')


def generate_final_report():
    global r0, disease, day_count, deceased_count, original_population_size

    # Printing report at the end of the simulation
    if day_count == target_duration:
        print('Disease simulated: ' + disease.name)
        print('Percentage of population that survived: ' +
              str((original_population_size - deceased_count) / original_population_size) +
              '\n' + 'Value of R0: ' + str(r0))

        # Checking whether or not we experienced an epidemic
        if r0 > 1:
            print('Was it an epidemic: Yes')
        else:
            print('Was it an epidemic: No')


def update_r0():
    # Computing r0 on the day 20 of the cycle
    global r0

    if day_count == 20:
        # the numerator is the sum of infected and deceased people minus the originally infected people
        numerator = infected_count + deceased_count - initial_infected
        r0 = numerator / initial_infected


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

    # Update the value of r0
    update_r0()

    # End the simulation once we reach the set target.
    if day_count == target_duration:
        generate_final_report()
        cs1_quit()


start_graphics(main, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, framerate=1)
