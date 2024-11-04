from dash import html, dcc
from src.data_loader import load_data

# Load data once for use in the layout
police_shootings, mass_shootings, background_checks, state_gun_deaths = load_data()

def create_layout(app):
    return html.Div([
    html.H1("Gun Violence Analysis Dashboard", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),

    dcc.Tabs([
        #  Dashboard Tab
        dcc.Tab(label='Analysis Dashboard', children=[
            html.Div([
                # Filters
                html.Div([
                    html.Div([
                        html.Label('Select Year'),
                        dcc.Dropdown(
                            id='year-filter',
                            options=[{'label': str(year), 'value': year} for year in
                                     sorted(mass_shootings['Year'].dropna().unique())],
                            value=int(mass_shootings['Year'].max()) if not mass_shootings['Year'].isna().all() else None
                        )
                    ], style={'width': '30%', 'display': 'inline-block'}),

                    html.Div([
                        html.Label('Select State'),
                        dcc.Dropdown(
                            id='state-filter',
                            options=[{'label': 'All States', 'value': 'All'}] +
                                    [{'label': state, 'value': state} for state in
                                     sorted(police_shootings['Location_of_death_state'].dropna().unique())],
                            value='All'
                        )
                    ], style={'width': '30%', 'display': 'inline-block', 'marginLeft': '5%'})
                ], style={'marginBottom': 30}),

                #stats
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4('Mass Shooting Incidents'),
                            html.H2(id='total-mass-incidents', children='0')
                        ], className='stats-card')
                    ], style={'width': '30%', 'display': 'inline-block'}),

                    html.Div([
                        html.Div([
                            html.H4('Total Victims'),
                            html.H2(id='total-victims', children='0')
                        ], className='stats-card')
                    ], style={'width': '30%', 'display': 'inline-block', 'marginLeft': '5%'}),

                    html.Div([
                        html.Div([
                            html.H4('Police Incidents'),
                            html.H2(id='total-police-incidents', children='0')
                        ], className='stats-card')
                    ], style={'width': '30%', 'display': 'inline-block', 'marginLeft': '5%'})
                ], style={'marginBottom': 30}),

                # Charts
                html.Div([
                    html.Div([dcc.Graph(id='monthly-trend')], style={'width': '48%', 'display': 'inline-block'}),
                    html.Div([dcc.Graph(id='state-comparison')],
                             style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
                ])
            ])
        ]),

        #  Map Tab
        dcc.Tab(label='Geographic View', children=[
            html.Div([
                #  Controls
                html.Div([
                    html.Label('Select Map Type:', style={'marginRight': '15px'}),
                    dcc.RadioItems(
                        id='map-type',
                        options=[
                            {'label': ' Mass Shootings', 'value': 'mass_shootings'},
                            {'label': ' Gun Deaths', 'value': 'gun_deaths'},
                            {'label': ' Police Incidents', 'value': 'police_shootings'}
                        ],
                        value='mass_shootings',
                        inline=True,
                        className='map-controls'
                    )
                ], style={'marginBottom': '20px', 'padding': '15px', 'backgroundColor': 'white',
                          'borderRadius': '5px'}),

                # Map
                dcc.Graph(id='map-view', style={'height': '700px'})
            ])
        ])
    ])
])