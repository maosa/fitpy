#!/bin/bash

# Export workout data to a JSON file

python /Users/maosa/fitpy/manage.py dumpdata workouts.workout > /Users/maosa/fitpy/workouts.json
