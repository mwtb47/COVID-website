# ----------------------------------------------------------------------
# Script, to be imported as a module into main.py, which downloads and
# prepares data on COVID-19 deaths by US state.
# ----------------------------------------------------------------------

import pandas as pd
import plotly.graph_objects as go
import numpy as np


class UnitedStatesData:
    """Class to download and prepare COVID-19 deaths data from CSSE for
    US states.
    """
    def __init__(self):
        pass

    def download_data(self):
        """Download the csv file containing data on deaths and return as
        a Data Frame."""
        url_usa = ("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/"
                   "master/csse_covid_19_data/csse_covid_19_time_series/"
                   "time_series_covid19_deaths_US.csv")
        usa = pd.read_csv(url_usa)
        return usa

    def prepare_data_1(self):
        """Perform the first stage of preparation."""
        usa = self.download_data()

        # Get list of all dates and melt them to single column.
        usa = pd.melt(
            usa,
            id_vars=['Province_State'],
            value_vars=usa.columns[12:],
            var_name='date',
            value_name='deaths')

        # Group deaths by state for each date as they are collected at
        # a local level.
        usa = usa.groupby(
            ['Province_State', 'date'], as_index = False)['deaths'].sum()

        usa['date'] = pd.to_datetime(usa['date'], format = '%m/%d/%y')

        # Create column with date string in format 'Jan 01, 2000' for
        # ease of reading in maps.
        usa['str_date'] = [x.strftime('%b %d, %Y') for x in usa['date']]

        usa.columns = ['state', 'date', 'deaths', 'str_date']

        return usa

    def merge_metrics(self):
        """Read in csv file containing metrics for the US states,
        including the population of each state.
        """
        usa = self.prepare_data_1()
        us_states = pd.read_csv('data/us_states_data.csv')
        usa = usa.merge(us_states, on='state', how='left').dropna()

        return usa

    def prepare_data_2(self):
        """Perform the second stage of preparation."""
        usa = self.merge_metrics()
        usa['deaths_per_100k'] = usa['deaths'] / usa['population'] * 100000
        usa = usa.sort_values('date')

        # For each date, rank states by total deaths and deaths per
        # 100,000.
        usa['rank_total'] = usa.groupby('date')['deaths'].rank(
            method='dense', ascending=False).astype(int)
        usa['rank_per_100k'] = usa.groupby('date')['deaths_per_100k'].rank(
            method='dense', ascending=False).astype(int)
        
        usa['deaths_str'] = [f'{x:,}' for x in usa['deaths']]
        usa['deaths_per_100k_str'] = [f'{x:,.2f}' 
                                      for x in usa['deaths_per_100k']]

        return usa

    def return_df(self):
        """Return the prepared Data Frame."""
        return self.prepare_data_2()
