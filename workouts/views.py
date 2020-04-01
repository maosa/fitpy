from django.shortcuts import render
import pandas as pd
# import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots

# Home page

# Create a function to handle the traffic from the home page of the app
# Within the function, return what we want the user to see when they are sent to this route

def home(request):

    ######################################################################

    # Read data

    data = pd.read_csv('/Users/maosa/fitpy/data.csv', sep=',')

    data_filt = pd.read_csv('/Users/maosa/fitpy/data_filt.csv', sep=',')

    run = pd.read_csv('/Users/maosa/fitpy/run.csv', sep=',') # only needed for stats

    # Convert the date column to datetime

    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

    data_filt['date'] = pd.to_datetime(data_filt['date'], format='%Y-%m-%d')

    ######################################################################

    # Stats

    if ((datetime.date(data['date'].iloc[-1]) - datetime.date(data['date'].iloc[0])).days + 1 == len(data)):
        days = len(data)

    workouts_tracked = len(data[
        ((data['workout'] != 'Rest') & (data['category'] != 'rest')) & (data['duration'] != 0)
    ])

    total_runs = len(run)

    runs_ratio = round((total_runs/workouts_tracked)*100, 2)

    rest_days = len(data[
        ((data['workout'] == 'Rest') & (data['category'] == 'rest')) & (data['duration'] == 0)
    ])

    rest_days_prop = round((rest_days/days)*100, 2)

    stats = [{
        'from' : data['date'].dt.strftime('%a, %d-%b-%Y').iloc[0],
        'to' : data['date'].dt.strftime('%a, %d-%b-%Y').iloc[-1],
        'days' : days,
        'workouts_tracked' : workouts_tracked,
        'total_runs' : total_runs,
        'runs_ratio' : runs_ratio,
        'rest_days' : rest_days,
        'rest_days_prop' : rest_days_prop
    }]

    ######################################################################

    # Generate plots and graphs

    ######################################################################

    # Calculate variables needed for the plots

    first_date = data_filt['date'].iloc[0]
    last_date = data_filt['date'].iloc[-1]
    mean_duration = data_filt['duration'].mean()

    fig = make_subplots(
        rows=4,
        cols=3,
        specs=[
            [{'colspan' : 3}, None, None],
            [{'colspan' : 3}, None, None],
            [{'colspan' : 3}, None, None],
            [{}, {}, {}]
        ],
        subplot_titles=('Duration per workout',
                        'Day difference between workouts',
                        'Duration change between workouts',
                        'Average workout time per week',
                        'Average workout time per month',
                        'Average workout time per year'),
        vertical_spacing=0.1
    )

    # Plot 1

    fig.add_trace(
        go.Scatter(
            x=data_filt['date'],
            y=data_filt['duration'],
            mode='lines',
            name='',
            line=dict(width=1),
            showlegend=False
        ),
        row=1,
        col=1
    )

    # Horizontal line at average

    fig.add_shape(
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
        row=1,
        col=1
    )

    # Add text on the horizontal line

    fig.add_trace(
        go.Scatter(
            x=[last_date - pd.DateOffset(60)],
            y=[mean_duration + 5],
            text=[round(mean_duration, 2)],
            textposition='top left',
            mode="text",
            showlegend=False,
            hoverinfo='none'
        ),
        row=1,
        col=1
    )

    # Plot 2

    fig.add_trace(
        go.Scatter(
            x=data_filt['date'],
            y=data_filt['daydelta'],
            mode='lines',
            name='',
            line=dict(width=1),
            showlegend=False
        ),
        row=2,
        col=1
    )

    # Plot 3

    fig.add_trace(
        go.Scatter(
            x=data_filt['date'],
            y=data_filt['duration_diff'],
            mode='lines',
            name='',
            line=dict(width=1),
            showlegend=False
        ),
        row=3,
        col=1
    )

    # Plot 4

    fig.add_trace(
        go.Scatter(
            x=data.groupby(['year', 'week'], as_index=False).mean().index + 1,
            y=round(data.groupby(['year', 'week'], as_index=False).mean()['duration'], 2),
            mode='lines',
            name='',
            line=dict(width=1),
            showlegend=False
        ),
        row=4,
        col=1
    )

    # Plot 5

    fig.add_trace(
        go.Scatter(
            x=data.groupby(['year', 'month'], as_index=False).mean().index + 1,
            y=round(data.groupby(['year', 'month'], as_index=False).mean()['duration'], 2),
            mode='lines',
            name='',
            line=dict(width=1),
            showlegend=False
        ),
        row=4,
        col=2
    )

    # Plot 6

    fig.add_trace(
        go.Scatter(
            x=data.groupby('year', as_index=False).mean()['year'],
            y=round(data.groupby('year', as_index=False).mean()['duration'], 2),
            mode='lines',
            name='',
            line=dict(#color='firebrick',
                width=1),
            showlegend=False
        ),
        row=4,
        col=3
    )

    # Update xaxis properties

    fig.update_xaxes(title_text='Date', row=3, col=1)

    fig.update_xaxes(title_text='Week', row=4, col=1)

    fig.update_xaxes(title_text='Month', row=4, col=2)

    fig.update_xaxes(title_text='Year', row=4, col=3)

    # Update yaxis properties

    fig.update_yaxes(title_text='Duration (mins)', row=1, col=1)

    fig.update_yaxes(title_text='Daydelta (days)', row=2, col=1)

    fig.update_yaxes(title_text='Duration change (%)', row=3, col=1)

    fig.update_yaxes(title_text='Duration (mins)', row=4, col=1)

    # Update layout

    fig.update_layout(
        height=1200,
        # margin=dict(l=10, r=10, t=10, b=10, pad=4),
        font=dict(
            family='Helvetica, monospace',
            size=16,
            color="#000000"
        )
    )

    fig_div = plot(
        fig,
        output_type='div',
        show_link=False,
        link_text=''
    )

    ######################################################################

    # Data transformation for generating pie charts

    data_stats = data.drop(
        labels=['no', 'year', 'month', 'week', 'day'], axis=1
    ).groupby(
        'category', as_index=False
    ).agg(
        ['sum', 'mean', 'count']
    )['duration'].transpose()

    data_stats.columns = [c.replace('_', ' ').capitalize() for c in data_stats.columns]

    ######################################################################

    # Pie charts

    pie_plots = make_subplots(
        rows=1,
        cols=2,
        specs=[[{'type' : 'domain'}, {'type' : 'domain'}]]
    )

    pie_plots.add_trace(
        go.Pie(
            labels=data_stats.columns,
            values=data_stats.loc['count', :],
            name='Count',
            title='Number of workouts per type'
        ),
        row=1,
        col=1
    )

    pie_plots.add_trace(
        go.Pie(
            labels=data_stats.drop(labels='Rest', axis=1).columns,
            values=data_stats.drop(labels='Rest', axis=1).loc['sum', :],
            name='Duration',
            title='Duration per workout type (mins)'
        ),
        row=1,
        col=2
    )

    pie_plots.update_layout(
        autosize=True,
        font=dict(
            family='Helvetica, monospace',
            size=16,
            color="#000000"
        )
    )

    pie_plots_div = plot(
        pie_plots,
        output_type='div',
        show_link=False,
        link_text=''
    )

    ######################################################################

    # Convert the data frame to a list of dictionaries where
    # each dictionary in the list is a data frame row
    # Note: This is used if one wants to loop over the data frame's rows
    # Run this just before the context dictionary is defined!

    # Modify date column

    data_filt['date'] = data_filt['date'].dt.strftime('%a, %d-%b-%Y')

    # Remove unnecessary columns

    data_filt.drop(labels=['daydelta', 'duration_diff', 'year', 'month', 'week', 'day'],
                   axis=1, inplace=True)

    # Get colnames

    # data_filt_cols = data_filt.columns

    # Convert data frame to dictionary

    data_filt = data_filt.to_dict(orient='records')

    ######################################################################

    context = {
        'stats' : stats,
        # 'data_filt_cols' : data_filt_cols,
        'data_filt' : data_filt,
        'fig_div' : fig_div,
        'pie_plots_div' : pie_plots_div
    }

    return render(request, 'workouts/home.html', context)



# Running page

def running(request):

    ######################################################################

    # Read data

    run = pd.read_csv('/Users/maosa/fitpy/run.csv', sep=',')

    # Convert the date column to datetime

    run['date'] = pd.to_datetime(run['date'], format='%Y-%m-%d')

    # Convert date column from datetime to string

    run['date'] = run['date'].dt.strftime('%a, %d-%b-%Y')

    # Get colnames

    run_cols = run.columns

    # Convert data frame to dictionary

    run = run.to_dict(orient='records')

    ######################################################################

    context = {
        'run_cols' : run_cols,
        'run' : run
    }

    return render(request, 'workouts/running.html', context)

#####
