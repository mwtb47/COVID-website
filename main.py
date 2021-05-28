# ----------------------------------------------------------------------
# Main script which import modules containing classes to download,
# prepare and plot data on various COVID-19 metrics as graphs, tables
# and maps.
# ----------------------------------------------------------------------

import plotly.graph_objects as go

import config
import covid_cases
import covid_deaths
import covid_maps
import covid_plot_lines
import covid_regions
import covid_tables
import covid_usa
import covid_vaccinations


# Template for line graphs.
line_template=dict(
    layout=go.Layout(
        title=dict(
            x=0,
            xref='paper',
            y=0.96,
            yref='container',
            yanchor='top'
        ),
        hovermode='closest',
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(
            showline=True,
            linewidth=2,
            linecolor='black',
            gridcolor='whitesmoke',
            gridwidth=1
        ),
        yaxis=dict(
            showline=True,
            linewidth=2,
            linecolor='black',
            gridcolor='whitesmoke',
            gridwidth=1
        )
    )
)

# Colours for graph traces.
colours = [
    'red', 'gold', 'seagreen', 'mediumvioletred', 'dodgerblue', 'indianred',
    'orange', 'forestgreen', 'purple', 'steelblue', 'salmon', 'sandybrown',
    'mediumseagreen', 'mediumorchid', 'cornflowerblue'
] * 20

# Mapbox access key
mapbox_key = config.mapbox_key


def get_data():
    """Run methods which download and prepare Data Frames, returning
    them in a dictionary of Data Frames.
    """
    cases = covid_cases.CasesData().return_df()
    continent_cases = covid_cases.CasesContinents(cases).return_df()
    deaths = covid_deaths.DeathsData().return_df()
    continent_deaths = covid_deaths.DeathsContinents(deaths).return_df()
    excess = covid_deaths.ExcessDeathsData().return_df()
    vaccine = covid_vaccinations.VaccineData().return_df()
    usa = covid_usa.UnitedStatesData().return_df()

    return {'cases': cases, 'deaths': deaths,
            'continent_cases': continent_cases,
            'continent_deaths': continent_deaths,
            'excess_deaths': excess,
            'vaccine': vaccine, 'usa': usa}


def main(line_template, colours, mapbox_key):
    """Run get_data and then the functions to plot these data as graphs,
    tables and maps.
    """
    data = get_data()

    covid_plot_lines.plot(data, line_template, colours)
    covid_vaccinations.plot(data, line_template)
    covid_regions.plot(data)
    covid_maps.plot(data, mapbox_key)
    covid_tables.plot(data)

    
if __name__=="__main__":
    main(line_template, colours, mapbox_key)
