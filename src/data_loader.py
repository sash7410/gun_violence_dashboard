import pandas as pd
from config import (
    POLICE_SHOOTINGS_FILE,
    MASS_SHOOTINGS_FILE,
    BACKGROUND_CHECKS_FILE,
    STATE_GUN_DEATHS_FILE
)

def load_data():
    try:
        police_shootings = pd.read_csv(POLICE_SHOOTINGS_FILE, encoding='latin1')
        # Data preprocessing for police shootings because dates are in ""
        police_shootings['Date_of_injury_resulting_in_death_month_day_year'] = (
            police_shootings['Date_of_injury_resulting_in_death_month_day_year']
            .str.replace('"', '')
            .str.strip()
        )
        police_shootings['parsed_date'] = pd.to_datetime(
            police_shootings['Date_of_injury_resulting_in_death_month_day_year'],
            format='%B %d, %Y',
            errors='coerce'
        )
        police_shootings['year'] = police_shootings['parsed_date'].dt.year

        mass_shootings = pd.read_csv(MASS_SHOOTINGS_FILE, encoding='latin1')
        mass_shootings['Date'] = pd.to_datetime(mass_shootings['Date'].str.strip(), format='%m/%d/%y', errors='coerce')
        mass_shootings['Year'] = mass_shootings['Date'].dt.year
        mass_shootings['month'] = mass_shootings['Date'].dt.month

        background_checks = pd.read_csv(BACKGROUND_CHECKS_FILE, encoding='latin1')
        background_checks['year'] = pd.to_datetime(background_checks['month'], format='%Y-%m', errors='coerce').dt.year
        background_checks['month'] = pd.to_datetime(background_checks['month'], format='%Y-%m', errors='coerce').dt.month
        # unfortunately have data only from 2012-2013 for the below
        state_gun_deaths = pd.read_csv(STATE_GUN_DEATHS_FILE, encoding='latin1')
        state_gun_deaths['date'] = pd.to_datetime(state_gun_deaths['date'], errors='coerce')
        state_gun_deaths['year'] = state_gun_deaths['date'].dt.year
        state_gun_deaths['month'] = state_gun_deaths['date'].dt.month

        return police_shootings, mass_shootings, background_checks, state_gun_deaths

    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None
