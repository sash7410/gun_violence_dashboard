from dash.dependencies import Input, Output
import plotly.graph_objects as go
from src.data_loader import load_data

# Load data
police_shootings, mass_shootings, background_checks, state_gun_deaths = load_data()

def register_callbacks(app):

    @app.callback(
        [Output('total-mass-incidents', 'children'),
         Output('total-victims', 'children'),
         Output('total-police-incidents', 'children')],
        [Input('year-filter', 'value'), Input('state-filter', 'value')]
    )
    def update_stats(year, state):
        filtered_mass = mass_shootings[mass_shootings['Year'] == year]
        if state != 'All':
            filtered_mass = filtered_mass[filtered_mass['Location'].str.contains(state)]
        filtered_police = police_shootings[police_shootings['year'] == year]
        if state != 'All':
            filtered_police = filtered_police[filtered_police['Location_of_death_state'] == state]

        return (
            f"{len(filtered_mass):,}",
            f"{filtered_mass['Totalvictims'].sum():,}",
            f"{len(filtered_police):,}"
        )

    @app.callback(
        Output('monthly-trend', 'figure'),
        [Input('year-filter', 'value'), Input('state-filter', 'value')]
    )
    def update_monthly_trend(year, state):
        filtered_mass = mass_shootings[mass_shootings['Year'] == year]
        if state != 'All':
            filtered_mass = filtered_mass[filtered_mass['Location'].str.contains(state)]
        filtered_police = police_shootings[police_shootings['year'] == year]
        if state != 'All':
            filtered_police = filtered_police[filtered_police['Location_of_death_state'] == state]

        mass_monthly = filtered_mass.groupby('month').size()
        police_monthly = filtered_police['parsed_date'].dt.month.value_counts()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=list(range(1, 13)),
            y=[mass_monthly.get(i, 0) for i in range(1, 13)],
            name='Mass Shootings',
            mode='lines+markers',
            line=dict(color='#e74c3c')
        ))

        fig.add_trace(go.Scatter(
            x=list(range(1, 13)),
            y=[police_monthly.get(i, 0) for i in range(1, 13)],
            name='Police Shootings',
            mode='lines+markers',
            line=dict(color='#3498db')
        ))

        fig.update_layout(
            title='Monthly Incident Trends',
            xaxis_title='Month',
            yaxis_title='Number of Incidents',
            xaxis=dict(ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                       tickvals=list(range(1, 13))),
            hovermode='x'
        )

        return fig

    @app.callback(
        Output('state-comparison', 'figure'),
        [Input('year-filter', 'value')]
    )
    def update_state_comparison(year):
        filtered_police = police_shootings[police_shootings['year'] == year]
        state_counts = filtered_police['Location_of_death_state'].value_counts().head(10)

        fig = go.Figure(data=[
            go.Bar(x=state_counts.index, y=state_counts.values)
        ])

        fig.update_layout(
            title='Top 10 States by Police Incidents',
            xaxis_title='State',
            yaxis_title='Number of Incidents'
        )

        return fig

    # Add new callback for the map
    @app.callback(
        Output('map-view', 'figure'),
        [Input('map-type', 'value'),
         Input('year-filter', 'value')]
    )
    def update_map(map_type, year):
        fig = go.Figure()

        if map_type == 'mass_shootings':
            filtered_data = mass_shootings[mass_shootings['Year'] == year]

            fig.add_trace(go.Scattergeo(
                lon=filtered_data['longitude'],
                lat=filtered_data['latitude'],
                mode='markers',
                marker=dict(
                    size=filtered_data['Totalvictims'] * 2,
                    color='#e74c3c',
                    opacity=0.6
                ),
                text=filtered_data.apply(
                    lambda
                        row: f"Location: {row['Location']}<br>Victims: {row['Totalvictims']}<br>Date: {row['Date'].strftime('%Y-%m-%d')}",
                    axis=1
                ),
                hoverinfo='text',
                name='Mass Shootings'
            ))

        elif map_type == 'police_shootings':
            filtered_data = police_shootings[police_shootings['year'] == year]
            state_counts = filtered_data['Location_of_death_state'].value_counts()

            fig.add_trace(go.Choropleth(
                locationmode='USA-states',
                locations=state_counts.index,
                z=state_counts.values,
                colorscale='Reds',
                text=state_counts.index + '<br>Incidents: ' + state_counts.values.astype(str),
                hoverinfo='text',
                colorbar_title='Incidents'
            ))

        elif map_type == 'gun_deaths':
            filtered_data = state_gun_deaths[state_gun_deaths['year'] == year]

            fig.add_trace(go.Scattergeo(
                lon=filtered_data['lng'],
                lat=filtered_data['lat'],
                mode='markers',
                marker=dict(
                    size=4,
                    color='#e74c3c',
                    opacity=0.4
                ),
                text=filtered_data.apply(
                    lambda row: f"Name: {row['name']}<br>Age: {row['age']}<br>Location: {row['city']}, {row['state']}",
                    axis=1
                ),
                hoverinfo='text',
                name='Gun Deaths'
            ))

        fig.update_layout(
            geo=dict(
                scope='usa',
                projection_type='albers usa',
                showland=True,
                landcolor='rgb(217, 217, 217)',
                showlakes=True,
                lakecolor='rgb(255, 255, 255)',
                subunitcolor='rgb(255, 255, 255)'
            ),
            title=dict(
                text=f"{map_type.replace('_', ' ').title()} in {year}",
                x=0.5
            ),
            height=700,
            margin=dict(l=0, r=0, t=30, b=0)
        )

        return fig
