from datetime import date, timedelta

import pandas as pd
import plotly.graph_objects as go
import numpy as np

from countre import country_info


class SummaryTables:
    """Class to prepare data for summary tables and to plot them."""
    def __init__(self, data):
        self.deaths = data['deaths']
        self.cases = data['cases']
        self.path = 'graphs/summary_tables/'
        self.table_config = {'displayModeBar': False}
        self.colors = ['rgb(240,240,240)', 'rgb(232,240,240)']*15

    def set_latest_date(self):
        """Get the latest date in the format 01 Jan, 2020 to be used in
        table titles.
        """
        latest_date = self.deaths['date'].max().strftime('%d %b, %Y')
        self.latest_date = latest_date

    def create_df(self, df, var_1, var_2):
        """Function to create a data frame containing two variables for
        each country. The data frame contains only the top 10 countries
        for the first of the two variables.
        """
        df = df[df['date'] == df['date'].max()]
        df = df.sort_values(var_1, ascending=False)
        df = df[['country', var_1, var_2]].head(10).reset_index(drop=True)
        df[var_1] = ["{:,}".format(round(x, 2)) for x in df[var_1]]
        df[var_2] = ["{:,}".format(round(x, 2)) for x in df[var_2]]
        df[var_1] = [x[:-2] if x[-2:] == '.0' else x for x in df[var_1]]
        df[var_2] = [x[:-2] if x[-2:] == '.0' else x for x in df[var_2]]
        df['rank'] = df.index+1
        return df

    def plot_table(self, df, colors, latest_date, col_1, col_2, var_1,
                   var_2, title):
        """Function to display the Data Frame created by create_df as a
        table.
        """
        table = go.Figure()

        table.add_trace(
            go.Table(
                header=dict(
                    values=['', '<b>Country</b>', '<b>' + col_1 + '</b>',
                            '<b>' + col_2 + '</b>'],
                    font=dict(
                        color='white'
                    ),
                    align='left',
                    height=30,
                    fill_color='rgba(0, 153, 153, 0.9)'
                ),
                cells=dict(
                    values=[list(df['rank']), list(df['country']),
                            list(df[var_1]), list(df[var_2])],
                    align='left',
                    height=30,
                    fill_color=[colors*3]
                ),
                columnwidth=[0.1, 0.3, 0.3, 0.3]
            )
        )

        table.update_layout(
            title="<b>" + title + "</b><br>(Top 10 as of " + latest_date + ")",
            width=400,
            height=450,
            margin=dict(b=0, t=70, l=0, r=0)
        )

        return table

    def plot_total_deaths(self):
        """Table with top 10 countries by total deaths.

        File name: total_deaths.html
        """
        df = self.create_df(self.deaths, 'deaths', 'deaths_per_million')

        table = self.plot_table(
            df, self.colors, self.latest_date,
            'Total Deaths', 'Total Deaths / million',
            'deaths', 'deaths_per_million',
            'Total Deaths')

        table.write_html(self.path + 'total_deaths.html',
                         config=self.table_config)

    def plot_total_deaths_per_million(self):
        """Table with top 10 countries by total deaths per million.

        File name: total_deaths_per_million.html
        """
        df = self.create_df(self.deaths, 'deaths_per_million', 'deaths')

        table = self.plot_table(
            df, self.colors, self.latest_date,
            'Total Deaths / million', 'Total Deaths',
            'deaths_per_million', 'deaths',
            'Total deaths per Million')

        table.write_html(self.path + 'total_deaths_per_million.html',
                         config=self.table_config)

    def plot_daily_deaths(self):
        """Table with top 10 countries by daily deaths.

        File name: daily_deaths.html
        """
        df = self.create_df(self.deaths, 'daily', 'deaths')

        table = self.plot_table(
            df, self.colors, self.latest_date,
            'Daily Deaths', 'Total Deaths',
            'daily', 'deaths',
            'Daily Deaths')

        table.write_html(self.path + 'daily_deaths.html',
                         config=self.table_config)

    def plot_daily_deaths_per_million(self):
        """Table with top 10 countries by daily deaths per million.

        File name: daily_deaths_per_million.html
        """
        df = self.create_df(self.deaths, 'daily_million', 'daily')

        table = self.plot_table(
            df, self.colors, self.latest_date,
            'Daily Deaths / million', 'Daily Deaths',
            'daily_million', 'daily',
            'Daily Deaths per Million')

        table.write_html(self.path + 'daily_deaths_per_million.html',
                         config=self.table_config)

    def plot_total_cases(self):
        """Table with top 10 countries by total cases.

        File name: total_cases.html
        """
        df = self.create_df(self.cases, 'cases', 'cases_per_million')

        table = self.plot_table(
            df, self.colors, self.latest_date,
            'Total Cases', 'Total Cases / million',
            'cases', 'cases_per_million',
            'Total Cases')

        table.write_html(self.path + 'total_cases.html',
                         config=self.table_config)

    def plot_total_cases_per_million(self):
        """Table with top 10 countries by total cases per million.

        File name: total_cases_per_million.html
        """
        df = self.create_df(self.cases, 'cases_per_million', 'cases')

        table = self.plot_table(
            df, self.colors, self.latest_date,
            'Total Cases / million', 'Total Cases',
            'cases_per_million', 'cases',
            'Total Cases per Million')

        table.write_html(self.path + 'total_cases_per_million.html',
                         config=self.table_config)

    def plot_daily_cases(self):
        """Table with top 10 countries by daily cases.

        File name: daily_cases.html
        """
        df = self.create_df(self.cases, 'daily', 'cases')

        table = self.plot_table(
            df, self.colors, self.latest_date,
            'Daily Cases', 'Total Cases',
            'daily', 'cases',
            'Daily Cases')

        table.write_html(self.path + 'daily_cases.html',
                         config=self.table_config)

    def plot_daily_cases_per_million(self):
        """Table with top 10 countries by daily cases per million.

        File name: daily_cases_per_million.html
        """
        df = self.create_df(self.cases, 'daily_million', 'daily')

        table = self.plot_table(
            df, self.colors, self.latest_date,
            'Daily Cases / million', 'Daily Cases',
            'daily_million', 'daily',
            'Daily Cases per Million')

        table.write_html(self.path + 'daily_cases_per_million.html',
                         config=self.table_config)


class LastTwoWeeks:
    """Class to create tables showing the total number of cases and
    deaths for a specific set of countries in the past 14 days.
    """
    def __init__(self, data):
        self.data = data
        self.table_config = {'displayModeBar': False}
        self.countries = [
            'Sweden', 'United Kingdom', 'France', 'Spain', 'Norway', 'Denmark',
            'Germany', 'Portugal', 'Poland', 'Italy', 'Belgium', 'Austria',
            'Netherlands', 'Switzerland', 'Ireland', 'Greece', 'New Zealand',
            'Australia', 'US',
            ]
        colors = (['rgb(240, 240, 240)', 'rgb(232, 240, 240)']
                  * len(self.countries))
        self.colors = colors[:len(self.countries)]

    def two_weeks(self, df, country):
        """Function to find the number of deaths/cases in the most recent
        14 days, find the population of the given country, and return the
        number of deaths/cases per 100,000.
        """
        incidence = df[df['country'] == country]['daily'].iloc[-14:].sum()
        population = country_info([country], 'population')[0]
        return round(incidence / population * 100000, 3)


    def create_df(self, df):
        """Create a Data Frame with the country name and the number of
        deaths/cases in the past 14 days per 100,000.
        """
        two_week_total = [self.two_weeks(df, country)
                          for country in self.countries]

        df = pd.DataFrame(
            {
                'country': self.countries,
                '14 day': two_week_total
                }
            )
        df = df.sort_values('14 day', ascending=False).reset_index(drop=True)
        df['rank'] = df.index+1

        return df

    def plot_deaths(self):
        """Create a table displaying the Data Frame created by
        create_df.

        File name: 14_day_deaths_per_100000.html
        """
        df = self.create_df(self.data['deaths'])

        table = go.Figure()

        table.add_trace(
            go.Table(
                header=dict(
                    values=['', '<b>Country</b>', '<b>Deaths</b>'],
                    font=dict(
                        color='white'
                    ),
                    align='left',
                    height=30,
                    fill_color='rgba(0, 153, 153, 0.9)'
                ),
                cells=dict(
                    values=[list(df['rank']), list(df['country']),
                            list(df['14 day'])],
                    align='left',
                    height=30,
                    fill_color=[self.colors * 3]
                ),
                columnwidth=[0.1, 0.45, 0.45]
            )
        )

        table.update_layout(
            title=("<b>Total Deaths in Past 14 Days<br>per 100,000 "
                   "(selected countries)</b>"),
            font=dict(
                family='Arial'
            ),
            width=400,
            height=720,
            margin=dict(
                b=0,
                t=70,
                l=0,
                r=0,
            )
        )

        table.write_html(
            'graphs/summary_tables/14_day_deaths_per_100000.html',
            config=self.table_config)


    def plot_cases(self):
        """Create a table displaying the Data Frame created by
        create_df.

        File name: 14_day_cases_per_100000.html
        """
        df = self.create_df(self.data['cases'])

        table = go.Figure()

        table.add_trace(
            go.Table(
                header=dict(
                    values=['', '<b>Country</b>', '<b>Cases</b>'],
                    font=dict(
                        color='white'
                    ),
                    align='left',
                    height=30,
                    fill_color='rgba(0, 153, 153, 0.9)'
                ),
                cells=dict(
                    values=[list(df['rank']), list(df['country']),
                            list(df['14 day'])],
                    align='left',
                    height=30,
                    fill_color=[self.colors * 3]
                ),
                columnwidth=[0.1, 0.45, 0.45]
            )
        )

        table.update_layout(
            title=("<b>Total Cases in Past 14 Days<br>per 100,000 "
                   "(selected countries)</b>"),
            font=dict(
                family='Arial'
            ),
            width=400,
            height=720,
            margin=dict(
                b=0,
                t=70,
                l=0,
                r=0
            )
        )

        table.write_html(
            'graphs/summary_tables/14_day_cases_per_100000.html',
            config=self.table_config)


class Recovered:
    """Class to prepare data for tables showing recovery rates by country
    and then create the tables.
    """
    def __init__(self, data):
        self.cases = data['cases']
        self.deaths = data['deaths']
        self.today = data['deaths']['date'].max()
        self.path = 'graphs/summary_tables/'
        self.table_config = {'displayModeBar': False}
        self.color_list = ['rgb(240, 240, 240)', 'rgb(232, 240, 240)']

    def create_df(self, deaths, cases, start_date):
        """Function to calculate the case fatality rate by country,
        using data from a specified start date.
        """
        # Select deaths data from the specified start date and the most
        # recent date. Select cases date from 20 days before the
        # specified start day to account for the lag between infection
        # and death, and the most recent date.
        deaths = deaths[ (deaths['date'] == start_date)
                        | (deaths['date'] == self.today) ]
        cases = cases[( (cases['date'] == start_date)
                       | (cases['date'] == self.today - timedelta(days=20)) )]

        deaths = deaths[['country', 'date', 'deaths', 'OECD']].copy()
        cases = cases[['country', 'cases']].copy()

        # Create column with ids to identify whether the date is the
        # start date or the most recent date.
        deaths['date_id'] = ['start', 'end'] * len(deaths['country'].unique())
        cases['date_id'] = ['start', 'end'] * len(cases['country'].unique())

        df = deaths.merge(cases, on=['country', 'date_id'], how='left')
        countries = list(df['country'])
        df = df.groupby('country')[['deaths', 'cases']].diff().reset_index()
        df['country'] = countries
        df = df.dropna()

        df['case_fatality_rate'] = df['deaths'] / df['cases']

        df = df[['country', 'case_fatality_rate']]
        df = df.sort_values('case_fatality_rate',
                            ascending=False).reset_index()

        df['case_fatality_rate'] = round(df['case_fatality_rate'] * 100, 3)
        df['rank'] = df.index+1

        return df

    def plot_table(self, df, title, colors):
        """Function to plot table showing either recovery rates
        contained in the Data Frame argument.
        """
        table = go.Figure()

        table.add_trace(
            go.Table(
                header=dict(
                    values=['', '<b>Country</b>', '<b>Case Fatality Rate</b>'],
                    font=dict(
                        color='white',
                        size=15
                    ),
                    align='left',
                    height=30,
                    fill_color='rgba(0, 153, 153, 0.9)'
                ),
                cells=dict(
                    values=[list(df['rank']), list(df['country']),
                            list(df['case_fatality_rate'])],
                    font=dict(
                        size=15
                    ),
                    align='left',
                    height=30,
                    fill_color=[colors * 3]
                ),
                columnwidth=[0.1, 0.45, 0.45]
            )
        )

        table.update_layout(
            title=("<b>Case Fatality Rate (" + title + ")<br>"
                   "(deaths per 100 infections)</b>"),
            font=dict(
                family='Arial'
            ),
            width=450,
            height=750,
            margin=dict(b=0, t=70, l=0, r=0)
        )

        return table

    def plot_all(self):
        """Create table showing recovery rates in all countries.

        File name: recovered_all.html
        """
        df = self.create_df(self.deaths, self.cases, '2020-02-01')

        # List of two colors to get alternating row colors in the table
        colors = self.color_list * len(df['country'])
        colors = colors[:len(df['country'])]

        table = self.plot_table(df, 'All Data', colors)

        table.write_html(self.path + 'recovered_all.html',
                         config=self.table_config)

    def plot_autumn_all(self):
        """Create table showing recovery rates since autumn 2020 in all
        countries.

        File name: recovered_autumn.html
        """
        df = self.create_df(self.deaths, self.cases, '2020-08-01')

        # List of two colors to get alternating row colors in the table
        colors = self.color_list * len(df['country'])
        colors = colors[:len(df['country'])]

        table = self.plot_table(df, 'Since August 1st', colors)

        table.write_html(self.path + 'recovered_autumn.html',
                         config=self.table_config)

    def plot_oecd_all(self):
        """Create table showing recovery rates in OECD countries.

        File name: recovered_all_oecd.html
        """
        oecd_deaths = self.deaths[self.deaths['OECD'] == True]
        oecd_cases = self.cases[self.cases['OECD'] == True]

        df = self.create_df(oecd_deaths, oecd_cases, '2020-02-01')

        # List of two colors to get alternating row colors in the table
        colors = self.color_list * len(df['country'])
        colors = colors[:len(df['country'])]

        table = self.plot_table(df, 'All Data', colors)

        table.write_html(self.path + 'recovered_all_OECD.html',
                         config=self.table_config)

    def plot_autumn_oecd(self):
        """Create table showing recovery rates since autumn 2020 in OECD
        countries.

        File name: recovered_autumn_OECD.html
        """
        oecd_deaths = self.deaths[self.deaths['OECD'] == True]
        oecd_cases = self.cases[self.cases['OECD'] == True]

        df = self.create_df(oecd_deaths, oecd_cases, '2020-08-01')

        # List of two colors to get alternating row colors in the table
        colors = self.color_list * len(df['country'])
        colors = colors[:len(df['country'])]

        table = self.plot_table(df, 'Since August 1st', colors)

        table.write_html(self.path + 'recovered_autumn_OECD.html',
                         config=self.table_config)


def plot(data):
    """Initiate SummaryTables, LastTwoWeeks and Recovered class and run
    methods to create the tables.
    """
    tables = SummaryTables(data)
    tables.set_latest_date()
    tables.plot_total_deaths()
    tables.plot_daily_deaths()
    tables.plot_total_deaths_per_million()
    tables.plot_daily_deaths_per_million()
    tables.plot_total_cases()
    tables.plot_daily_cases()
    tables.plot_total_cases_per_million()
    tables.plot_daily_cases_per_million()

    two_week = LastTwoWeeks(data)
    two_week.plot_deaths()
    two_week.plot_cases()

    recovered = Recovered(data)
    recovered.plot_all()
    recovered.plot_autumn_all()
    recovered.plot_oecd_all()
    recovered.plot_autumn_oecd()
