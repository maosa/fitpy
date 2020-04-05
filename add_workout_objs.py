# Firstly, run in the command line the following:

# python manage.py shell

import pandas as pd
from workouts.models import Workout
from django.contrib.auth.models import User

# Read data

data = pd.read_csv('/Users/maosa/fitr/data.csv', sep=',', )

# Make colnames lowercase

data.columns = [x.lower() for x in list(data.columns)]

# Categorise workouts

category = []

for w in range(len(data['workout'])):

    workout = data['workout'][w]

    if workout == 'Chest':
        category.append('chest')
    elif workout == 'Back':
        category.append('back')
    elif workout in ['Legs', 'Legs and Core']:
        category.append('legs')
    elif workout in ['Compound', 'Multisport']:
        category.append('compound')
    elif workout in ['Running', 'Cycling', 'Cardio', 'Basketball', 'Surfing']:
        category.append('cardio')
    elif workout == 'Rest':
        category.append('rest')
    else:
        category.append('other')

if len(category) == len(data):
    data['category'] = category

# Add user

data['user'] = 'maosa'

# data.head()

# Get user

user = User.objects.first()

# Trial

# workout = Workout(no=1, date='2020-04-06', workout='Multisport', duration=40, category='other', user=user)
# workout.save()

# Loop over the rows and add to database

for i in range(0, len(data)):

    # Create object

    workout = Workout(
        no = data['no'][i],
        date = data['date'][i],
        workout = data['workout'][i],
        duration = data['duration'][i],
        category = data['category'][i],
        user=user
    )

    # Add object to database

    try:
        workout.save()
    except:
        print('There was a problem with row', i)
