# ----------------------------------------------------------------------
# Script, to be imported as a module into main.py, which plots maps
# showing COVID-19 deaths globally and at a US state level.
# ----------------------------------------------------------------------

import pandas as pd
import plotly.graph_objects as go
import numpy as np


class WorldMaps:
    """Class to prepare data and plot two maps, one showing total deaths
    per country on a global map and one showing total deaths per million
    per country on a global map. The maps are animated, showing the
    development of deaths over time.
    """
    def __init__(self, data, mapbox_key):
        self.data = data
        self.mapbox_key = mapbox_key

    def prepare_data(self):
        """To keeps the html maps files small, each animation frame
        represents a jump of 7 days instead of just 1. Therefore weekly
        dates from the 15th March 2020 are selected, with the others
        being dropped.
        """
        deaths = self.data['deaths']
        weekly_dates = pd.date_range(start='2020-03-15',
                                     end=deaths['date'].max(),
                                     freq='7D')
        deaths_weekly = deaths[deaths['date'].isin(weekly_dates)]
        self.deaths_weekly = deaths_weekly

    def plot_total_deaths(self):
        """Using Plotly and Mapbox, plot the animated map showing total
        deaths.
        """
        df = self.deaths_weekly

        # Construct frames
        frames = [{
            'name': 'frame_{}'.format(day),
            'data': [{
                'type': 'scattermapbox',
                'lat': df[df['date'] == day]['latitude'],
                'lon': df[df['date'] == day]['longitude'],
                'marker': go.scattermapbox.Marker(
                    size=df[df['date'] == day]['deaths'] ** 0.35,
                    color=df[df['date'] == day]['deaths'],
                    colorscale=['rgb(247, 255, 0)', 'rgb(180, 0, 0)'],
                    showscale=False
                ),
                'customdata': np.stack(
                    (df[df['date'] == day]['country'],
                     df[df['date'] == day]['flag'],
                     df[df['date'] == day]['deaths_str']),
                    axis=-1),
                'hovertemplate':
                "<extra></extra>" +
                "<b>%{customdata[0]}</b> %{customdata[1]} <br>" +
                "Deaths: %{customdata[2]}"
            }],
        } for day in df['date_string'].unique()]

        # Construct sliders
        sliders = [{
            'transition': {'duration': 0},
            'x': 0.08,
            'len': 0.88,
            'currentvalue': {'font': {'size': 15},
                             'prefix': '📅 ',
                             'visible': True,
                             'xanchor': 'center'},
            'steps': [
                {
                    'label': day,
                    'method': 'animate',
                    'args': [
                        ['frame_{}'.format(day)],
                        {'mode': 'immediate',
                         'frame': {'duration': 100, 'redraw': True},
                         'transition': {'duration':50}}
                      ],
                } for day in df['date_string'].unique()]
        }]

        # Play button
        play_button = [dict(
            type='buttons',
            showactive=True,
            x=0.02,
            y=-0.09,
            buttons=[dict(
                label='Play',
                method='animate',
                args=[
                    None,
                    dict(frame={'duration': 500, 'redraw': True},
                         transition={'duration':50},
                         fromcurrent=True,
                         mode='immediate'
                        )
                ]
            )]
        )]

        # Define the initial state
        data = frames[0]['data']

        # Add all sliders to the layout
        layout = go.Layout(
            sliders=sliders,
            updatemenus=play_button,
            mapbox={
                'accesstoken': self.mapbox_key,
                'center': {"lat": 20, "lon": 2.15},
                'zoom': 1.3,
                'style': 'light',
            }
        )

        # Create the figure
        fig = go.Figure(
            data=data,
            layout=layout,
            frames=frames
        )

        fig.update_layout(
            title=("<b>Total Deaths</b><br><sub>Source: John Hopkins "
                   "University CSSE"),
            height=700,
            margin=dict(l=50, r=50, b=50, t=70, pad=4),
        )

        fig.write_html('maps/world/total_deaths.html')

    def plot_total_deaths_per_million(self):
        """Using Plotly and Mapbox, plot the animated map showing total
        deaths per million.
        """
        df = self.deaths_weekly

        # Construct frames
        frames = [{
            'name': 'frame_{}'.format(day),
            'data': [{
                'type': 'scattermapbox',
                'lat': df[df['date'] == day]['latitude'],
                'lon': df[df['date'] == day]['longitude'],
                'marker': go.scattermapbox.Marker(
                    size=df[df['date'] == day]['deaths_per_million']**0.55,
                    color=df[df['date'] == day]['deaths_per_million'],
                    colorscale=['rgb(247, 255, 0)', 'rgb(180, 0, 0)'],
                    showscale=False,
                ),
                'customdata': np.stack(
                    (df[df['date'] == day]['country'],
                     df[df['date'] == day]['flag'],
                     df[df['date'] == day]['deaths_per_million_str']),
                    axis=-1),
                'hovertemplate':
                "<extra></extra>" +
                "<b>%{customdata[0]}</b> %{customdata[1]} <br>" +
                "Deaths / million: %{customdata[2]:.2f}"
            }],
        } for day in df['date_string'].unique()]

        # Construct sliders
        sliders = [{
            'transition':{'duration': 0},
            'x':0.08,
            'len':0.88,
            'currentvalue':{'font':{'size':15},
                            'prefix':'📅 ',
                            'visible':True,
                            'xanchor':'center'},
            'steps': [
                {
                    'label': day,
                    'method': 'animate',
                    'args':[
                        ['frame_{}'.format(day)],
                        {'mode': 'immediate',
                         'frame': {'duration': 100, 'redraw': True},
                         'transition': {'duration':50}}
                      ],
                } for day in df['date_string'].unique()]
        }]

        # Play button
        play_button = [dict(
            type='buttons',
            showactive=True,
            x=0.02,
            y=-0.09,
            buttons=[dict(
                label='Play',
                method='animate',
                args=[
                    None,
                    dict(frame={'duration': 500, 'redraw': True},
                         transition={'duration': 50},
                         fromcurrent=True,
                         mode='immediate'
                        )
                ]
            )]
        )]

        # Define the initial state
        data = frames[0]['data']

        # Add all sliders to the layout
        layout = go.Layout(
            sliders=sliders,
            updatemenus=play_button,
            mapbox={
                'accesstoken': self.mapbox_key,
                'center': {"lat": 20, "lon": 2.15},
                'zoom': 1.3,
                'style': 'light',
            }
        )

        # Create the figure
        fig = go.Figure(
            data = data,
            layout=layout,
            frames=frames
        )

        fig.update_layout(
            title=("<b>Total Deaths per Million</b><br><sub>Source: John "
                   "Hopkins University CSSE, World Bank"),
            height=700,
            margin=dict(l=50, r=50, b=50, t=70, pad=4),
        )

        fig.write_html('maps/world/total_deaths_per_million.html')


class UnitedStatesMaps:
    """Class to prepare data and plot two maps, one showing total deaths
    per US state and one showing total deaths per million per US state
    on a global map. The maps are animated, showing the development of
    deaths over time.
    """
    def __init__(self, data, mapbox_key):
        self.data = data
        self.mapbox_key = mapbox_key

    def prepare_data(self):
        """To keeps the html maps files small, each animation frame
        represents a jump of 7 days instead of just 1. Therefore weekly
        dates from the 15th March 2020 are selected, with the others
        being dropped.
        """
        usa = self.data['usa']

        weekly_dates = pd.date_range(start='2020-03-15',
                                     end=usa['date'].max(),
                                     freq='7D')

        usa_weekly = usa[usa['date'].isin(weekly_dates)]
        self.usa_weekly = usa_weekly

    def plot_total_deaths(self):
        """Using Plotly and Mapbox, plot the animated map showing total
        deaths.
        """
        df = self.usa_weekly

        # Construct frames
        frames = [{
            'name': 'frame_{}'.format(day),
            'data': [{
                'type': 'scattermapbox',
                'lat': df[df['str_date'] == day]['latitude'],
                'lon': df[df['str_date'] == day]['longitude'],
                'marker': go.scattermapbox.Marker(
                    size=df[df['str_date'] == day]['deaths']**0.4,
                    color=df[df['str_date'] == day]['deaths'],
                    colorscale=['rgb(247, 255, 0)', 'rgb(180, 0, 0)'],
                    showscale=False,
                ),
                'customdata': np.stack(
                    (df[df['str_date'] == day]['state'],
                     df[df['str_date'] == day]['deaths_str'],
                     df[df['str_date'] == day]['rank_total']),
                    axis=-1),
                'hovertemplate':
                "<extra></extra>" +
                "<b>%{customdata[0]}</b><br>" +
                "Deaths: %{customdata[1]} <br>" +
                "Rank: %{customdata[2]}"
            }],
        } for day in df['str_date'].unique()]

        # Construct sliders
        sliders = [{
            'transition': {'duration': 0},
            'x': 0.08,
            'len': 0.88,
            'currentvalue': {'font': {'size':15},
                             'prefix': '📅 ',
                             'visible': True,
                             'xanchor': 'center'},
            'steps': [
                {
                    'label': day,
                    'method': 'animate',
                    'args': [
                        ['frame_{}'.format(day)],
                        {'mode': 'immediate',
                         'frame': {'duration':100, 'redraw': True},
                         'transition': {'duration': 50}}
                      ],
                } for day in df['str_date'].unique()]
        }]

        # Play button
        play_button = [dict(
            type='buttons',
            showactive=True,
            x=0.02,
            y=-0.09,
            buttons=[dict(
                label='Play',
                method='animate',
                args=[
                    None,
                    dict(frame={'duration': 500, 'redraw': True},
                         transition={'duration': 50},
                         fromcurrent=True,
                         mode='immediate'
                        )
                ]
            )]
        )]

        # Define the initial state
        data = frames[0]['data']

        # Add all sliders to the layout
        layout = go.Layout(
            sliders=sliders,
            updatemenus=play_button,
            mapbox={
                'accesstoken': self.mapbox_key,
                'center': {"lat": 40, "lon": -95},
                'zoom': 3.3,
                'style': 'light',
            }
        )

        # Creat the figure
        fig = go.Figure(
            data=data,
            layout=layout,
            frames=frames
        )

        fig.update_layout(
            title=("<b>US States - Total Deaths</b><br><sub>Source: John "
                   "Hopkins University CSSE"),
            height=700,
            margin=dict(l=50, r=50, b=50, t=70, pad=4),
        )

        fig.write_html('maps/usa/total_deaths.html')

    def plot_total_deaths_per_100k(self):
        """Using Plotly and Mapbox, plot the animated map showing total
        deaths per 100,000.
        """
        df = self.usa_weekly

        # Construct frames
        frames = [{
            'name': 'frame_{}'.format(day),
            'data': [{
                'type': 'scattermapbox',
                'lat': df[df['str_date'] == day]['latitude'],
                'lon': df[df['str_date'] == day]['longitude'],
                'marker': go.scattermapbox.Marker(
                    size=df[df['str_date'] == day]['deaths_per_100k']**0.7,
                    color=df[df['str_date'] == day]['deaths_per_100k'],
                    colorscale=['rgb(247, 255, 0)', 'rgb(180, 0, 0)'],
                    showscale=False,
                ),
                'customdata': np.stack(
                    (df[df['str_date'] == day]['state'],
                     df[df['str_date'] == day]['deaths_per_100k_str'],
                     df[df['str_date'] == day]['rank_per_100k']),
                    axis=-1),
                'hovertemplate':
                "<extra></extra>" +
                "<b>%{customdata[0]}</b><br>" +
                "Deaths per 100k: %{customdata[1]} <br>" +
                "Rank: %{customdata[2]}"
            }],
        } for day in df['str_date'].unique()]

        # Construct sliders
        sliders = [{
            'transition': {'duration': 0},
            'x': 0.08,
            'len': 0.88,
            'currentvalue':{'font': {'size': 15},
                            'prefix': '📅 ',
                            'visible': True,
                            'xanchor': 'center'},
            'steps':[
                {
                    'label': day,
                    'method': 'animate',
                    'args': [
                        ['frame_{}'.format(day)],
                        {'mode': 'immediate',
                         'frame': {'duration': 100, 'redraw': True},
                         'transition': {'duration': 50}}
                      ],
                } for day in df['str_date'].unique()]
        }]

        # Play button
        play_button = [dict(
            type='buttons',
            showactive=True,
            x=0.02,
            y=-0.09,
            buttons=[dict(
                label='Play',
                method='animate',
                args=[
                    None,
                    dict(frame={'duration': 500, 'redraw': True},
                         transition={'duration': 50},
                         fromcurrent=True,
                         mode='immediate'
                        )
                ]
            )]
        )]

        # Define the initial state
        data = frames[0]['data']

        # Add all sliders to the layout
        layout = go.Layout(
            sliders=sliders,
            updatemenus=play_button,
            mapbox={
                'accesstoken': self.mapbox_key,
                'center': {"lat": 40, "lon": -95},
                'zoom': 3.3,
                'style': 'light',
            }
        )

        # Creat the figure
        fig = go.Figure(
            data=data,
            layout=layout,
            frames=frames
        )

        fig.update_layout(
            title=("<b>US States - Total Deaths per 100,000</b><br><sub>"
                   "Source: John Hopkins University CSSE"),
            height=700,
            margin=dict(l=50, r=50, b=50, t=70, pad=4),
        )

        fig.write_html('maps/usa/total_deaths_per_100000.html')


def plot(data, mapbox_key):
    """Initiate WorldMaps and UnitedStatesMaps classes and run methods
    to plot map.
    """
    maps = WorldMaps(data, mapbox_key)
    maps.prepare_data()
    maps.plot_total_deaths()
    #maps.plot_total_deaths_per_million()

    maps = UnitedStatesMaps(data, mapbox_key)
    maps.prepare_data()
    maps.plot_total_deaths()
    maps.plot_total_deaths_per_100k()
