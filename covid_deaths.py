# ----------------------------------------------------------------------
# Script, to be imported as a module into main.py, which downloads and
# prepares data on COVID-19 deaths.
# ----------------------------------------------------------------------

import pandas as pd
import numpy as np

from countre import country_info


class DeathsData:
    """Class to download deaths data from CSSE and prepare it for
    plotting on graphs.
    """
    def __init__(self):
        pass

    def download_data(self):
        """Download the csv file containing data on deaths and return as
        a Data Frame."""
        url_deaths = ("https://raw.githubusercontent.com/CSSEGISandData/"
                      "COVID-19/master/csse_covid_19_data/"
                      "csse_covid_19_time_series/"
                      "time_series_covid19_deaths_global.csv")
        deaths = pd.read_csv(url_deaths)
        return deaths

    def prepare_data_1(self):
        """Take the downloaded data and perform the first stage of
        cleaning.
        """
        deaths = self.download_data()

        # Each column from column 5 is date. These are melted into a
        # single date column.
        deaths = pd.melt(
            deaths,
            id_vars=['Province/State', 'Country/Region'],
            value_vars=deaths.columns[4:])

        deaths.columns = ['province_state', 'country', 'date', 'deaths']
        deaths['date'] = pd.to_datetime(deaths['date'], format='%m/%d/%y')

        # Group deaths by country as some countries as split into
        # regions / states.
        deaths = deaths.groupby(
            ['country', 'date'], as_index=False)['deaths'].sum()
        return deaths

    def merge_metrics(self):
        """Add ISO3 code, population, OECD / EU/EEA membership,
        continent, flag emoji, latitude and longitude for each country.
        """
        deaths = self.prepare_data_1()
        country_list = deaths['country'].unique()
        metrics = ['iso3', 'population', 'OECD', 'EU_EEA', 'continent', 'flag',
                   'latitude', 'longitude']

        # Use countre package to get metrics.
        metrics = pd.DataFrame(country_info(country_list, metrics))
        metrics = metrics.replace('', np.nan)
        metrics['country'] = country_list

        deaths = deaths.merge(metrics, on='country', how='left')
        deaths = deaths[deaths['iso3'] != 'no match']
        return deaths

    def prepare_data_2(self):
        """Perform the second stage of cleaning."""
        deaths = self.merge_metrics()

        deaths['deaths_per_million'] = (deaths['deaths'] / deaths['population']
                                        * 1000000)

        # Column with daily deaths calculated from cumulative deaths
        # column.
        deaths['daily'] = deaths.groupby('country')['deaths'].apply(
            lambda x: x.diff())

        # Revisements to the overall figures can lead to negative daily
        # deaths. Where this is the case, the daily deaths are set to 0.
        deaths['daily'] = np.where(deaths['daily'] < 0, 0 , deaths['daily'])

        deaths['daily_million'] = (deaths['daily'] / deaths['population']
                                   * 1000000)

        # 7 day rolling average of daily deaths
        deaths['7_day_average'] = deaths.groupby('country')['daily'].apply(
            lambda x: x.rolling(window=7, min_periods=1).mean())

        deaths['7_day_average_per_million'] = (deaths['7_day_average']
                                               / deaths['population']
                                               * 1000000)

        # Drops first date for each country as daily deaths can't be
        # calculated (0 for almost all countries anyway).
        deaths = deaths.dropna()

        # Column with dates in format 'Jan 01, 2000'
        deaths['date_string'] = [x.strftime('%b %d, %Y')
                                 for x in deaths['date']]

        # Create columns with thousand comma formatted str versions of
        # the figures. These are used in the graph labels as they are
        # easier to read.
        cols = ['deaths', 'deaths_per_million', 'daily', 'daily_million',
                '7_day_average', '7_day_average_per_million']
        for c in cols:
            str_list = [f'{x:,.2f}' for x in deaths[c]]
            str_list = [x[:-3] if x[-3:] == '.00' else x for x in str_list]
            deaths[c + '_str'] = str_list

        deaths = deaths.sort_values(['country', 'date'])

        return deaths

    def return_df(self):
        """Return the prepared Data Frame."""
        return self.prepare_data_2()


class DeathsContinents:
    """Class to take the prepared deaths Data Frame and create a new
    Data Frame with a breakdown of cases by continent.
    """
    def __init__(self, deaths):
        self.deaths = deaths

    def prepare_data(self):
        """Prepare and clean the data."""
        deaths = self.deaths.copy()
        continents_deaths = deaths[deaths['date'] > '2020-03-01'].copy()

        # Sum by continent and date
        continents_deaths = continents_deaths.groupby(
            ['continent', 'date'], as_index=False)[['deaths', 'daily']].sum()

        # Columns with percentage of total deaths and percentage of
        # daily deaths for each continent for each date.
        continents_deaths['%_total'] = (continents_deaths['deaths']
            / continents_deaths.groupby('date')['deaths'].transform(sum) * 100)
        continents_deaths['%_daily'] = (continents_deaths['daily']
            / continents_deaths.groupby('date')['daily'].transform(sum) * 100)
        return continents_deaths

    def return_df(self):
        """Return the prepared Data Frame."""
        return self.prepare_data()


class ExcessDeathsData:
    """Class to download and prepare the data from The Economist on
    excess deaths.
    """
    def __init__(self):
        pass

    def download_data(self):
        """Download the csv file containing data on excess deaths and
        return as a Data Frame."""
        url_excess = ("https://raw.githubusercontent.com/TheEconomist/"
                      "covid-19-excess-deaths-tracker/master/output-data/"
                      "excess-deaths/all_weekly_excess_deaths.csv")
        excess = pd.read_csv(url_excess)
        return excess

    def prepare_data(self):
        """Prepare and clean the downloaded data."""
        excess = self.download_data()

        # Percentage changes are in decimal form so are multiplied by
        # 100.
        excess['excess_deaths_pct_change'] = excess['excess_deaths_pct_change'] * 100

        # Some countries have regional data so this is dropped from the
        # data frame.
        drop_regions = ['United States', 'Spain', 'Britain',
                        'France', 'Italy', 'Chile']
        for country in drop_regions:
            excess = excess.drop(( excess[ (excess['country'] == country)
                                   & (excess['region'] != country) ].index ))

        excess = excess.replace('Britain', 'United Kingdom')
        excess = excess.sort_values(['country', 'year', 'week'])
        return excess

    def merge_info(self):
        """Add ISO3 codes and flag emojis for each country."""
        excess = self.prepare_data()
        excess['iso3'] = country_info(excess['country'], 'iso3')
        excess['flag'] = country_info(excess['country'], 'flag')
        return excess

    def return_df(self):
        """Return the prepared Data Frame."""
        return self.merge_info()
