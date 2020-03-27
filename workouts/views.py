from django.shortcuts import render
import pandas as pd

# Home page

# Create a function to handle the traffic from the home page of the app
# Within the function, return what we want the user to see when they are sent to this route

def home(request):

    # Read workout data

    data = pd.read_csv('/Users/maosa/fitpy/data.csv', sep=',')

    # Convert the data frame to a list of dictionaries where
    # each dictionary in the list is a data frame row
    # Note: This is used if one wants to loop over the data frame's rows

    workouts_cols = data.columns

    workouts = data.to_dict(orient='records')

    context = {
        'workouts' : workouts,
        'workouts_cols' : workouts_cols
    }

    return render(request, 'workouts/home.html', context)

# Running page

def running(request):
    return render(request, 'workouts/running.html')

#####
