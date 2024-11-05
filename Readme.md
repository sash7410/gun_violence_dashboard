
# Gun Violence Analysis Dashboard 🎯

An interactive visualization dashboard that analyzes and displays gun violence data across the United States, featuring geographic mapping, temporal trends, and comparative state-level statistics.


## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gun_violence_dashboard.git
cd gun_violence_dashboard
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Run the dashboard:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:8050
```

## Features 🌟

- **Geographic Views**: Interactive maps showing distribution of incidents across the US
- **Temporal Analysis**: Yearly and monthly trend visualization
- **State Comparison**: Comparative analysis between states
- **Multiple Data Views**: 
  - Mass shootings map with victim count
  - Gun deaths distribution
  - Police incidents by state
  - Monthly trend charts
  - State-wise statistics

## Interactive Elements 🔄

- Year selection dropdown
- State filtering
- Incident type toggle
- Interactive tooltips
- Dynamic chart updates
- Hover interactions for detailed information

## Technologies Used 💻

- Python 3.x
- Dash
- Plotly
- Pandas
- NumPy
- HTML/CSS

## Data Sources 📁

The dashboard utilizes four comprehensive datasets:
- Mass Shootings Dataset: Records of mass shooting incidents
- Gun Deaths Dataset: Information on gun-related fatalities
- Police Incidents Dataset: Records of police-involved shootings
- Background Checks Dataset: Firearm background check statistics

## Live Demo 🌐

View the live dashboard at: https://gun-violence-dashboard.onrender.com/

## Author 👤

Sashank RM - sr6890@nyu.edu

## Acknowledgments 🙏

- NYU Tandon School of Engineering
- CS-GY 6313 Information Visualization course
- Built using Plotly and Dash