import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import plotly.io as pio
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt

# Set custom Plotly template for consistent styling
pio.templates["custom_dark"] = pio.templates["plotly_dark"].update({
    'layout': {
        'plot_bgcolor': 'rgba(28, 28, 36, 0.95)',
        'paper_bgcolor': 'rgba(28, 28, 36, 0.95)',
        'font': {'color': '#FFFFFF'},
        'title': {'font': {'color': '#FFFFFF', 'size': 24, 'family': 'Arial, sans-serif'}},
        'legend': {'bgcolor': 'rgba(28, 28, 36, 0.2)'}
    }
})

pio.templates["custom_light"] = pio.templates["plotly_white"].update({
    'layout': {
        'plot_bgcolor': 'rgba(250, 250, 250, 0.95)',
        'paper_bgcolor': 'rgba(250, 250, 250, 0.95)',
        'font': {'color': '#1E1E1E'},
        'title': {'font': {'color': '#1E1E1E', 'size': 24, 'family': 'Arial, sans-serif'}}
    }
})

# Set page configuration
st.set_page_config(
    page_title="COVID-19 Global Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get parameters from user
current_time = "2025-03-03 07:17:12"  # Use the provided timestamp
current_user = "FaheemKhan0817"  # Use the provided username

# Apply modern custom CSS for enhanced styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
        color: #333;
    }
    
    /* Header styling */
    .main-header {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #1E88E5 0%, #6A1B9A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 0.5rem;
        border-bottom: 4px solid #f0f0f0;
    }
    
    .sub-header {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #424242;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    /* Metric card styling with gradient backgrounds */
    .metric-row {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        padding: 1.5rem;
        transition: transform 0.2s;
        border-left: 5px solid;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    
    .metric-card-confirmed {
        border-left-color: #1E88E5;
    }
    
    .metric-card-deaths {
        border-left-color: #E53935;
    }
    
    .metric-card-recovered {
        border-left-color: #43A047;
    }
    
    .metric-card-mortality {
        border-left-color: #FFB300;
    }
    
    .metric-card-active {
        border-left-color: #7E57C2;
    }
    
    .metric-title {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 1rem;
        color: #757575;
        font-weight: 500;
        margin-bottom: 0.25rem;
    }
    
    .metric-value-confirmed {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 2.2rem;
        color: #1E88E5;
        font-weight: 700;
    }
    
    .metric-value-deaths {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 2.2rem;
        color: #E53935;
        font-weight: 700;
    }
    
    .metric-value-recovered {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 2.2rem;
        color: #43A047;
        font-weight: 700;
    }
    
    .metric-value-mortality {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 2.2rem;
        color: #FFB300;
        font-weight: 700;
    }
    
    .metric-value-active {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 2.2rem;
        color: #7E57C2;
        font-weight: 700;
    }
    
    .metric-trend {
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }
    
    .trend-up {
        color: #E53935;
    }
    
    .trend-down {
        color: #43A047;
    }
    
    /* Tab styling */
    .tab-subheader {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: #424242;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Custom chart container */
    .chart-container {
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        padding: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2E3951 0%, #1A1F2C 100%);
        color: white;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e0e0e0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Customizing Streamlit elements */
    .stSelectbox label, .stDateInput label {
        color: #1E88E5;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1E88E5 !important;
        color: white !important;
    }
    
    /* Data table styling */
    .dataframe {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* Status indicator */
    .status-indicator {
        padding: 6px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    .status-high {
        background-color: rgba(229, 57, 53, 0.2);
        color: #E53935;
    }
    
    .status-medium {
        background-color: rgba(255, 179, 0, 0.2);
        color: #FFB300;
    }
    
    .status-low {
        background-color: rgba(67, 160, 71, 0.2);
        color: #43A047;
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        position: relative;
        width: 80px;
        height: 80px;
    }
    
    /* Improve expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #1E88E5;
    }
    
    /* Custom divider */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, #1E88E5 0%, #6A1B9A 100%);
        margin: 2rem 0;
        border-radius: 2px;
    }
    
    /* Tooltip styling */
    .stTooltipIcon {
        color: #1E88E5;
    }
    </style>
""", unsafe_allow_html=True)

# Custom header with animated gradient effect
st.markdown("<h1 class='main-header'>🌍 COVID-19 Global Analytics Dashboard</h1>", unsafe_allow_html=True)

# Add a custom progress bar for data loading
def custom_progress_bar():
    progress_container = st.empty()
    for percent_complete in range(0, 101, 5):
        progress_container.progress(percent_complete)
        time.sleep(0.02)
    progress_container.empty()

with st.spinner("Loading global pandemic data..."):
    # Loading data with caching
    @st.cache_data(ttl=3600)
    def load_data():
        try:
            # Define paths based on file structure
            base_dir = os.path.dirname(os.path.abspath(__file__))
            processed_dir = os.path.join(base_dir, "data", "processed")
            
            # Load datasets
            confirmed_df = pd.read_csv(os.path.join(processed_dir, "confirmed_processed.csv"))
            deaths_df = pd.read_csv(os.path.join(processed_dir, "deaths_processed.csv"))
            recovered_df = pd.read_csv(os.path.join(processed_dir, "recovered_processed.csv"))
            
            return {
                'confirmed': confirmed_df,
                'deaths': deaths_df,
                'recovered': recovered_df
            }
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None

    # Load the data
    data = load_data()

# Show error if data loading failed
if data is None:
    st.error("Failed to load COVID-19 data files from data/processed directory.")
    st.info("Please ensure the data files are correctly located and formatted.")
    st.stop()

# Process JHU CSSE data format
def process_jhu_data(data):
    # Extract metadata columns and date columns
    meta_cols = ['Province/State', 'Country/Region', 'Lat', 'Long']
    
    confirmed_dates = [col for col in data['confirmed'].columns if col not in meta_cols]
    deaths_dates = [col for col in data['deaths'].columns if col not in meta_cols]
    recovered_dates = [col for col in data['recovered'].columns if col not in meta_cols]
    
    # Use the intersection of all datasets to ensure consistent dates
    common_dates = sorted(set(confirmed_dates).intersection(set(deaths_dates)).intersection(set(recovered_dates)))
    
    # Get unique countries - we'll aggregate provinces together
    countries = sorted(data['confirmed']['Country/Region'].unique())
    
    return meta_cols, common_dates, countries

try:
    meta_cols, date_columns, countries = process_jhu_data(data)
    
    # Create a sidebar with improved styling
    st.sidebar.markdown("### 🔍 Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Add time indicator to sidebar
    st.sidebar.markdown(f"**Last Data Update:** {current_time} UTC")
    
    # Enhanced country selection with search
    default_country = 'India' if 'India' in countries else countries[0]
    selected_country = st.sidebar.selectbox(
        "Select Country/Region",
        countries,
        index=countries.index(default_country),
        help="Choose a country to display its COVID-19 data"
    )
    
    # Parse dates for date range selector with better formatting
    parsed_dates = []
    for date_str in date_columns:
        try:
            # Handle JHU date format (e.g., "1/22/20")
            parsed_date = pd.to_datetime(date_str, format='%m/%d/%y')
            parsed_dates.append((date_str, parsed_date))
        except:
            continue
    
    parsed_dates.sort(key=lambda x: x[1])
    
    if parsed_dates:
        min_date = parsed_dates[0][1]
        max_date = parsed_dates[-1][1]
        
        # Better date range selection
        st.sidebar.markdown("#### 📅 Select Date Range")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                min_date,
                min_value=min_date,
                max_value=max_date,
                help="Select starting date for analysis"
            )
        with col2:
            end_date = st.date_input(
                "End Date", 
                max_date, 
                min_value=min_date,
                max_value=max_date,
                help="Select ending date for analysis"
            )
        
        # Filter dates based on selected range
        selected_date_strs = []
        for date_str, date_obj in parsed_dates:
            if start_date <= date_obj.date() <= end_date:
                selected_date_strs.append(date_str)
    else:
        st.warning("Could not parse date columns correctly")
        selected_date_strs = date_columns[:30]  # Just use the first 30 dates as fallback
    
    # Add visualization options to sidebar
    st.sidebar.markdown("#### 📊 Visualization Options")
    
    # Toggle for log scale
    use_log_scale = st.sidebar.checkbox("Use logarithmic scale", False, help="Toggle between linear and logarithmic scale")
    
    # Chart color theme
    color_theme = st.sidebar.selectbox(
        "Chart Theme",
        ["Light", "Dark", "Default"],
        help="Select the visual theme for charts"
    )
    
    # Map theme selection to plotly templates
    if color_theme == "Dark":
        chart_template = "custom_dark"
    elif color_theme == "Light":
        chart_template = "custom_light"
    else:
        chart_template = "plotly"
    
    # Chart height setting
    chart_height = st.sidebar.slider(
        "Chart Height",
        min_value=400,
        max_value=800,
        value=500,
        step=50,
        help="Adjust the height of charts"
    )
    
    # Add a comparison country option
    comparison_country = st.sidebar.selectbox(
        "Compare with Country (Optional)",
        ["None"] + [c for c in countries if c != selected_country],
        help="Select a country to compare with the primary selection"
    )
    
    # Process data for selected country (aggregating provinces)
    def get_country_data(df, country, date_cols):
        # Filter rows for the selected country
        country_data = df[df['Country/Region'] == country]
        
        if len(country_data) > 1:
            # If multiple provinces, sum them up
            aggregated = country_data[date_cols].sum(axis=0)
            return aggregated.values
        elif len(country_data) == 1:
            # If only one entry, return its values
            return country_data[date_cols].values[0]
        else:
            # No data for this country
            return np.zeros(len(date_cols))
    
    # Get data for the selected country
    confirmed_values = get_country_data(data['confirmed'], selected_country, selected_date_strs)
    deaths_values = get_country_data(data['deaths'], selected_country, selected_date_strs)
    
    # Handle recovered data which might have fewer countries
    if selected_country in data['recovered']['Country/Region'].values:
        recovered_values = get_country_data(data['recovered'], selected_country, selected_date_strs)
    else:
        recovered_values = np.zeros(len(selected_date_strs))
    
    # Get comparison country data if selected
    if comparison_country != "None":
        comp_confirmed_values = get_country_data(data['confirmed'], comparison_country, selected_date_strs)
        comp_deaths_values = get_country_data(data['deaths'], comparison_country, selected_date_strs)
        
        if comparison_country in data['recovered']['Country/Region'].values:
            comp_recovered_values = get_country_data(data['recovered'], comparison_country, selected_date_strs)
        else:
            comp_recovered_values = np.zeros(len(selected_date_strs))
    
    # Convert to proper dates for plotting
    plot_dates = [pd.to_datetime(d, format='%m/%d/%y') for d in selected_date_strs]
    
    # Create plotting dataframe with enhanced metrics
    plot_df = pd.DataFrame({
        'Date': plot_dates,
        'Confirmed': confirmed_values,
        'Deaths': deaths_values,
        'Recovered': recovered_values
    })
    
    # Add active cases calculation
    plot_df['Active'] = plot_df['Confirmed'] - plot_df['Deaths'] - plot_df['Recovered']
    plot_df['Active'] = plot_df['Active'].clip(lower=0)  # Ensure no negative active cases
    
    # Calculate daily new cases and 7-day averages
    plot_df['Daily Confirmed'] = plot_df['Confirmed'].diff().fillna(plot_df['Confirmed'].iloc[0])
    plot_df['Daily Deaths'] = plot_df['Deaths'].diff().fillna(plot_df['Deaths'].iloc[0])
    plot_df['Daily Recovered'] = plot_df['Recovered'].diff().fillna(plot_df['Recovered'].iloc[0])
    plot_df['Daily Active'] = plot_df['Active'].diff().fillna(plot_df['Active'].iloc[0])
    
    # Replace negative daily values with 0 (data corrections can cause negative values)
    plot_df['Daily Confirmed'] = plot_df['Daily Confirmed'].clip(lower=0)
    plot_df['Daily Deaths'] = plot_df['Daily Deaths'].clip(lower=0)
    plot_df['Daily Recovered'] = plot_df['Daily Recovered'].clip(lower=0)
    
    # Add more advanced metrics
    if len(plot_df) >= 14:
        # Growth rates (14-day)
        plot_df['Growth Rate (%)'] = (plot_df['Confirmed'] / plot_df['Confirmed'].shift(14) - 1) * 100
        
        # Case doubling time (in days)
        plot_df['Doubling Time'] = np.log(2) / (np.log(plot_df['Confirmed'] / plot_df['Confirmed'].shift(7)) / 7)
        plot_df['Doubling Time'] = plot_df['Doubling Time'].replace([np.inf, -np.inf], np.nan)
        
    # Calculate 7-day rolling averages
    if len(plot_df) >= 7:
        plot_df['7-Day Avg (Confirmed)'] = plot_df['Daily Confirmed'].rolling(window=7).mean()
        plot_df['7-Day Avg (Deaths)'] = plot_df['Daily Deaths'].rolling(window=7).mean()
        plot_df['7-Day Avg (Recovered)'] = plot_df['Daily Recovered'].rolling(window=7).mean()
        plot_df['7-Day Avg (Active)'] = plot_df['Daily Active'].rolling(window=7).mean()
    
    # Create comparison dataframe if needed
    if comparison_country != "None":
        comp_df = pd.DataFrame({
            'Date': plot_dates,
            'Confirmed': comp_confirmed_values,
            'Deaths': comp_deaths_values,
            'Recovered': comp_recovered_values
        })
        
        comp_df['Active'] = comp_df['Confirmed'] - comp_df['Deaths'] - comp_df['Recovered']
        comp_df['Active'] = comp_df['Active'].clip(lower=0)
        
        comp_df['Daily Confirmed'] = comp_df['Confirmed'].diff().fillna(comp_df['Confirmed'].iloc[0])
        comp_df['Daily Deaths'] = comp_df['Deaths'].diff().fillna(comp_df['Deaths'].iloc[0])
        comp_df['Daily Recovered'] = comp_df['Recovered'].diff().fillna(comp_df['Recovered'].iloc[0])
        
        comp_df['Daily Confirmed'] = comp_df['Daily Confirmed'].clip(lower=0)
        comp_df['Daily Deaths'] = comp_df['Daily Deaths'].clip(lower=0)
        comp_df['Daily Recovered'] = comp_df['Daily Recovered'].clip(lower=0)
        
        if len(comp_df) >= 7:
            comp_df['7-Day Avg (Confirmed)'] = comp_df['Daily Confirmed'].rolling(window=7).mean()
            comp_df['7-Day Avg (Deaths)'] = comp_df['Daily Deaths'].rolling(window=7).mean()
            comp_df['7-Day Avg (Recovered)'] = comp_df['Daily Recovered'].rolling(window=7).mean()
    
    # Calculate key metrics for dashboard
    latest_confirmed = int(plot_df['Confirmed'].iloc[-1])
    latest_deaths = int(plot_df['Deaths'].iloc[-1])
    latest_recovered = int(plot_df['Recovered'].iloc[-1])
    latest_active = int(plot_df['Active'].iloc[-1])
    
    # Calculate day-over-day changes for trend indicators
    if len(plot_df) >= 2:
        confirmed_change = plot_df['Confirmed'].iloc[-1] - plot_df['Confirmed'].iloc[-2]
        deaths_change = plot_df['Deaths'].iloc[-1] - plot_df['Deaths'].iloc[-2]
        recovered_change = plot_df['Recovered'].iloc[-1] - plot_df['Recovered'].iloc[-2]
        active_change = plot_df['Active'].iloc[-1] - plot_df['Active'].iloc[-2]
        
        confirmed_change_pct = (confirmed_change / plot_df['Confirmed'].iloc[-2] * 100) if plot_df['Confirmed'].iloc[-2] > 0 else 0
        deaths_change_pct = (deaths_change / plot_df['Deaths'].iloc[-2] * 100) if plot_df['Deaths'].iloc[-2] > 0 else 0
        recovered_change_pct = (recovered_change / plot_df['Recovered'].iloc[-2] * 100) if plot_df['Recovered'].iloc[-2] > 0 else 0
        active_change_pct = (active_change / plot_df['Active'].iloc[-2] * 100) if plot_df['Active'].iloc[-2] > 0 else 0
    else:
        confirmed_change = confirmed_change_pct = 0
        deaths_change = deaths_change_pct = 0
        recovered_change = recovered_change_pct = 0
        active_change = active_change_pct = 0
    
    # Calculate mortality rate and other metrics
    mortality_rate = (latest_deaths / latest_confirmed * 100) if latest_confirmed > 0 else 0
    recovery_rate = (latest_recovered / latest_confirmed * 100) if latest_confirmed > 0 else 0
    
    # Determine status indicators
    if mortality_rate > 5:
        mortality_status = "status-high"
        mortality_text = "HIGH"
    elif mortality_rate > 2:
        mortality_status = "status-medium"
        mortality_text = "MEDIUM"
    else:
        mortality_status = "status-low"
        mortality_text = "LOW"
    
    # Main dashboard content
    st.markdown(f"<h2 class='sub-header'>COVID-19 Analytics for {selected_country}</h2>", unsafe_allow_html=True)
    
    # Key metrics section with improved cards and trend indicators
    st.markdown('<div class="metric-row">', unsafe_allow_html=True)
    
    # Confirmed cases card with trend
    st.markdown(f'''
        <div class="metric-card metric-card-confirmed">
            <div class="metric-title">Confirmed Cases</div>
            <div class="metric-value-confirmed">{latest_confirmed:,}</div>
            <div class="metric-trend {'trend-up' if confirmed_change > 0 else 'trend-down'}">
                {'+' if confirmed_change > 0 else ''}{confirmed_change:,} ({confirmed_change_pct:.1f}%) {'↑' if confirmed_change > 0 else '↓'} 
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Deaths card with trend
    st.markdown(f'''
        <div class="metric-card metric-card-deaths">
            <div class="metric-title">Deaths</div>
            <div class="metric-value-deaths">{latest_deaths:,}</div>
            <div class="metric-trend {'trend-up' if deaths_change > 0 else 'trend-down'}">
                {'+' if deaths_change > 0 else ''}{deaths_change:,} ({deaths_change_pct:.1f}%) {'↑' if deaths_change > 0 else '↓'}
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Recovered cases card with trend
    st.markdown(f'''
        <div class="metric-card metric-card-recovered">
            <div class="metric-title">Recovered</div>
            <div class="metric-value-recovered">{latest_recovered:,}</div>
            <div class="metric-trend {'trend-up' if recovered_change > 0 else 'trend-down'}">
                {'+' if recovered_change > 0 else ''}{recovered_change:,} ({recovered_change_pct:.1f}%) {'↑' if recovered_change > 0 else '↓'}
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Active cases card with trend
    st.markdown(f'''
        <div class="metric-card metric-card-active">
            <div class="metric-title">Active Cases</div>
            <div class="metric-value-active">{latest_active:,}</div>
            <div class="metric-trend {'trend-up' if active_change > 0 else 'trend-down'}">
                {'+' if active_change > 0 else ''}{active_change:,} ({active_change_pct:.1f}%) {'↑' if active_change > 0 else '↓'}
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Mortality rate card with status indicator
    st.markdown(f'''
        <div class="metric-card metric-card-mortality">
            <div class="metric-title">Mortality Rate</div>
            <div class="metric-value-mortality">{mortality_rate:.2f}%</div>
            <div class="status-indicator {mortality_status}">{mortality_text}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Custom divider
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Trends Analysis Section
    st.markdown("<h2 class='sub-header'>Trends Analysis</h2>", unsafe_allow_html=True)
    
    # Create main tabs for different analyses
    tabs = st.tabs([
        "📈 Cumulative Cases", 
        "📊 Daily New Cases", 
        "🔄 Rolling Averages", 
        "🧩 Case Breakdown",
        "🔍 Advanced Metrics"
    ])
    
    # Tab 1: Cumulative Cases
    with tabs[0]:
        st.markdown("<div class='tab-subheader'>Cumulative COVID-19 Cases</div>", unsafe_allow_html=True)
        
        # Enhanced cumulative cases chart with comparison if selected
        if comparison_country != "None":
            cumulative_fig = go.Figure()
            
            # Add primary country data
            cumulative_fig.add_trace(go.Scatter(
                                x=plot_df['Date'], 
                y=plot_df['Confirmed'],
                mode='lines',
                name=f'{selected_country} Confirmed',
                line=dict(color='#1E88E5', width=3),
                hovertemplate='%{x}<br>Confirmed: %{y:,.0f}<extra></extra>'
            ))
            
            cumulative_fig.add_trace(go.Scatter(
                x=plot_df['Date'], 
                y=plot_df['Deaths'],
                mode='lines',
                name=f'{selected_country} Deaths',
                line=dict(color='#E53935', width=3),
                hovertemplate='%{x}<br>Deaths: %{y:,.0f}<extra></extra>'
            ))
            
            cumulative_fig.add_trace(go.Scatter(
                x=plot_df['Date'], 
                y=plot_df['Recovered'],
                mode='lines',
                name=f'{selected_country} Recovered',
                line=dict(color='#43A047', width=3),
                hovertemplate='%{x}<br>Recovered: %{y:,.0f}<extra></extra>'
            ))
            
            # Add comparison country data with dashed lines
            cumulative_fig.add_trace(go.Scatter(
                x=comp_df['Date'], 
                y=comp_df['Confirmed'],
                mode='lines',
                name=f'{comparison_country} Confirmed',
                line=dict(color='#1E88E5', width=2, dash='dot'),
                hovertemplate='%{x}<br>Confirmed: %{y:,.0f}<extra></extra>'
            ))
            
            cumulative_fig.add_trace(go.Scatter(
                x=comp_df['Date'], 
                y=comp_df['Deaths'],
                mode='lines',
                name=f'{comparison_country} Deaths',
                line=dict(color='#E53935', width=2, dash='dot'),
                hovertemplate='%{x}<br>Deaths: %{y:,.0f}<extra></extra>'
            ))
            
            cumulative_fig.add_trace(go.Scatter(
                x=comp_df['Date'], 
                y=comp_df['Recovered'],
                mode='lines',
                name=f'{comparison_country} Recovered',
                line=dict(color='#43A047', width=2, dash='dot'),
                hovertemplate='%{x}<br>Recovered: %{y:,.0f}<extra></extra>'
            ))
        else:
            cumulative_fig = px.line(
                plot_df, x='Date', y=['Confirmed', 'Deaths', 'Recovered', 'Active'],
                title=f"COVID-19 Cases in {selected_country}",
                labels={'value': 'Number of Cases', 'variable': 'Type'},
                color_discrete_map={
                    'Confirmed': '#1E88E5', 
                    'Deaths': '#E53935', 
                    'Recovered': '#43A047',
                    'Active': '#7E57C2'
                },
                log_y=use_log_scale,
                template=chart_template
            )
        
        cumulative_fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of Cases (Log Scale)" if use_log_scale else "Number of Cases",
            yaxis_type="log" if use_log_scale else "linear",
            legend_title="Case Type",
            hovermode="x unified",
            height=chart_height,
            template=chart_template
        )
        
        # Add annotation for important events or milestones
        if len(plot_df) > 30:
            peak_idx = plot_df['Daily Confirmed'].idxmax()
            peak_date = plot_df.loc[peak_idx, 'Date']
            peak_cases = plot_df.loc[peak_idx, 'Daily Confirmed']
            
            cumulative_fig.add_annotation(
                x=peak_date,
                y=plot_df.loc[peak_idx, 'Confirmed'],
                text=f"Peak daily cases: {int(peak_cases):,}",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#FF9800",
                ax=0,
                ay=-40,
                font=dict(size=12, color="#FF9800"),
                bordercolor="#FF9800",
                borderwidth=2,
                borderpad=4,
                bgcolor="rgba(255, 255, 255, 0.8)"
            )
        
        st.plotly_chart(cumulative_fig, use_container_width=True)
        
        # Add rate of change visualization
        st.markdown("<div class='tab-subheader'>Rate of Change</div>", unsafe_allow_html=True)
        
        if len(plot_df) >= 14:
            change_df = plot_df[['Date', 'Growth Rate (%)']].dropna()
            if len(change_df) > 0:
                rate_fig = px.line(
                    change_df, x='Date', y='Growth Rate (%)',
                    title=f"14-Day Growth Rate in {selected_country}",
                    color_discrete_sequence=['#FF9800'],
                    template=chart_template
                )
                
                rate_fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="14-Day Growth Rate (%)",
                    height=350,
                    hovermode="x unified"
                )
                
                # Add a horizontal line at 0% growth
                rate_fig.add_shape(
                    type="line",
                    x0=change_df['Date'].min(),
                    y0=0,
                    x1=change_df['Date'].max(),
                    y1=0,
                    line=dict(color="green", width=2, dash="dash")
                )
                
                st.plotly_chart(rate_fig, use_container_width=True)
            else:
                st.info("Insufficient data to calculate growth rate")

    # Tab 2: Daily New Cases
    with tabs[1]:
        st.markdown("<div class='tab-subheader'>Daily New Cases Analysis</div>", unsafe_allow_html=True)
        
        # Daily cases bar chart with enhanced design
        daily_fig = go.Figure()
        
        # Add bars for daily confirmed cases
        daily_fig.add_trace(go.Bar(
            x=plot_df['Date'],
            y=plot_df['Daily Confirmed'],
            name='Daily Confirmed',
            marker_color='rgba(30, 136, 229, 0.7)',
            hovertemplate='%{x}<br>Daily Confirmed: %{y:,.0f}<extra></extra>'
        ))
        
        daily_fig.add_trace(go.Bar(
            x=plot_df['Date'],
            y=plot_df['Daily Deaths'],
            name='Daily Deaths',
            marker_color='rgba(229, 57, 53, 0.7)',
            hovertemplate='%{x}<br>Daily Deaths: %{y:,.0f}<extra></extra>'
        ))
        
        if plot_df['Daily Recovered'].sum() > 0:  # Only show recovered if data exists
            daily_fig.add_trace(go.Bar(
                x=plot_df['Date'],
                y=plot_df['Daily Recovered'],
                name='Daily Recovered',
                marker_color='rgba(67, 160, 71, 0.7)',
                hovertemplate='%{x}<br>Daily Recovered: %{y:,.0f}<extra></extra>'
            ))
        
        # Enhanced layout
        daily_fig.update_layout(
            title=f"Daily New Cases in {selected_country}",
            xaxis_title="Date",
            yaxis_title="Number of Daily Cases",
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1,
            height=chart_height,
            template=chart_template,
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(daily_fig, use_container_width=True)
        
        # Add heatmap visualization of daily cases
        st.markdown("<div class='tab-subheader'>Daily Cases Calendar Heatmap</div>", unsafe_allow_html=True)
        
        if len(plot_df) >= 30:
            # Create calendar heatmap data
            heatmap_df = plot_df.copy()
            heatmap_df['Year'] = heatmap_df['Date'].dt.year
            heatmap_df['Month'] = heatmap_df['Date'].dt.month
            heatmap_df['Day'] = heatmap_df['Date'].dt.day
            heatmap_df['WeekDay'] = heatmap_df['Date'].dt.dayofweek
            
            # Only show recent data if there's too much
            if len(heatmap_df) > 90:
                heatmap_df = heatmap_df.iloc[-90:]  # Last 90 days
            
            # Create heatmap
            heatmap_fig = px.density_heatmap(
                heatmap_df, 
                x='Day', 
                y='Month',
                z='Daily Confirmed',
                nbinsx=31,  # Max days in a month
                nbinsy=12,  # 12 months
                color_continuous_scale='YlOrRd',
                title=f"Daily Confirmed Cases Calendar Heatmap - {selected_country}",
                template=chart_template
            )
            
            heatmap_fig.update_layout(
                xaxis_title="Day of Month",
                yaxis_title="Month",
                height=350,
                coloraxis_colorbar=dict(title="Daily Cases")
            )
            
            st.plotly_chart(heatmap_fig, use_container_width=True)
        else:
            st.info("Not enough data points for calendar heatmap visualization")

    # Tab 3: Rolling Averages
    with tabs[2]:
        st.markdown("<div class='tab-subheader'>7-Day Rolling Average Trends</div>", unsafe_allow_html=True)
        
        if len(plot_df) >= 7 and '7-Day Avg (Confirmed)' in plot_df.columns:
            # Create combined chart with bars and lines for better visualization
            rolling_fig = go.Figure()
            
            # Add bars for daily values
            rolling_fig.add_trace(go.Bar(
                x=plot_df['Date'],
                y=plot_df['Daily Confirmed'],
                name='Daily Confirmed',
                marker_color='rgba(30, 136, 229, 0.3)',
                hovertemplate='%{x}<br>Daily Cases: %{y:,.0f}<extra></extra>'
            ))
            
            # Add line for 7-day average
            rolling_fig.add_trace(go.Scatter(
                x=plot_df['Date'],
                y=plot_df['7-Day Avg (Confirmed)'],
                mode='lines',
                name='7-Day Average',
                line=dict(color='#1E88E5', width=4),
                hovertemplate='%{x}<br>7-Day Avg: %{y:,.1f}<extra></extra>'
            ))
            
            # Add comparison country if selected
            if comparison_country != "None" and '7-Day Avg (Confirmed)' in comp_df.columns:
                rolling_fig.add_trace(go.Scatter(
                    x=comp_df['Date'],
                    y=comp_df['7-Day Avg (Confirmed)'],
                    mode='lines',
                    name=f'{comparison_country} 7-Day Avg',
                    line=dict(color='#9C27B0', width=3, dash='dot'),
                    hovertemplate='%{x}<br>7-Day Avg: %{y:,.1f}<extra></extra>'
                ))
            
            rolling_fig.update_layout(
                title=f"7-Day Rolling Average of Daily Confirmed Cases in {selected_country}",
                xaxis_title='Date',
                yaxis_title='Number of Cases',
                legend_title='Metric',
                hovermode="x unified",
                height=chart_height,
                template=chart_template
            )
            
            st.plotly_chart(rolling_fig, use_container_width=True)
            
            # Split charts for deaths and recoveries
            col1, col2 = st.columns(2)
            
            with col1:
                # Deaths rolling average
                deaths_rolling_fig = go.Figure()
                
                deaths_rolling_fig.add_trace(go.Bar(
                    x=plot_df['Date'],
                    y=plot_df['Daily Deaths'],
                    name='Daily Deaths',
                    marker_color='rgba(229, 57, 53, 0.3)',
                    hovertemplate='%{x}<br>Daily Deaths: %{y:,.0f}<extra></extra>'
                ))
                
                deaths_rolling_fig.add_trace(go.Scatter(
                    x=plot_df['Date'],
                    y=plot_df['7-Day Avg (Deaths)'],
                    mode='lines',
                    name='7-Day Average',
                    line=dict(color='#E53935', width=4),
                    hovertemplate='%{x}<br>7-Day Avg: %{y:,.1f}<extra></extra>'
                ))
                
                deaths_rolling_fig.update_layout(
                    title=f"Deaths 7-Day Average",
                    xaxis_title='Date',
                    yaxis_title='Number of Deaths',
                    height=350,
                    template=chart_template,
                    hovermode="x unified"
                )
                
                st.plotly_chart(deaths_rolling_fig, use_container_width=True)
            
            with col2:
                # Recoveries rolling average if data exists
                if plot_df['Daily Recovered'].sum() > 0:
                    recovery_rolling_fig = go.Figure()
                    
                    recovery_rolling_fig.add_trace(go.Bar(
                        x=plot_df['Date'],
                        y=plot_df['Daily Recovered'],
                        name='Daily Recovered',
                        marker_color='rgba(67, 160, 71, 0.3)',
                        hovertemplate='%{x}<br>Daily Recovered: %{y:,.0f}<extra></extra>'
                    ))
                    
                    recovery_rolling_fig.add_trace(go.Scatter(
                        x=plot_df['Date'],
                        y=plot_df['7-Day Avg (Recovered)'],
                        mode='lines',
                        name='7-Day Average',
                        line=dict(color='#43A047', width=4),
                        hovertemplate='%{x}<br>7-Day Avg: %{y:,.1f}<extra></extra>'
                    ))
                    
                    recovery_rolling_fig.update_layout(
                        title=f"Recoveries 7-Day Average",
                        xaxis_title='Date',
                        yaxis_title='Number of Recoveries',
                        height=350,
                        template=chart_template,
                        hovermode="x unified"
                    )
                    
                    st.plotly_chart(recovery_rolling_fig, use_container_width=True)
                else:
                    st.info("No recovery data available for this country")
        else:
            st.info("Not enough data points to calculate 7-day rolling averages")

    # Tab 4: Case Breakdown
    with tabs[3]:
        st.markdown("<div class='tab-subheader'>COVID-19 Case Distribution Analysis</div>", unsafe_allow_html=True)
        
        # Create pie chart for case distribution
        case_distribution = {
            'Status': ['Active', 'Recovered', 'Deaths'],
            'Count': [latest_active, latest_recovered, latest_deaths]
        }
        distribution_df = pd.DataFrame(case_distribution)
        
        pie_fig = px.pie(
            distribution_df, 
            names='Status', 
            values='Count',
            title=f"Current Case Status Distribution in {selected_country}",
            color='Status',
            color_discrete_map={
                'Active': '#7E57C2',
                'Recovered': '#43A047',
                'Deaths': '#E53935'
            },
            hole=0.4,
            template=chart_template
        )
        
        pie_fig.update_layout(
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        
        pie_fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value:,.0f}<br>Percentage: %{percent:.1%}<extra></extra>'
        )
        
        st.plotly_chart(pie_fig, use_container_width=True)
        
        # Stacked area chart for case progression
        stack_data = plot_df[['Date', 'Active', 'Recovered', 'Deaths']].copy()
        
        # Create stacked area chart
        stack_fig = px.area(
            stack_data, 
            x='Date', 
            y=['Active', 'Recovered', 'Deaths'],
            title=f"Case Progression Over Time in {selected_country}",
            color_discrete_map={
                'Active': '#7E57C2',
                'Recovered': '#43A047',
                'Deaths': '#E53935'
            },
            template=chart_template
        )
        
        stack_fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Number of Cases',
            legend_title='Case Status',
            hovermode="x unified",
            height=chart_height
        )
        
        st.plotly_chart(stack_fig, use_container_width=True)
        
        # Provincial breakdown if data exists
        provinces = data['confirmed'][data['confirmed']['Country/Region'] == selected_country]['Province/State'].dropna().unique()
        
        if len(provinces) > 1:
            st.markdown("<div class='tab-subheader'>Provincial/State Breakdown</div>", unsafe_allow_html=True)
            
            # Get latest date for the breakdown
            latest_date = selected_date_strs[-1]
            
            # Create dataframe with province data
            province_data = []
            for province in provinces:
                province_row = data['confirmed'][(data['confirmed']['Country/Region'] == selected_country) & 
                                            (data['confirmed']['Province/State'] == province)]
                if len(province_row) > 0 and latest_date in province_row.columns:
                    cases = province_row[latest_date].values[0]
                    province_data.append({
                        'Province/State': province,
                        'Confirmed Cases': cases
                    })
            
            if province_data:
                province_df = pd.DataFrame(province_data)
                province_df = province_df.sort_values('Confirmed Cases', ascending=False).head(10)  # Top 10 provinces
                
                # Create horizontal bar chart
                province_bar = px.bar(
                    province_df, 
                    x='Confirmed Cases', 
                    y='Province/State',
                    orientation='h',
                    title=f"Top Provinces/States in {selected_country} by Confirmed Cases",
                    color='Confirmed Cases',
                    color_continuous_scale='Blues',
                    template=chart_template
                )
                
                province_bar.update_layout(
                    xaxis_title='Confirmed Cases',
                    yaxis_title='Province/State',
                    height=max(400, len(province_df) * 30),  # Adjust height based on number of provinces
                    yaxis={'categoryorder':'total ascending'}
                )
                
                st.plotly_chart(province_bar, use_container_width=True)

    # Tab 5: Advanced Metrics
    with tabs[4]:
        st.markdown("<div class='tab-subheader'>Advanced Epidemiological Metrics</div>", unsafe_allow_html=True)
        
        if len(plot_df) >= 14:
            advanced_metrics = plot_df[['Date', 'Growth Rate (%)', 'Doubling Time']].dropna()
            
            if len(advanced_metrics) > 0:
                # Create columns for metrics
                col1, col2 = st.columns(2)
                
                with col1:
                    # Case doubling time chart
                    doubling_fig = px.line(
                        advanced_metrics,
                        x='Date',
                        y='Doubling Time',
                        title=f"Case Doubling Time (Days) in {selected_country}",
                        color_discrete_sequence=['#FF9800'],
                        template=chart_template
                    )
                    
                    # Add highlighting for concerning doubling times
                    doubling_fig.add_shape(
                        type="rect",
                        x0=advanced_metrics['Date'].min(),
                        x1=advanced_metrics['Date'].max(),
                        y0=0,
                        y1=7,
                        fillcolor="rgba(229, 57, 53, 0.2)",
                        line_width=0,
                        layer="below"
                    )
                    
                    doubling_fig.add_shape(
                        type="rect",
                        x0=advanced_metrics['Date'].min(),
                        x1=advanced_metrics['Date'].max(),
                        y0=7,
                        y1=14,
                        fillcolor="rgba(255, 179, 0, 0.2)",
                        line_width=0,
                        layer="below"
                    )
                    
                    doubling_fig.update_layout(
                        xaxis_title='Date',
                        yaxis_title='Doubling Time (Days)',
                        height=350,
                        hovermode="x unified"
                    )
                    
                    # Add annotations explaining doubling time
                    doubling_fig.add_annotation(
                        x=advanced_metrics['Date'].min(),
                        y=3.5,
                        text="Critical Zone",
                        showarrow=False,
                        font=dict(size=10, color="red"),
                        align="left"
                    )
                    
                    doubling_fig.add_annotation(
                        x=advanced_metrics['Date'].min(),
                        y=10.5,
                        text="Caution Zone",
                        showarrow=False,
                        font=dict(size=10, color="orange"),
                        align="left"
                    )
                    
                    st.plotly_chart(doubling_fig, use_container_width=True)
                
                with col2:
                    # Case Fatality Rate over time
                    if len(plot_df) > 0 and plot_df['Confirmed'].sum() > 0:
                        plot_df['CFR (%)'] = (plot_df['Deaths'] / plot_df['Confirmed'] * 100).clip(upper=100)
                        
                        cfr_fig = px.line(
                            plot_df,
                            x='Date',
                            y='CFR (%)',
                            title=f"Case Fatality Rate (%) in {selected_country}",
                            color_discrete_sequence=['#E53935'],
                            template=chart_template
                        )
                        
                        cfr_fig.update_layout(
                            xaxis_title='Date',
                            yaxis_title='Case Fatality Rate (%)',
                            height=350,
                            hovermode="x unified"
                        )
                        
                        # Add global average CFR for comparison
                        global_cfr = 2.1  # Example value, should be calculated from actual global data
                        cfr_fig.add_shape(
                            type="line",
                            x0=plot_df['Date'].min(),
                            y0=global_cfr,
                            x1=plot_df['Date'].max(),
                            y1=global_cfr,
                            line=dict(
                                color="gray",
                                width=2,
                                dash="dash",
                            )
                        )
                        
                        cfr_fig.add_annotation(
                            x=plot_df['Date'].max(),
                            y=global_cfr,
                            text="Global Average",
                            showarrow=False,
                            font=dict(size=10, color="gray"),
                            align="right",
                            xshift=-10
                        )
                        
                        st.plotly_chart(cfr_fig, use_container_width=True)
                
                # R0 Estimation (Simplified)
                st.markdown("<div class='tab-subheader'>Reproduction Number (R₀) Estimation</div>", unsafe_allow_html=True)
                st.info("Note: This is a simplified estimation of R₀ based on the growth of cases over time. For accurate epidemiological modeling, more complex methods are required.")
                
                # Simplified R0 calculation using 5-day interval growth
                if len(plot_df) >= 10:
                    # Calculate simplified R0 using 5-day growth and assuming 5-day serial interval
                    plot_df['R0_est'] = plot_df['Confirmed'] / plot_df['Confirmed'].shift(5)
                    r0_df = plot_df[['Date', 'R0_est']].dropna().tail(30)  # Last 30 points
                    
                    r0_fig = px.line(
                        r0_df,
                        x='Date',
                        y='R0_est',
                        title=f"Estimated Reproduction Number (R₀) in {selected_country}",
                        color_discrete_sequence=['#673AB7'],
                        template=chart_template
                    )
                    
                    # Add reference line at R0=1 (critical threshold)
                    r0_fig.add_shape(
                        type="line",
                        x0=r0_df['Date'].min(),
                        y0=1,
                        x1=r0_df['Date'].max(),
                        y1=1,
                        line=dict(color="red", width=2, dash="dash")
                    )
                    
                    r0_fig.add_annotation(
                        x=r0_df['Date'].max(),
                        y=1,
                        text="Critical Threshold (R₀=1)",
                        showarrow=False,
                        font=dict(size=10, color="red"),
                        xshift=-10,
                        yshift=10
                    )
                    
                    r0_fig.update_layout(
                        xaxis_title='Date',
                        yaxis_title='Estimated R₀',
                        height=400,
                        hovermode="x unified",
                        yaxis=dict(range=[0, min(5, r0_df['R0_est'].max() * 1.2)])  # Cap y-axis for better visualization
                    )
                    
                    st.plotly_chart(r0_fig, use_container_width=True)
            else:
                st.info("Insufficient data to calculate advanced metrics")
        else:
            st.info("Insufficient data points to calculate advanced metrics (requires at least 14 days)")
    
    # Regional Analysis Section
    st.markdown("<h2 class='sub-header'>Regional Analysis</h2>", unsafe_allow_html=True)
    
    # Get provinces data if available
    provinces = data['confirmed'][data['confirmed']['Country/Region'] == selected_country]['Province/State'].dropna().unique()
    
    if len(provinces) > 1:
        # There are multiple provinces - show breakdown
        st.subheader(f"Provincial/State Breakdown for {selected_country}")
        
        # Get latest date for the pie chart
        latest_date = selected_date_strs[-1]
        
        # Get confirmed cases for each province
        province_data = []
        for province in provinces:
            province_row = data['confirmed'][(data['confirmed']['Country/Region'] == selected_country) & 
                                        (data['confirmed']['Province/State'] == province)]
            if len(province_row) > 0:
                cases = province_row[latest_date].values[0]
                
                # Get lat/long if available
                lat = province_row['Lat'].values[0] if 'Lat' in province_row.columns and not pd.isna(province_row['Lat'].values[0]) else None
                long = province_row['Long'].values[0] if 'Long' in province_row.columns and not pd.isna(province_row['Long'].values[0]) else None
                
                province_data.append({
                    'Province': province,
                    'Cases': cases,
                    'Lat': lat,
                    'Long': long
                })
        
        if province_data:
            province_df = pd.DataFrame(province_data)
            province_df = province_df.sort_values('Cases', ascending=False)
            
            # Create a pie chart of provinces
            province_fig = px.pie(
                province_df.head(10),  # Top 10 provinces
                names='Province',
                values='Cases',
                title=f"Provincial Distribution of Cases in {selected_country} (as of {latest_date})",
                hole=0.4,
                template=chart_template
            )
            
            province_fig.update_layout(height=500)
            st.plotly_chart(province_fig, use_container_width=True)
            
            # Create map if lat/long data is available
            if 'Lat' in province_df.columns and not province_df['Lat'].isna().all():
                st.markdown("<div class='tab-subheader'>Regional Case Distribution Map</div>", unsafe_allow_html=True)
                
                # Create map with scatter points sized by case count
                map_fig = px.scatter_geo(
                    province_df,
                    lat='Lat',
                    lon='Long',
                    text='Province',
                    size='Cases',
                    color='Cases',
                    hover_name='Province',
                    size_max=50,
                    color_continuous_scale='Viridis',
                    title=f"COVID-19 Cases by Region in {selected_country}"
                )
                
                map_fig.update_layout(
                    height=600,
                    geo=dict(
                        showland=True,
                        landcolor='rgb(243, 243, 243)',
                        countrycolor='rgb(204, 204, 204)',
                        showocean=True,
                        oceancolor='rgb(230, 230, 250)',
                        showlakes=True,
                        lakecolor='rgb(220, 220, 250)',
                        showrivers=True,
                        rivercolor='rgb(220, 220, 250)'
                    )
                )
                
                st.plotly_chart(map_fig, use_container_width=True)
    else:
        st.info(f"No provincial/state data available for {selected_country}")
    
        # Data table view with improved styling
    st.markdown("<h2 class='sub-header'>Detailed Data Analysis</h2>", unsafe_allow_html=True)
    
    with st.expander("View Raw Data Table"):
        # Create tabs for different data views
        data_tabs = st.tabs(["Time Series Data", "Summary Statistics", "Export Options"])
        
        with data_tabs[0]:
            # Show the full time series data
            st.dataframe(
                plot_df.style.format({
                    'Confirmed': '{:,.0f}',
                    'Deaths': '{:,.0f}',
                    'Recovered': '{:,.0f}',
                    'Active': '{:,.0f}',
                    'Daily Confirmed': '{:,.0f}',
                    'Daily Deaths': '{:,.0f}',
                    'Daily Recovered': '{:,.0f}',
                    '7-Day Avg (Confirmed)': '{:,.1f}',
                    '7-Day Avg (Deaths)': '{:,.1f}',
                    '7-Day Avg (Recovered)': '{:,.1f}',
                    'Growth Rate (%)': '{:,.2f}',
                    'Doubling Time': '{:,.1f}',
                    'CFR (%)': '{:,.2f}'
                }),
                use_container_width=True,
                height=400
            )
        
        with data_tabs[1]:
            # Create a summary statistics table
            summary_stats = pd.DataFrame({
                'Metric': [
                    'Total Confirmed Cases',
                    'Total Deaths',
                    'Total Recovered',
                    'Active Cases',
                    'Case Fatality Rate (%)',
                    'Maximum Daily Cases',
                    'Maximum Daily Deaths',
                    'Latest Daily Cases',
                    'Latest Daily Deaths',
                    'Latest 7-Day Avg Cases',
                    'Latest 7-Day Avg Deaths'
                ],
                'Value': [
                    f"{latest_confirmed:,}",
                    f"{latest_deaths:,}",
                    f"{latest_recovered:,}",
                    f"{latest_active:,}",
                    f"{mortality_rate:.2f}%",
                    f"{plot_df['Daily Confirmed'].max():,.0f}",
                    f"{plot_df['Daily Deaths'].max():,.0f}",
                    f"{plot_df['Daily Confirmed'].iloc[-1]:,.0f}",
                    f"{plot_df['Daily Deaths'].iloc[-1]:,.0f}",
                    f"{plot_df['7-Day Avg (Confirmed)'].iloc[-1]:,.1f}" if '7-Day Avg (Confirmed)' in plot_df else "N/A",
                    f"{plot_df['7-Day Avg (Deaths)'].iloc[-1]:,.1f}" if '7-Day Avg (Deaths)' in plot_df else "N/A"
                ]
            })
            
            st.dataframe(summary_stats, use_container_width=True)
        
        with data_tabs[2]:
            # Create CSV download buttons
            csv = plot_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Full Dataset as CSV",
                data=csv,
                file_name=f"covid19_data_{selected_country.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                help="Download the complete dataset for selected country and date range"
            )
            
            # Excel download option
            st.markdown("""
            ### Additional Export Options
            
            For more advanced analysis, you may want to export this data to other formats or tools:
            
            - Use the CSV download above for most spreadsheet applications
            - For programmatic access, use the COVID-19 API endpoints
            - For BI tools, connect to the COVID-19 data warehouse
            """)

    # Add interactive data exploration section
    st.markdown("<h2 class='sub-header'>Interactive Data Explorer</h2>", unsafe_allow_html=True)
    
    # Create a scatter plot with selectable dimensions
    if len(plot_df) > 10:
        # Allow user to select x and y dimensions
        explorer_cols = st.columns([1, 1, 2])
        with explorer_cols[0]:
            x_dim = st.selectbox(
                "X-Axis Metric",
                options=['Date', 'Confirmed', 'Deaths', 'Recovered', 'Active', 
                         'Daily Confirmed', 'Daily Deaths', 'Daily Recovered'],
                index=0
            )
        
        with explorer_cols[1]:
            y_dim = st.selectbox(
                "Y-Axis Metric",
                options=['Confirmed', 'Deaths', 'Recovered', 'Active', 
                         'Daily Confirmed', 'Daily Deaths', 'Daily Recovered',
                         '7-Day Avg (Confirmed)', '7-Day Avg (Deaths)'],
                index=0
            )
        
        # Create the scatter plot with trend line
        if x_dim in plot_df.columns and y_dim in plot_df.columns:
            explore_fig = px.scatter(
                plot_df, 
                x=x_dim, 
                y=y_dim,
                title=f"Relationship between {x_dim} and {y_dim}",
                trendline="ols" if x_dim != 'Date' else None,
                labels={x_dim: x_dim, y_dim: y_dim},
                template=chart_template
            )
            
            explore_fig.update_traces(
                marker=dict(
                    size=10,
                    opacity=0.7,
                    line=dict(width=1, color='DarkSlateGrey')
                )
            )
            
            explore_fig.update_layout(
                height=450,
                hovermode='closest'
            )
            
            st.plotly_chart(explore_fig, use_container_width=True)
        else:
            st.warning("Selected metrics not available in the dataset")
    else:
        st.info("Not enough data points for interactive exploration")

    # Footer with attribution and timestamp
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="footer">
            © 2025 COVID-19 Global Analytics Dashboard | Data source: Johns Hopkins CSSE<br>
            Last data update: {current_time} UTC<br>
            Created by: {current_user}<br>
            <small>This dashboard is for educational and informational purposes only. For official guidance, please consult public health authorities.</small>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error processing data: {str(e)}")
    st.write("Please check the data structure and ensure it matches the expected JHU CSSE format.")
    
    # Help for common errors
    st.markdown("""
    ### Troubleshooting Common Data Issues
    
    If you're seeing errors, check the following:
    
    1. **File Format**: Ensure CSV files are properly formatted with expected column names
    2. **File Locations**: Files should be in `data/processed/` directory
    3. **Date Formats**: Dates should be in format like "1/22/20" (JHU CSSE standard)
    4. **Country Names**: Country names should be consistent across all datasets
    """)
    
    # Show data structure for debugging
    with st.expander("View Data Structure for Debugging"):
        for key in data:
            st.write(f"Sample of {key}_processed.csv:")
            st.dataframe(data[key].head())
            st.write(f"Column names in {key}_processed.csv:")
            st.write(data[key].columns.tolist()[:10])