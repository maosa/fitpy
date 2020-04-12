
################################################################################
################################################################################

# Clear the database and migrations
# https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html
# https://www.techiediaries.com/resetting-django-migrations/

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
find . -name "db.sqlite3" -delete
find . -type d -name 'profile_pics' -exec rm -rf {} +

################################################################################
################################################################################

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser # remember to upload a profile picture

python manage.py shell

################################################################################
################################################################################

# Run the following python code from within the shell

import pandas as pd
from workouts.models import Workout
from django.contrib.auth.models import User

# Get user

user = User.objects.filter(username='maosa').first()

# Try adding just one entry

# workout = Workout(
#     date='2020-04-12',
#     workout='Running',
#     duration=45,
#     distance=8,
#     user=user
# )
#
# workout.save()

# Define functions

def pace(dur, dist):
    pace_tmp = dur/dist
    pace_m = pace_tmp.astype(int)
    pace_s = [round((int(str(x).split('.')[1])/(10**(len(str(x).split('.')[1])))) * 0.6, 2) for x in list(pace_tmp)]
    pace = pace_m + pace_s
    del pace_tmp, pace_m, pace_s
    return(pace)

# Read data

data = pd.read_csv('/Users/maosa/fitr/data.csv', sep=',', )

# Make colnames lowercase

data.columns = [x.lower() for x in list(data.columns)]

# Drop unnecessary columns

data.drop(['no'], axis=1, inplace=True)

# Categorise workouts

category = []

for w in range(0, len(data)):

    workout = data['workout'][w]

    if workout == 'Chest':
        category.append('chest')
    elif workout == 'Back':
        category.append('back')
    elif workout in ['Legs', 'Legs and Core']:
        category.append('legs')
    elif workout in ['Compound', 'Multisport']:
        category.append('compound')
    elif workout in [
        'Running', 'Cycling', 'Cardio', 'Basketball', 'Swimming', 'Surfing', 'Skiing'
    ]:
        category.append('cardio')
    elif workout == 'Rest':
        category.append('rest')
    else:
        category.append('other')

if len(category) == len(data):
    data['category'] = category

# Add user

data['user'] = 'maosa'

# Handle running data

run = pd.read_csv('/Users/maosa/fitr/run.csv', sep=',', )

run.columns = [x.lower() for x in list(run.columns)]

run['pace'] = pace(run['duration'], run['distance'])

run.drop(labels=['no', 'duration'], axis=1, inplace=True)

# Compile the database

db = pd.merge(left=data, right=run, how='left', on='date')

db.fillna(value=0, inplace=True)

db = db[['date', 'workout', 'duration', 'distance', 'pace', 'category', 'user']]

################################################################################
################################################################################

# Loop over the rows and add to database

for i in range(0, len(db)):

    # Create object

    workout = Workout(
        # no = db['no'][i], # do not enter the no field as Django uses its own ID (primary key)
        date = db['date'][i],
        workout = db['workout'][i],
        duration = db['duration'][i],
        distance = db['distance'][i],
        pace = db['pace'][i],
        category = db['category'][i],
        user=user
    )

    # Add object to database

    try:
        workout.save()
    except:
        print('There was a problem with row', i)

################################################################################
################################################################################

# View the database containing the workouts

python manage.py dbshell

# Get all tables in the database

.tables

# Get table structure

.schema workouts_workout

################################################################################
################################################################################

# Filter the database

python manage.py shell

from workouts.models import Workout
from django.contrib.auth.models import User

Workout.objects.filter(workout='Running')

################################################################################
################################################################################

# Remove a table from the database

python manage.py dbshell

DROP TABLE workouts_workout;

################################################################################
################################################################################
