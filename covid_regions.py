# ----------------------------------------------------------------------
# Script, to be imported as a module into main.py, which plots two bar
# charts showing the breakdown of deaths and cases by continent.
# ----------------------------------------------------------------------

import pandas as pd
import plotly.graph_objects as go
import numpy as np


class PlotRegions:
    """Class to plot two graphs, one showing the breakdown of deaths and
    cases by continent.
    """
    def __init__(self, data):
        self.data = data
        self.colours = ['orange', 'thistle', 'lightblue', 'steelblue', 'teal',
                        'indianred']

    def plot_deaths(self):
        """Plot deaths by continent.

        File name: deaths_by_region.html
        """
        df = self.data['continent_deaths']
        continents_list = df['continent'].unique()

        fig = go.Figure()

        # Total deaths
        for continent, color in zip(reversed(continents_list), self.colours):
            fig.add_trace(
                go.Scatter(
                    x=list(df['date'][df['continent'] == continent]),
                    y=list(df['%_total'][df['continent'] == continent]),
                    name=continent,
                    marker_color=color,
                    stackgroup='one',
                    hovertemplate=
                    '<b>Share</b>: %{y:.2f}%'+
                    '<br><b>Date</b>: %{x}</br>'
                ))

        # Daily deaths
        for continent, color in zip(reversed(continents_list), self.colours):
            fig.add_trace(
                go.Scatter(
                    x=list(df['date'][df['continent'] == continent]),
                    y=list(df['%_daily'][df['continent'] == continent]),
                    name=continent,
                    marker_color=color,
                    stackgroup='one',
                    visible = False,
                    hovertemplate=
                    '<b>Share</b>: %{y:.2f}%'+
                    '<br><b>Date</b>: %{x}</br>'
                ))

        fig.update_layout(
            title=dict(
                text=("<b>Percentage of Total Deaths by Region</b><br><sub>"
                      "Source: John Hopkins University CSSE"),
                x=0,
                xref='paper',
                y=0.96,
                yref='container',
                yanchor='top',
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(t=50),
            updatemenus=[
                dict(
                    direction="down",
                    x=1,
                    xanchor='right',
                    y=0.98,
                    yanchor='bottom',
                    buttons=list([
                        dict(
                            label="Total",
                            method="update",
                            args=[{"visible": [True]*6 + [False]*6},
                                  {"title": ("<b>Percentage of Total Deaths "
                                             "by Region</b><br><sub>Source: "
                                             "John Hopkins University CSSE")}]
                            ),
                        dict(
                            label="Daily",
                            method="update",
                            args=[{"visible": [False]*6 + [True]*6},
                                  {"title": ("<b>Percentage of Daily Deaths "
                                             "by Region</b><br><sub>Source: "
                                             "John Hopkins University CSSE")}]
                            ),
                    ])
                )
            ]
        )

        fig.write_html('graphs/deaths/deaths_by_region.html')

    def plot_cases(self):
        """Plot cases by continent.

        File name: cases_by_region.html
        """
        df = self.data['continent_cases']
        continents_list = df['continent'].unique()

        fig = go.Figure()

        # Total cases
        for continent, color in zip(reversed(continents_list), self.colours):
            fig.add_trace(
                go.Scatter(
                    x=list(df['date'][df['continent'] == continent]),
                    y=list(df['%_total'][df['continent'] == continent]),
                    name=continent,
                    marker_color=color,
                    stackgroup='one',
                    hovertemplate=
                    '<b>Share</b>: %{y:.2f}%'+
                    '<br><b>Date</b>: %{x}</br>'
                ))

        # Daily cases
        for continent, color in zip(reversed(continents_list), self.colours):
            fig.add_trace(
                go.Scatter(
                    x=list(df['date'][df['continent'] == continent]),
                    y=list(df['%_daily'][df['continent'] == continent]),
                    name=continent,
                    marker_color=color,
                    stackgroup='one',
                    visible=False,
                    hovertemplate=
                    '<b>Share</b>: %{y:.2f}%'+
                    '<br><b>Date</b>: %{x}</br>'
                ))

        fig.update_layout(
            title=dict(
                text=("<b>Percentage of Total Cases by Region</b><br><sub>"
                      "Source: John Hopkins University CSSE"),
                x=0,
                xref='paper',
                y=0.96,
                yref='container',
                yanchor='top',
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(t=50),
            updatemenus=[
                dict(
                    direction="down",
                    x=1,
                    xanchor='right',
                    y=0.98,
                    yanchor='bottom',
                    buttons=list([
                        dict(
                            label="Total",
                            method="update",
                            args=[{"visible": [True]*6 + [False]*6},
                                  {"title": ("<b>Percentage of Total Cases "
                                             "by Region</b><br><sub>Source: "
                                             "John Hopkins University CSSE")}]
                            ),
                        dict(
                            label="Daily",
                            method="update",
                            args=[{"visible": [False]*6 + [True]*6},
                                  {"title": ("<b>Percentage of Daily Cases "
                                             "by Region</b><br><sub>Source: "
                                             "John Hopkins University CSSE")}]
                            ),
                    ])
                )
            ]
        )

        fig.write_html('graphs/cases/cases_by_region.html')


def plot(data):
    """Initiate PlotRegions class and run methods to plot graphs."""
    regions = PlotRegions(data)
    regions.plot_deaths()
    regions.plot_cases()
