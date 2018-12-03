from random import *


# This class defines a Person in our simulation and describes how they behave throughout
class Person:
    def __init__(self, disease, initial_state='Susceptible'):
        self.disease = disease  # The disease the person may or may not be sick of

        # A person can only start with one of the 3 following states as they cannot start dead
        if initial_state == 'Susceptible' or initial_state == 'Immune' or initial_state == 'Infected':
            self.state = initial_state
        else:
            # The default state should be susceptible
            self.state = 'Susceptible'

    def __str__(self):
        return 'Person currently ' + self.state

    # This method tells us if this person recovers from the disease
    def recovers(self):
        recovers = random() <= self.disease.recovery_rate
        if recovers:
            self.state = 'Immune'

        return recovers

    # This method tells us if this person dies from the disease
    def dies(self):
        dies = random() <= self.disease.lethality_rate
        if dies:
            self.state = 'Dead'

        return dies

    # This method tells us if this person catches the disease after a single contact
    def gets_sick(self, contact_person):
        if contact_person.state != 'Infected':
            return False

        got_sick = random() <= self.disease.infection_rate
        if got_sick:
            self.state = 'Infected'

        return got_sick

