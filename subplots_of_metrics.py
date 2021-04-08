from datetime import date, timedelta
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import statsmodels.api as sm
import statsmodels.formula.api as smf
import scipy

from countre import country_info

cases_url = ("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
             "csse_covid_19_data/csse_covid_19_time_series/"
             "time_series_covid19_confirmed_global.csv")
deaths_url = ("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/"
              "master/csse_covid_19_data/csse_covid_19_time_series/"
              "time_series_covid19_deaths_global.csv")

# -----------
# Deaths data
# -----------

deaths = pd.read_csv(deaths_url)
deaths = pd.melt(
    deaths,
    id_vars=['Province/State','Country/Region'],
    value_vars=deaths.columns[4:])
deaths.columns = ['province_state', 'country', 'date', 'deaths']
deaths['date'] = pd.to_datetime(deaths['date'], format='%m/%d/%y')
deaths = deaths.groupby(['country', 'date'], as_index=False)['deaths'].sum()
info = pd.DataFrame({
    'country':deaths['country'].unique(),
    'iso3':country_info(deaths['country'].unique(), 'iso3'),
    'population_2019':country_info(deaths['country'].unique(), 'population_2019', np.nan)
}).replace('', np.nan)
deaths = deaths.merge(info, on='country', how='left')
deaths = deaths[deaths['iso3'] != 'no match']
deaths['deaths_per_million'] = (deaths['deaths'] / deaths['population_2019']
                                * 1000000)
deaths_max = deaths[deaths['date'] == deaths['date'].max()]
deaths_max = deaths_max.drop(deaths_max[deaths_max['deaths_per_million'] == 0].index)

# ----------
# Cases data
# ----------

cases = pd.read_csv(cases_url)
cases = pd.melt(
    cases,
    id_vars=['Province/State','Country/Region'],
    value_vars=cases.columns[4:])
cases.columns = ['province_state', 'country', 'date', 'cases']
cases['date'] = pd.to_datetime(cases['date'], format='%m/%d/%y')
cases = cases.groupby(['country', 'date'], as_index=False)['cases'].sum()
info = pd.DataFrame({
    'country':cases['country'].unique(),
    'iso3':country_info(cases['country'].unique(), 'iso3'),
    'population_2019':country_info(cases['country'].unique(), 'population_2019', np.nan)
}).replace('', np.nan)
cases = cases.merge(info, on='country', how='left')
cases = cases[cases['iso3'] != 'no match']
cases['cases_per_million'] = (cases['cases'] / cases['population_2019']
                              * 1000000)

cases_max = cases[cases['date'] == cases['date'].max()]

# ------------
# Metrics data
# ------------

metrics = pd.read_csv('data/metrics.csv')
deaths_max = deaths_max.merge(metrics, on='iso3', how='left')
cases_max = cases_max.merge(metrics, on='iso3', how='left')

deaths_max['land_area'] = country_info(deaths_max['iso3'], 'land_area', np.nan)
deaths_max['land_area'] = deaths_max['land_area'].replace('', np.nan)
deaths_max['density'] = deaths_max['population_2019'] / deaths_max['land_area']

# Stringency Index
stringency = pd.read_csv('data/covid-stringency-index.csv',
                         usecols=[1,2,3],
                         names=['iso3', 'date', 'stringency_index'],
                         skiprows=1)
stringency['date'] = pd.to_datetime(stringency['date'], format='%Y-%m-%d')
deaths = deaths.merge(stringency, on=['iso3', 'date'], how='left')

# --------------
# Graph template
# --------------

template=dict(
    layout=go.Layout(
        title=dict(
            x=0,
            xref='paper',
            y=0.96,
            yref='container',
            yanchor='top'
        ),
        xaxis=dict(
            showline=True,
            linewidth=1.5,
            linecolor='black',
            gridwidth=1,
            gridcolor='whitesmoke',
            zerolinewidth=1,
            zerolinecolor='whitesmoke'
        ),
        yaxis=dict(
            showline=True,
            linewidth=1.5,
            linecolor='black',
            gridwidth=1,
            gridcolor='whitesmoke'
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        hovermode='closest'
    )
)

# -------------
# All countries
# -------------

metrics = ['percent_overweight', 'median_age', 'percent_1_household_member',
           'per_house', 'percent_urban', 'cigarettes',
           'democracy_score', 'healthcare_percent_gdp', 'pm25', 'gini',
           'political_trust', 'ghs_overall']
titles = ['% Overweight (BMI > 25)', 'Median Age', '% Single Household',
          'People Per House', '% Living in Urban Area',
          'Average Annual Cigarettes per Person', 'Democracy Score',
          'Healthcare as % of GDP', 'PM2.5', 'Gini Coefficient',
          'Political Trust', 'GHS Overall Score']

rows = [1,1,1,2,2,2,3,3,3,4,4,4]
cols = [1,2,3,1,2,3,1,2,3,1,2,3]

# Coordinates for annotations
anno_x = [57, 40, 30, 6, 75, 4000, 8, 12, 75, 50, 5, 60]
anno_y = [0.3, 1, 1, 3.3, 0.5, 1, 0.5, 0.5, 3.5, 1, 0, 0]

fig = make_subplots(rows=4, cols=3, subplot_titles=titles)

for metric, row, col, a_x, a_y in zip(metrics, rows, cols, anno_x, anno_y):

    # Calculate regression line and R2
    formula = 'np.log(deaths_per_million) ~ ' + metric
    results = smf.ols(formula , deaths_max).fit()
    m = results.params[1]
    c = results.params[0]
    r = results.rsquared
    x = np.linspace(deaths_max[metric].min(), deaths_max[metric].max())
    y = np.exp(m*x+c)

    # Plot scatter for metric vs. deaths per million
    fig.add_trace(
        go.Scatter(
            x=list(deaths_max[metric]),
            y=list(deaths_max['deaths_per_million']),
            mode='markers',
            text=deaths_max['country'],
            showlegend=False,
            hovertemplate=
            '<extra></extra>'
            +'<b>%{text}</b><br>'
            +'Deaths per million: %{y:.2f}'
        ), row, col
    )

    # Plot OLS regression line
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            showlegend=False,
            hoverinfo='skip'
        ), row, col
    )

    # Add annotations for line formula and R2
    fig.add_annotation(
        x=a_x, y=a_y, xanchor='left', yanchor='top',
        text=("y = " + str(round(m,2)) + "x + " + str(round(c,2))
              + "<br>R<sup>2</sup> = " + str(round(r,2))),
        showarrow=False,
        align='left', row=row, col=col
    )

# Add x-axis title for each subplot
fig.update_xaxes(title="% Overweight", row=1, col=1)
fig.update_xaxes(title="Median Age", row=1, col=2)
fig.update_xaxes(title="% Single Household", row=1, col=3)
fig.update_xaxes(title="People Per House", row=2, col=1)
fig.update_xaxes(title="% Urban", row=2, col=2)
fig.update_xaxes(title="Cigarettes Per Person", row=2, col=3)
fig.update_xaxes(title="Democracy Score", row=3, col=1)
fig.update_xaxes(title="% GDP", row=3, col=2)
fig.update_xaxes(title="PM2.5", row=3, col=3)
fig.update_xaxes(title="Gini Coefficient", row=4, col=1)
fig.update_xaxes(title="Poltical Trust", row=4, col=2)
fig.update_xaxes(title="GHS Score", row=4, col=3)

fig.update_xaxes(title_standoff=10)
fig.update_yaxes(type='log')

fig.update_layout(
    template=template,
    title=("<b>Various Metrics vs. COVID-19 Deaths per Million (log scale)"
           "<br>All Countries</b>"),
    height=1000,
    margin=dict(t=120)
)

fig.write_html('graphs/analysis/subplots_world.html')

# --------------
# OECD countries
# --------------

oecd = deaths_max.copy()
oecd['OECD'] = country_info(oecd['iso3'], 'OECD')
oecd = oecd[oecd['OECD']==True]

# Coordinates for annotations
anno_x = [40, 30, 10, 3, 60, 3500, 5, 12, 30, 38, 2.8, 60]
anno_y = [2, 1.5, 1.5, 2, 2, 2, 2, 2, 2, 2, 1.5, 1]

fig = make_subplots(rows=4, cols=3, subplot_titles=titles)

for metric, row, col, a_x, a_y in zip(metrics, rows, cols, anno_x, anno_y):

    # Calculate regression line and R2
    formula = 'np.log(deaths_per_million) ~ ' + i
    results = smf.ols(formula , oecd).fit()
    m = results.params[1]
    c = results.params[0]
    r = results.rsquared
    x = np.linspace(oecd[metric].min(), oecd[metric].max())
    y = np.exp(m*x+c)

    # Plot scatter for metric vs. deaths per million
    fig.add_trace(
        go.Scatter(
            x=list(oecd[metric]),
            y=list(oecd['deaths_per_million']),
            mode='markers',
            text=oecd['country'],
            showlegend=False,
            hovertemplate=
            '<extra></extra>'
            +'<b>%{text}</b><br>'
            +'Deaths per million: %{y:.2f}'
        ), row, col
    )

    # Plot OLS regression line
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            showlegend=False,
            hoverinfo='skip'
        ), row, col
    )

    # Add annotations for line formula and R2
    fig.add_annotation(
        x=a_x, y=a_y, xanchor='left', yanchor='top',
        text=("y = " + str(round(m,2)) + "x + " + str(round(c,2))
              + "<br>R<sup>2</sup> = " + str(round(r,2))),
        showarrow=False,
        align='left', row=row, col=col
    )

# Add x-axis title for each subplot
fig.update_xaxes(title="% Overweight", row=1, col=1)
fig.update_xaxes(title="Median Age", row=1, col=2)
fig.update_xaxes(title="% Single Household", row=1, col=3)
fig.update_xaxes(title="People Per House", row=2, col=1)
fig.update_xaxes(title="% Urban", row=2, col=2)
fig.update_xaxes(title="Cigarettes Per Person", row=2, col=3)
fig.update_xaxes(title="Democracy Score", row=3, col=1)
fig.update_xaxes(title="% GDP", row=3, col=2)
fig.update_xaxes(title="PM2.5", row=3, col=3)
fig.update_xaxes(title="Gini Coefficient", row=4, col=1)
fig.update_xaxes(title="Poltical Trust", row=4, col=2)
fig.update_xaxes(title="GHS Score", row=4, col=3)

fig.update_xaxes(title_standoff=10)
fig.update_yaxes(type='log')

fig.update_layout(
    template=template,
    title=("<b>Various Metrics vs. COVID-19 Deaths per Million (log scale)"
           "<br>OECD Countries</b>"),
    height=1000,
    margin=dict(t=120)
)

fig.write_html('graphs/analysis/subplots_oecd.html')
