# ----------------------------------------------------------------------
# Script, to be imported as a module into main.py, which plots line
# graphs showing a time series of COVID-19 cases and deaths per country
# and the excess deeaths per country.
# ----------------------------------------------------------------------

import pandas as pd
import plotly.graph_objects as go
import numpy as np


class PlotLines:
    """Class to plot time series graphs showing COVID-19 cases and
    deaths per country."""
    def __init__(self, data, line_template, colours):
        self.data = data
        self.line_template = line_template
        self.colours = colours

    def plot_graph(self, df, countries, var_1, var_2, title_1, title_2,
                   subtitle, label, button_1, button_2, y_axis_title):
        """There are 12 graphs which are built the same way, therefore a
        template for the plot can be used to avoid replicating code. It
        takes arguments which fill the template with the required
        parameters.

        Arguments
            df : the Data Frame containing data to plot
            countries : list of countries to plot
            var_1 : either cases or deaths
            var_2 : either cases per million or deaths per million
            title_1 : title for all cases/deaths
            title_2 : title for per million cases/deaths
            subtitle : subtitle
            label : label for the hoverlabel
            button_1 : label for the all cases/deaths button
            button_2 : label for the per million cases/deaths button
            y_axis_title : title for the y-axis
        """
        fig = go.Figure()

        # Total cases / deaths
        for country, color in zip(countries, self.colours):
            fig.add_trace(
                go.Scatter(
                    x=list(df['date'][df['country'] == country]),
                    y=list(df[var_1][df['country'] == country]),
                    name=country,
                    mode='lines',
                    line=dict(
                        color=color
                    ),
                    customdata=np.stack((
                        df['country'][df['country'] == country],
                        df['flag'][df['country'] == country],
                        df[var_1 + '_str'][df['country'] == country]),
                        axis=-1),
                    hovertemplate=
                    '<b>Date:</b> %{x}<br>'+
                    '<b>' + label + ':</b> %{customdata[2]}'+
                    '<extra>%{customdata[0]} %{customdata[1]}</extra>'
                )
            )

        # Total cases / deaths per million
        for country, color in zip(countries, self.colours):
            fig.add_trace(
                go.Scatter(
                    x=list(df['date'][df['country'] == country]),
                    y=list(df[var_2][df['country'] == country]),
                    name=country,
                    mode='lines',
                    visible=False,
                    line=dict(
                        color=color
                    ),
                    customdata=np.stack((
                        df['country'][df['country'] == country],
                        df['flag'][df['country'] == country],
                        df[var_2 + '_str'][df['country'] == country]),
                        axis=-1),
                    hovertemplate=
                    '<b>Date:</b> %{x}<br>'+
                    '<b>' + label + ':</b> %{customdata[2]}'+
                    '<extra>%{customdata[0]} %{customdata[1]}</extra>'
                )
            )

        fig.update_layout(
            template=self.line_template,
            title="<b>" + title_1 + "</b><br><sub>" + subtitle,
            yaxis_title=y_axis_title,
            legend_title=("<b>Click to add/remove country,<br>Double click to "
                          "isolate</b>"),
            updatemenus=[
                dict(
                    direction='down',
                    x=1,
                    xanchor='right',
                    y=1.1,
                    yanchor='top',
                    buttons=list([
                        dict(label=button_1,
                             method='update',
                             args=[{'visible': ([True] * len(countries)
                                                + [False] * len(countries))},
                                   {'title': ("<b>" + title_1 + "</b><br><sub>"
                                              + subtitle)}]),
                        dict(label=button_2,
                             method='update',
                             args=[{'visible': ([False] * len(countries)
                                                + [True] * len(countries))},
                                   {'title': ("<b>" + title_2 + "</b><br><sub>"
                                              + subtitle)}]),
                    ])
                )
            ]
        )
        return fig

    def plot_daily_cases(self):
        """Plot daily cases per country for the world.

        File name: daily_cases.html"""
        df = self.data['cases']
        countries = df['country'].unique()

        fig = self.plot_graph(
            df, countries, '7_day_average', '7_day_average_per_million',
            'Daily Cases', 'Daily Cases per Million',
            ('7 day rolling average<br>Sources: John Hopkins University '
             'CSSE, World Bank'),
            '7 day average','Cases', 'Cases / million', 'Daily Cases')

        fig.write_html('graphs/cases/daily_cases.html')

    def plot_daily_cases_oecd(self):
        """Plot daily cases per country for OECD countries.

        File name: daily_cases_OECD.html"""
        df = self.data['cases']
        df = df[df['OECD'] == True]
        countries = df['country'].unique()

        fig = self.plot_graph(
            df, countries, '7_day_average', '7_day_average_per_million',
            'Daily Cases - OECD', 'Daily Cases per Million - OECD',
            ('7 day rolling average<br>Sources: John Hopkins University '
             'CSSE, World Bank'),
            '7 day average', 'Cases', 'Cases / million', 'Daily Cases')

        fig.write_html('graphs/cases/daily_cases_OECD.html')

    def plot_daily_cases_eu(self):
        """Plot daily cases per country for EU/EEA countries.

        File name: daily_cases_EU_EEA.html"""
        df = self.data['cases']
        df = df[df['EU_EEA'] == True]
        countries = df['country'].unique()

        fig = self.plot_graph(
            df, countries, '7_day_average', '7_day_average_per_million',
            'Daily Cases - EU/EEA', 'Daily Cases per Million - EU/EEA',
            ('7 day rolling average<br>Sources: John Hopkins University '
             'CSSE, World Bank'),
            '7 day average', 'Cases', 'Cases / million', 'Daily Cases')

        fig.write_html('graphs/cases/daily_cases_EU_EEA.html')

    def plot_total_cases(self):
        """Plot total cases per country for the world.

        File name: total_cases.html"""
        df = self.data['cases']
        countries = df['country'].unique()

        fig = self.plot_graph(
            df, countries, 'cases', 'cases_per_million',
            'Total Cases', 'Total Cases per Million',
            'Sources: John Hopkins University CSSE, World Bank',
            'Total', 'Cases', 'Cases / million', 'Total Cases')

        fig.write_html('graphs/cases/total_cases.html')

    def plot_total_cases_oecd(self):
        """Plot total cases per country for OECD countries.

        File name: total_cases_OECD.html"""
        df = self.data['cases']
        df = df[df['OECD'] == True]
        countries = df['country'].unique()

        fig = self.plot_graph(
            df, countries, 'cases', 'cases_per_million',
            'Total Cases - OECD', 'Total Cases per Million - OECD',
            'Sources: John Hopkins University CSSE, World Bank',
            'Total', 'Cases', 'Cases / million', 'Total Cases')

        fig.write_html('graphs/cases/total_cases_OECD.html')

    def plot_total_cases_eu(self):
        """Plot total cases per country for EU/EEA countries.

        File name: total_cases_EU_EEA.html"""
        df = self.data['cases']
        df = df[df['EU_EEA'] == True]
        countries = df['country'].unique()

        fig = self.plot_graph(
            df, countries, 'cases', 'cases_per_million',
            'Total Cases - EU/EEA', 'Total Cases per Million - EU/EEA',
            'Sources: John Hopkins University CSSE, World Bank',
            'Total', 'Cases', 'Cases / million', 'Total Cases')

        fig.write_html('graphs/cases/total_cases_EU_EEA.html')

    def plot_daily_deaths(self):
        """Plot daily deaths per country for the world.

        File name: daily_deaths.html"""
        df = self.data['deaths']
        countries = df['country'].unique()

        fig = self.plot_graph(
            df, countries, '7_day_average', '7_day_average_per_million',
            'Daily Deaths', 'Daily Deaths per million',
            ('7 day rolling average<br>Sources: John Hopkins University '
             'CSSE, World Bank'),
            '7 day average', 'Deaths', 'Deaths / million', 'Daily Cases')

        fig.write_html('graphs/deaths/daily_deaths.html')

    def plot_daily_deaths_oecd(self):
        """Plot daily deaths per country for OECD countries.

        File name: daily_deaths_OECD.html"""
        df = self.data['deaths']
        df = df[df['OECD'] == True]
        countries = df['country'].unique()

        fig = self.plot_graph(
            df, countries, '7_day_average', '7_day_average_per_million',
            'Daily Deaths - OECD', 'Daily Deaths per million - OECD',
            ('7 day rolling average<br>Sources: John Hopkins University '
             'CSSE, World Bank'),
            '7 day average', 'Deaths', 'Deaths / million', 'Daily Deaths')

        fig.write_html('graphs/deaths/daily_deaths_OECD.html')

    def plot_daily_deaths_eu(self):
        """Plot daily deaths per country for EU/EEA countries.

        File name: daily_deaths_EU_EEA.html"""
        df = self.data['deaths']
        df = df[df['EU_EEA'] == True]
        countries = df['country'].unique()

        fig = self.plot_graph(
            df, countries, '7_day_average', '7_day_average_per_million',
            'Daily Deaths - EU/EEA', 'Daily Deaths per million - EU/EEA',
            ('7 day rolling average<br>Sources: John Hopkins University '
             'CSSE, World Bank'),
            '7 day average', 'Deaths', 'Deaths / million', 'Daily Deaths')

        fig.write_html('graphs/deaths/daily_deaths_EU_EEA.html')

    def plot_total_deaths(self):
        """Plot total deaths per country for the world.

        File name: total_deaths.html"""
        df = self.data['deaths']
        countries = df['country'].unique()

        fig = self.plot_graph(
            df, countries, 'deaths', 'deaths_per_million',
            'Total Deaths', 'Total Deaths per million',
            'Sources: John Hopkins University CSSE, World Bank',
            'Total', 'Deaths', 'Deaths / million', 'Total Deaths')

        fig.write_html('graphs/deaths/total_deaths.html')

    def plot_total_deaths_oecd(self):
        """Plot total deaths per country for OECD countries.

        File name: total_deaths_OECD.html"""
        df = self.data['deaths']
        df = df[df['OECD'] == True]
        countries = df['country'].unique()

        fig = self.plot_graph(
            df, countries, 'deaths', 'deaths_per_million',
            'Total Deaths - OECD', 'Total Deaths per million - OECD',
            'Sources: John Hopkins University CSSE, World Bank',
            'Total', 'Deaths', 'Deaths / million', 'Total Deaths')

        fig.write_html('graphs/deaths/total_deaths_OECD.html')

    def plot_total_deaths_eu(self):
        """Plot total deaths per country for EU/EEA.

        File name: total_deaths_EU_EEA.html"""
        df = self.data['deaths']
        df = df[df['EU_EEA'] == True]
        countries = df['country'].unique()

        fig = self.plot_graph(
            df, countries, 'deaths', 'deaths_per_million',
            'Total Deaths - EU/EEA', 'Total Deaths per million - EU/EEA',
            'Sources: John Hopkins University CSSE, World Bank',
            'Total', 'Deaths', 'Deaths / million', 'Total Deaths')

        fig.write_html('graphs/deaths/total_deaths_EU_EEA.html')


class PlotExcess:
    """Class to plot graph showing excess deaths by country."""
    def __init__(self, data, line_template, colours):
        self.excess = data['excess_deaths']
        self.line_template = line_template
        self.colours = colours

    def plot_excess(self):
        """Plot excess deaths by country.

        File name: excess_deaths.html
        """
        df = self.excess
        countries = df['country'].unique()

        fig = go.Figure()

        # Horizontal line
        fig.add_hline(
            y=0,
            line=dict(
                color='rgba(30, 30, 30, 0.4)',
                dash='dot'
            )
        )

        # Excess deaths
        for country, col in zip(countries, self.colours):
            fig.add_trace(
                go.Scatter(
                    x=[list(df['year'][df['country'] == country]),
                       list(df['week'][df['country'] == country])],
                    y=list(df['excess_deaths_pct_change'][
                        df['country'] == country]
                    ),
                    marker=dict(
                        color=col
                    ),
                    name=country,
                    customdata=np.stack((
                        df['week'][df['country'] == country],
                        df['year'][df['country'] == country],
                        df['country'][df['country'] == country],
                        df['flag'][df['country'] == country]),
                        axis=-1),
                    hovertemplate=
                    '<b>Week %{customdata[0]} - %{customdata[1]}</b><br>'+
                    '<b>Excess</b>: %{y:.2f}%'+
                    '<extra>%{customdata[2]} %{customdata[3]}</extra>'
                )
            )

        fig.update_layout(
            template=self.line_template,
            title=("<b>Weekly Excess Deaths (2020-2021) - % Over Expected "
                   "Weekly Deaths</b>"
                   "<br><sub>Source: The Economist"),
            legend_title=("<b>Click to add/remove country,<br>Double click to "
                          "isolate</b>"),
        )

        fig.write_html('graphs/deaths/excess_deaths.html')


def plot(data, line_template, colours):
    """Initiate PlotLines and PlotExcess classes and run methods to plot
    graphs.
    """
    line_plots = PlotLines(data, line_template, colours)

    # Cases
    line_plots.plot_daily_cases()
    line_plots.plot_daily_cases_oecd()
    line_plots.plot_daily_cases_eu()
    line_plots.plot_total_cases()
    line_plots.plot_total_cases_oecd()
    line_plots.plot_total_cases_eu()

    # Deaths
    line_plots.plot_daily_deaths()
    line_plots.plot_daily_deaths_oecd()
    line_plots.plot_daily_deaths_eu()
    line_plots.plot_total_deaths()
    line_plots.plot_total_deaths_oecd()
    line_plots.plot_total_deaths_eu()

    # Excess deaths
    excess = PlotExcess(data, line_template, colours)
    excess.plot_excess()
