# ----------------------------------------------------------------------
# Script, to be imported as a module into main.py, which downloads and
# prepares data on COVID-19 cases.
# ----------------------------------------------------------------------

import pandas as pd
import numpy as np

from countre import country_info


class CasesData:
    """Class to download cases data from CSSE and prepare it for
    plotting on graphs.
    """
    def __init__(self):
        pass

    def download_data(self):
        """Download the csv file containing data on cases and return as
        a Data Frame."""
        url_cases = ("https://raw.githubusercontent.com/CSSEGISandData/"
                     "COVID-19/master/csse_covid_19_data/"
                     "csse_covid_19_time_series/"
                     "time_series_covid19_confirmed_global.csv")
        cases = pd.read_csv(url_cases)
        return cases

    def prepare_data_1(self):
        """Take the downloaded data and perform the first stage of
        cleaning.
        """
        cases = self.download_data()

        # Each column from column 5 is date. These are melted into a
        # single date column.
        cases = pd.melt(
            cases,
            id_vars=['Province/State', 'Country/Region'],
            value_vars=cases.columns[4:])

        cases.columns = ['province_state', 'country', 'date', 'cases']
        cases['date'] = pd.to_datetime(cases['date'], format='%m/%d/%y')

        # Group cases by country as some countries as split into
        # regions / states.
        cases = cases.groupby(
            ['country', 'date'], as_index=False)['cases'].sum()
        return cases

    def merge_metrics(self):
        """Add ISO3 code, population, OECD / EU/EEA membership,
        continent, flag emoji, latitude and longitude for each country.
        """
        cases = self.prepare_data_1()
        country_list = cases['country'].unique()
        metrics = ['iso3', 'population', 'OECD', 'EU_EEA', 'continent', 'flag',
                   'latitude', 'longitude']

        # Use countre package to get metrics.
        metrics = pd.DataFrame(country_info(country_list, metrics))
        metrics = metrics.replace('', np.nan)
        metrics['country'] = country_list

        cases = cases.merge(metrics, on='country', how='left')
        cases = cases[cases['iso3'] != 'no match']
        return cases

    def prepare_data_2(self):
        """Perform the second stage of cleaning."""
        cases = self.merge_metrics()

        cases['cases_per_million'] = (cases['cases'] / cases['population']
                                      * 1000000)

        # Column with daily cases calculated from cumulative cases
        # column.
        cases['daily'] = cases.groupby('country')['cases'].apply(
            lambda x: x.diff())

        # Revisements to the overall figures can lead to negative daily
        # cases. Where this is the case, the daily cases are set to 0.
        cases['daily'] = np.where(cases['daily'] < 0, 0 , cases['daily'])

        cases['daily_million'] = (cases['daily'] / cases['population']
                                  * 1000000)

        # 7 day rolling average of daily cases
        cases['7_day_average'] = cases.groupby('country')['daily'].apply(
            lambda x: x.rolling(window=7, min_periods=1).mean())

        cases['7_day_average_per_million'] = (cases['7_day_average']
                                              / cases['population']
                                              * 1000000)

        # Drops first date for each country as daily cases can't be
        # calculated (0 for almost all countries anyway).
        cases = cases.dropna()

        # Column with dates in format 'Jan 01, 2000' for ease of reading
        # on graphs.
        cases['date_string'] = [x.strftime('%b %d, %Y') for x in cases['date']]

        # Create columns with thousand comma formatted str versions of
        # the figures. These are used in the graph labels as they are
        # easier to read.
        cols = ['cases', 'cases_per_million', 'daily', 'daily_million',
                '7_day_average', '7_day_average_per_million']
        for c in cols:
            str_list = [f'{x:,.2f}' for x in cases[c]]
            str_list = [x[:-3] if x[-3:] == '.00' else x for x in str_list]
            cases[c + '_str'] = str_list

        cases = cases.sort_values(['country', 'date'])
        return cases

    def return_df(self):
        """Return the prepared Data Frame."""
        return self.prepare_data_2()


class CasesContinents:
    """Class to take the prepared cases Data Frame and create a new
    Data Frame with a breakdown of cases by continent.
    """
    def __init__(self, cases):
        self.cases = cases

    def prepare_data(self):
        """Prepare and clean the data."""
        cases = self.cases.copy()
        continents_cases = cases[cases['date'] > '2020-03-01'].copy()

        # Sum by continent and date
        continents_cases = continents_cases.groupby(
            ['continent', 'date'], as_index=False)[['cases', 'daily']].sum()

        # Columns with percentage of total cases and percentage of daily
        # cases for each continent for each date.
        continents_cases['%_total'] = (continents_cases['cases']
            / continents_cases.groupby('date')['cases'].transform(sum) * 100)
        continents_cases['%_daily'] = (continents_cases['daily']
            / continents_cases.groupby('date')['daily'].transform(sum) * 100)
        return continents_cases

    def return_df(self):
        """Return the prepared Data Frame."""
        return self.prepare_data()
