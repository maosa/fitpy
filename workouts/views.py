from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin # user must be logged in to add a new workout
from django.views.generic import (
    ListView,
    DetailView,
    CreateView
) # class-based views
from .models import Workout

import pandas as pd
import numpy as np
from datetime import datetime

import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots

# Change current working directory

# import os
#
# if os.getcwd() != os.path.expanduser('~') + '/fitpy/':
#     os.chdir(os.path.expanduser('~') + '/fitpy/')
# else:
#     pass

####################################################################################################
####################################################################################################

# Define functions

def pace_avg(dur, dist):
    pace_tmp = dur/dist
    pace_m = pace_tmp.astype(int)
    pace_s = [(int(str(x).split('.')[1])/(10**(len(str(x).split('.')[1])))) for x in list(pace_tmp)]
    pace = (pace_m + pace_s).mean()
    pace_m = int(pace)
    pace_s = round((int(str(pace).split('.')[1])/(10**(len(str(pace).split('.')[1]))) * 0.6), 2)
    mean_pace = pace_m + pace_s
    del pace_tmp, pace_m, pace_s
    return(mean_pace)

####################################################################################################
####################################################################################################

# WORKOUTS TAB

####################################################################################################

class WorkoutListView(ListView):
    # What model to query in order to create the list
    model = Workout
    # Looks for a template as <app>/<model>_<viewtype>.html - change this to home.html
    template_name = 'workouts/home.html'
    # Change how the variable we loop over (in home.html) is named
    context_object_name = 'objects'
    # Change the database query order (descending)
    ordering = ['-date'] # use date for ascending order

####################################################################################################

# Define a class for a detailed view of individual workouts (use default conventions)

class WorkoutDetailView(DetailView):
    # By convention, this looks for a workouts/workout_detail.html
    model = Workout

####################################################################################################

# Class to create new workout entries - this will use a form
# User must be logged in to add a new workout (enabled by LoginRequiredMixin)

class WorkoutCreateView(LoginRequiredMixin, CreateView):

    model = Workout

    # Provide the form fields

    fields = [
        'date',
        'workout',
        'duration',
        'distance'
    ]

    # Override the default form_valid

    def form_valid(self, form):

        # Set the user to the currently logged in user

        form.instance.user = self.request.user

        # Automatically set the workout category

        if form.cleaned_data.get('workout') == 'Chest':
            form.instance.category = 'chest'
        elif form.cleaned_data.get('workout') == 'Back':
            form.instance.category = 'back'
        elif form.cleaned_data.get('workout') in ['Legs', 'Legs and Core']:
            form.instance.category = 'legs'
        elif form.cleaned_data.get('workout') in ['Compound', 'Multisport']:
            form.instance.category = 'compound'
        elif form.cleaned_data.get('workout') in [
            'Running', 'Cycling', 'Cardio', 'Basketball', 'Swimming', 'Surfing', 'Skiing'
        ]:
            form.instance.category = 'cardio'
        elif form.cleaned_data.get('workout') == 'Rest':
            form.instance.category = 'rest'
        else:
            form.instance.category = 'other'

        # Calculate the running pace

        def pace(dur, dist):
            pace_tmp = dur/dist
            pace_m = int(pace_tmp)
            pace_s = round((int(str(pace_tmp).split('.')[1])/(10**(len(str(pace_tmp).split('.')[1])))) * 0.6, 2)
            pace = pace_m + pace_s
            del pace_tmp, pace_m, pace_s
            return(pace)

        distance = form.cleaned_data.get('distance')

        if form.cleaned_data.get('workout') == 'Running' and distance > 0:
            form.instance.pace = pace(
                dur=form.cleaned_data.get('duration'),
                dist=form.cleaned_data.get('distance')
            )
        else:
            form.instance.pace = 0

        # Validate the form

        return super().form_valid(form)

####################################################################################################
####################################################################################################

# Create a function to handle the traffic from the home page of the app
# Within the function, return what we want the user to see when they are sent to this route

def home(request):

    ######################################################################

    # # Read data
    #
    # data = pd.read_csv('/Users/maosa/fitr/data.csv', sep=',', )
    #
    # # Make colnames lowercase
    #
    # data.columns = [x.lower() for x in list(data.columns)]
    #
    # # Convert dates to datetime
    #
    # data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    #
    # # Categorise workouts
    #
    # category = []
    #
    # for w in range(len(data['workout'])):
    #
    #     workout = data['workout'][w]
    #
    #     if workout == 'Chest':
    #         category.append('chest')
    #     elif workout == 'Back':
    #         category.append('back')
    #     elif workout in ['Legs', 'Legs and Core']:
    #         category.append('legs')
    #     elif workout in ['Compound', 'Multisport']:
    #         category.append('compound')
    #     elif workout in ['Running', 'Cycling', 'Cardio', 'Basketball', 'Surfing']:
    #         category.append('cardio')
    #     elif workout == 'Rest':
    #         category.append('rest')
    #     else:
    #         category.append('other')
    #
    # if len(category) == len(data):
    #     data['category'] = category
    #
    # # Add user
    #
    # data['user'] = 'maosa'
    #
    # # Generate year, month, week, day columns
    #
    # data['year'] = data['date'].dt.year
    #
    # data['month'] = data['date'].dt.month
    #
    # data['week'] = data['date'].dt.week
    #
    # data['day'] = data['date'].dt.day
    #
    # # Remove rest days
    #
    # data_filt = data.copy() # copy the original data frame to a new one for filtering
    #
    # mask = ((data['workout'] != 'Rest') & (data['category'] != 'rest')) & (data['duration'] != 0)
    #
    # data_filt = data_filt[mask]
    #
    # # Calculate percentage change between workout durations
    #
    # duration_diff = list(round(data_filt['duration'].pct_change() * 100, 2))
    #
    # duration_diff[0] = 0
    #
    # data_filt['duration_diff'] = duration_diff
    #
    # # Fix the first column
    #
    # data_filt['no'] = range(1, len(data_filt) + 1)
    #
    # # Reset index
    #
    # data_filt.reset_index(drop=True, inplace=True)
    #
    # # Calculate day difference between workouts
    #
    # daydelta = [
    #     int((data_filt['date'][i + 1] - data_filt['date'][i])/np.timedelta64(1, 'D')) for i in range(len(data_filt) - 1)
    # ]
    #
    # daydelta.insert(0, 0) # or use float('NaN')
    #
    # data_filt['daydelta'] = daydelta
    #
    # ######################################################################
    #
    # # Stats
    #
    # if ((datetime.date(data['date'].iloc[-1]) - datetime.date(data['date'].iloc[0])).days + 1 == len(data)):
    #     days = len(data)
    # else:
    #     days = 'ERROR'
    #
    # workouts = len(data[
    #     ((data['workout'] != 'Rest') & (data['category'] != 'rest')) & (data['duration'] != 0)
    # ])
    #
    # workouts_prop = round((workouts/days)*100, 2)
    #
    # rest = len(data[
    #     ((data['workout'] == 'Rest') & (data['category'] == 'rest')) & (data['duration'] == 0)
    # ])
    #
    # rest_prop = round((rest/days)*100, 2)
    #
    # runs = len(data[data['workout'] == 'Running'])
    #
    # runs_prop = round((runs/days)*100, 2)
    #
    # stats = [{
    #     'from' : data['date'].dt.strftime('%a, %d-%b-%Y').iloc[0],
    #     'to' : data['date'].dt.strftime('%a, %d-%b-%Y').iloc[-1],
    #     'days' : days,
    #     'workouts' : workouts,
    #     'workouts_prop' : workouts_prop,
    #     'rest' : rest,
    #     'rest_prop' : rest_prop,
    #     'runs' : runs,
    #     'runs_prop' : runs_prop
    # }]
    #
    # ######################################################################
    #
    # # Generate plots and graphs
    #
    # # Calculate required variables
    #
    # first_date = data_filt['date'].iloc[0]
    # last_date = data_filt['date'].iloc[-1]
    # mean_duration = data_filt['duration'].mean()
    #
    # fig = make_subplots(
    #     rows=4,
    #     cols=3,
    #     specs=[
    #         [{'colspan' : 3}, None, None],
    #         [{'colspan' : 3}, None, None],
    #         [{'colspan' : 3}, None, None],
    #         [{}, {}, {}]
    #     ],
    #     subplot_titles=('Duration per workout',
    #                     'Day difference between workouts',
    #                     'Duration change between workouts',
    #                     'Average workout time per week',
    #                     'Average workout time per month',
    #                     'Average workout time per year'),
    #     vertical_spacing=0.1
    # )
    #
    # # Plot 1
    #
    # fig.add_trace(
    #     go.Scatter(
    #         x=data_filt['date'],
    #         y=data_filt['duration'],
    #         mode='lines',
    #         name='',
    #         line=dict(width=1),
    #         showlegend=False
    #     ),
    #     row=1,
    #     col=1
    # )
    #
    # # Horizontal line at average
    #
    # fig.add_shape(
    #     type='line',
    #     x0=first_date,
    #     y0=mean_duration,
    #     x1=last_date,
    #     y1=mean_duration,
    #     line=dict(
    #         color='#000000',
    #         width=1,
    #         dash='dash',
    #     ),
    #     row=1,
    #     col=1
    # )
    #
    # # Add text on the horizontal line
    #
    # fig.add_trace(
    #     go.Scatter(
    #         x=[last_date - pd.DateOffset(60)],
    #         y=[mean_duration + 5],
    #         text=[round(mean_duration, 2)],
    #         textposition='top left',
    #         mode="text",
    #         showlegend=False,
    #         hoverinfo='none'
    #     ),
    #     row=1,
    #     col=1
    # )
    #
    # # Plot 2
    #
    # fig.add_trace(
    #     go.Scatter(
    #         x=data_filt['date'],
    #         y=data_filt['daydelta'],
    #         mode='lines',
    #         name='',
    #         line=dict(width=1),
    #         showlegend=False
    #     ),
    #     row=2,
    #     col=1
    # )
    #
    # # Plot 3
    #
    # fig.add_trace(
    #     go.Scatter(
    #         x=data_filt['date'],
    #         y=data_filt['duration_diff'],
    #         mode='lines',
    #         name='',
    #         line=dict(width=1),
    #         showlegend=False
    #     ),
    #     row=3,
    #     col=1
    # )
    #
    # # Plot 4
    #
    # fig.add_trace(
    #     go.Scatter(
    #         x=data.groupby(['year', 'week'], as_index=False).mean().index + 1,
    #         y=round(data.groupby(['year', 'week'], as_index=False).mean()['duration'], 2),
    #         mode='lines',
    #         name='',
    #         line=dict(width=1),
    #         showlegend=False
    #     ),
    #     row=4,
    #     col=1
    # )
    #
    # # Plot 5
    #
    # fig.add_trace(
    #     go.Scatter(
    #         x=data.groupby(['year', 'month'], as_index=False).mean().index + 1,
    #         y=round(data.groupby(['year', 'month'], as_index=False).mean()['duration'], 2),
    #         mode='lines',
    #         name='',
    #         line=dict(width=1),
    #         showlegend=False
    #     ),
    #     row=4,
    #     col=2
    # )
    #
    # # Plot 6
    #
    # fig.add_trace(
    #     go.Scatter(
    #         x=data.groupby('year', as_index=False).mean()['year'],
    #         y=round(data.groupby('year', as_index=False).mean()['duration'], 2),
    #         mode='lines',
    #         name='',
    #         line=dict(#color='firebrick',
    #             width=1),
    #         showlegend=False
    #     ),
    #     row=4,
    #     col=3
    # )
    #
    # # Update xaxis properties
    #
    # fig.update_xaxes(title_text='Date', row=3, col=1)
    #
    # fig.update_xaxes(title_text='Week', row=4, col=1)
    #
    # fig.update_xaxes(title_text='Month', row=4, col=2)
    #
    # fig.update_xaxes(title_text='Year', row=4, col=3)
    #
    # # Update yaxis properties
    #
    # fig.update_yaxes(title_text='Duration (mins)', row=1, col=1)
    #
    # fig.update_yaxes(title_text='Daydelta (days)', row=2, col=1)
    #
    # fig.update_yaxes(title_text='Duration change (%)', row=3, col=1)
    #
    # fig.update_yaxes(title_text='Duration (mins)', row=4, col=1)
    #
    # # Update layout
    #
    # fig.update_layout(
    #     height=1200,
    #     # margin=dict(l=10, r=10, t=10, b=10, pad=4),
    #     font=dict(
    #         family='Helvetica, monospace',
    #         size=16,
    #         color="#000000"
    #     )
    # )
    #
    # fig_div = plot(
    #     fig,
    #     output_type='div',
    #     show_link=False,
    #     link_text='',
    #     config=dict(
    #         displayModeBar=False
    #     )
    # )
    #
    # ######################################################################
    #
    # # Data transformation for generating pie charts
    #
    # data_stats = data.drop(
    #     labels=['no', 'year', 'month', 'week', 'day'], axis=1
    # ).groupby(
    #     'category', as_index=False
    # ).agg(
    #     ['sum', 'mean', 'count']
    # )['duration'].transpose()
    #
    # data_stats.columns = [c.replace('_', ' ').capitalize() for c in data_stats.columns]
    #
    # ######################################################################
    #
    # # Pie charts
    #
    # pie_plots = make_subplots(
    #     rows=1,
    #     cols=2,
    #     specs=[[{'type' : 'domain'}, {'type' : 'domain'}]]
    # )
    #
    # pie_plots.add_trace(
    #     go.Pie(
    #         labels=data_stats.columns,
    #         values=data_stats.loc['count', :],
    #         name='Count',
    #         title='Number of workouts per type'
    #     ),
    #     row=1,
    #     col=1
    # )
    #
    # pie_plots.add_trace(
    #     go.Pie(
    #         labels=data_stats.drop(labels='Rest', axis=1).columns,
    #         values=data_stats.drop(labels='Rest', axis=1).loc['sum', :],
    #         name='Duration',
    #         title='Duration per workout type (mins)'
    #     ),
    #     row=1,
    #     col=2
    # )
    #
    # pie_plots.update_layout(
    #     autosize=True,
    #     font=dict(
    #         family='Helvetica, monospace',
    #         size=16,
    #         color="#000000"
    #     )
    # )
    #
    # pie_plots_div = plot(
    #     pie_plots,
    #     output_type='div',
    #     show_link=False,
    #     link_text='',
    #     config=dict(
    #         displayModeBar=False
    #     )
    # )
    #
    # ######################################################################
    #
    # # Convert the data frame to a list of dictionaries where
    # # each dictionary in the list is a data frame row
    # # Note: This is used if one wants to loop over the data frame's rows
    # # Run this just before the context dictionary is defined!
    #
    # # Modify date column
    #
    # data['date'] = data['date'].dt.strftime('%a, %d-%b-%Y')
    #
    # # Remove unnecessary columns
    #
    # data.drop(labels=['year', 'month', 'week', 'day'], axis=1, inplace=True)
    #
    # # data_filt.drop(labels=['daydelta', 'duration_diff', 'year', 'month', 'week', 'day'], axis=1, inplace=True)
    #
    # # Convert data frame to dictionary
    #
    # data = data.to_dict(orient='records')
    #
    # # data_filt = data_filt.to_dict(orient='records')
    #
    # # Convert data frame to list of lists
    #
    # # data_filt = data_filt.values.tolist()

    ######################################################################

    context = {
        'title' : 'Workout log',
        # 'stats' : stats,
        'objects' : Workout.objects.all()
        # 'fig_div' : fig_div,
        # 'pie_plots_div' : pie_plots_div
    }

    return render(request, 'workouts/home.html', context)

####################################################################################################
####################################################################################################

# RUNS TAB

def runs(request):

    ######################################################################

    # Read data

    run = pd.read_csv('/Users/maosa/fitr/run.csv', sep=',')

    data = pd.read_csv('data.csv', sep=',')

    # Convert colnames to lowercase

    run.columns = [c.lower() for c in run.columns]

    data.columns = [x.lower() for x in list(data.columns)]

    # Convert date column to datetime

    run['date'] = pd.to_datetime(run['date'], format='%Y-%m-%d')

    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

    ######################################################################

    # Stats

    if ((datetime.date(data['date'].iloc[-1]) - datetime.date(data['date'].iloc[0])).days + 1 == len(data)):
        days = len(data)
    else:
        days = 'ERROR'

    runs = len(run)

    runs_prop = round((runs/days)*100, 2)

    stats = [{
        'from' : data['date'].dt.strftime('%a, %d-%b-%Y').iloc[0],
        'to' : data['date'].dt.strftime('%a, %d-%b-%Y').iloc[-1],
        'days' : days,
        'runs' : runs,
        'runs_prop' : runs_prop,
        'mean_dist' : round(run['distance'].mean(), 2),
        'mean_dur' : round(run['duration'].mean(), 2),
        'mean_pace' : pace_avg(dur=run.duration, dist=run.distance)
    }]

    ######################################################################

    # Generate run plots

    # Calculate variables needed for the plots

    first_date = run['date'].iloc[0]
    last_date = run['date'].iloc[-1]
    mean_distance = run['distance'].mean()
    mean_duration = run['duration'].mean()
    mean_pace = run['pace'].mean()

    run_plots = make_subplots(
        rows=3,
        cols=1,
        specs=[
            [{}],
            [{}],
            [{}]
        ],
        subplot_titles=('Distance per run',
                        'Duration per run',
                        'Pace per run'),
        vertical_spacing=0.1
    )

    # Plot 1

    run_plots.add_trace(
        go.Scatter(
            x=run['date'],
            y=run['distance'],
            mode='lines',
            name='',
            line=dict(width=1),
            showlegend=False
        ),
        row=1,
        col=1
    )

    # Horizontal line at average (plot 1)

    run_plots.add_shape(
        type='line',
        x0=first_date,
        y0=mean_distance,
        x1=last_date,
        y1=mean_distance,
        line=dict(
            color='#000000',
            width=1,
            dash='dash',
        ),
        row=1,
        col=1
    )

    # Add text on the horizontal line (plot 1)

    run_plots.add_trace(
        go.Scatter(
            x=[last_date - pd.DateOffset(60)],
            y=[mean_distance + 0.5],
            text=[round(mean_distance, 2)],
            textposition='top left',
            mode="text",
            showlegend=False,
            hoverinfo='none'
        ),
        row=1,
        col=1
    )

    # Plot 2

    run_plots.add_trace(
        go.Scatter(
            x=run['date'],
            y=run['duration'],
            mode='lines',
            name='',
            line=dict(width=1),
            showlegend=False
        ),
        row=2,
        col=1
    )

    # Horizontal line at average (plot 2)

    run_plots.add_shape(
        type='line',
        x0=first_date,
        y0=mean_duration,
        x1=last_date,
        y1=mean_duration,
        line=dict(
            color='#000000',
            width=1,
            dash='dash',
        ),
        row=2,
        col=1
    )

    # Add text on the horizontal line (plot 2)

    run_plots.add_trace(
        go.Scatter(
            x=[last_date - pd.DateOffset(60)],
            y=[mean_duration + 2],
            text=[round(mean_duration, 2)],
            textposition='top left',
            mode="text",
            showlegend=False,
            hoverinfo='none'
        ),
        row=2,
        col=1
    )

    # Plot 3

    run_plots.add_trace(
        go.Scatter(
            x=run['date'],
            y=run['pace'],
            mode='lines',
            name='',
            line=dict(width=1),
            showlegend=False
        ),
        row=3,
        col=1
    )

    # Update xaxis properties

    run_plots.update_xaxes(title_text='Date', row=3, col=1)

    # Update yaxis properties

    run_plots.update_yaxes(title_text='Distance (km)', row=1, col=1)

    run_plots.update_yaxes(title_text='Duration (mins)', row=2, col=1)

    run_plots.update_yaxes(title_text='Pace (mins/km)', row=3, col=1)

    # Update layout

    run_plots.update_layout(
        height=900,
        font=dict(
            family='Helvetica, monospace',
            size=16,
            color="#000000"
        )
    )

    run_plots_div = plot(
        run_plots,
        output_type='div',
        show_link=False,
        link_text='',
        config=dict(
            displayModeBar=False
        )
    )

    # Convert date column from datetime to string

    run['date'] = run['date'].dt.strftime('%a, %d-%b-%Y')

    # Get colnames

    run_cols = run.columns

    # Convert data frame to dictionary

    run = run.to_dict(orient='records')

    ######################################################################

    context = {
        'title' : 'Running log',
        'stats' : stats,
        'run_cols' : run_cols,
        'run' : run,
        'run_plots_div' : run_plots_div
    }

    return render(request, 'workouts/runs.html', context)

#####
