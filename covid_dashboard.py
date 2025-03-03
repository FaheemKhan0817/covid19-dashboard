import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time  # Added for progress bar function

# Set page configuration
st.set_page_config(
    page_title="COVID-19 Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get parameters from user input (updated)
current_time = "2025-03-03 09:03:57"  # Updated timestamp
current_user = "FaheemKhan0817"  # Your user login

# Apply simplified CSS styling
st.markdown("""
    <style>
    /* Main styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #424242;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Metric cards */
    .metric-row {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 1.2rem;
        border-left: 4px solid;
    }
    
    .metric-card-confirmed { border-left-color: #1E88E5; }
    .metric-card-deaths { border-left-color: #E53935; }
    .metric-card-recovered { border-left-color: #43A047; }
    .metric-card-mortality { border-left-color: #FFB300; }
    
    .metric-title {
        font-size: 0.9rem;
        color: #757575;
        font-weight: 500;
        margin-bottom: 0.25rem;
    }
    
    .metric-value-confirmed { font-size: 1.8rem; color: #1E88E5; font-weight: 700; }
    .metric-value-deaths { font-size: 1.8rem; color: #E53935; font-weight: 700; }
    .metric-value-recovered { font-size: 1.8rem; color: #43A047; font-weight: 700; }
    .metric-value-mortality { font-size: 1.8rem; color: #FFB300; font-weight: 700; }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>🌍 COVID-19 Dashboard</h1>", unsafe_allow_html=True)

# Add a custom progress bar for data loading
def custom_progress_bar():
    progress_container = st.empty()
    for percent_complete in range(0, 101, 5):
        progress_container.progress(percent_complete)
        time.sleep(0.02)  # Short delay for visual effect
    progress_container.empty()

# Load data with caching
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

with st.spinner("Loading data..."):
    custom_progress_bar()  # Show progress bar while loading
    data = load_data()

if data is None:
    st.error("Failed to load COVID-19 data files.")
    st.info("Please ensure data files are in the data/processed/ directory.")
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
    
    # Sidebar controls
    st.sidebar.header("Dashboard Controls")
    
    # Country selection
    default_country = 'Albania'  # Set Albania as default
    if default_country not in countries:
        default_country = countries[0]
        
    selected_country = st.sidebar.selectbox(
        "Select Country/Region",
        countries,
        index=countries.index(default_country)
    )
    
    # Parse dates for date range selector
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
        
        # Set default start date to Jan 22, 2020 if available
        default_start = pd.to_datetime("2020-01-22")
        if default_start < min_date:
            default_start = min_date
        
        # Set default end date to Mar 9, 2023 if available
        default_end = pd.to_datetime("2023-03-09")
        if default_end > max_date:
            default_end = max_date
        elif default_end < min_date:
            default_end = max_date
        
        # Date range selection
        st.sidebar.subheader("Select Date Range")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input("Start Date", default_start, min_value=min_date, max_value=max_date)
        with col2:
            end_date = st.date_input("End Date", default_end, min_value=min_date, max_value=max_date)
        
        # Filter dates based on selected range
        selected_date_strs = []
        for date_str, date_obj in parsed_dates:
            if start_date <= date_obj.date() <= end_date:
                selected_date_strs.append(date_str)
    else:
        st.warning("Could not parse date columns correctly")
        selected_date_strs = date_columns[:30]  # Use first 30 dates as fallback
    
    # Simple visualization options
    st.sidebar.subheader("Visualization Options")
    use_log_scale = st.sidebar.checkbox("Use logarithmic scale", False)
    
    # Add chart type selection
    chart_type = st.sidebar.radio(
        "Chart Type for Cumulative Cases",
        ["Line", "Bar"],
        index=0
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
    
    # Convert to proper dates for plotting
    plot_dates = [pd.to_datetime(d, format='%m/%d/%y') for d in selected_date_strs]
    
    # Create plotting dataframe
    plot_df = pd.DataFrame({
        'Date': plot_dates,
        'Confirmed': confirmed_values,
        'Deaths': deaths_values,
        'Recovered': recovered_values
    })
    
    # Add active cases calculation
    plot_df['Active'] = plot_df['Confirmed'] - plot_df['Deaths'] - plot_df['Recovered']
    plot_df['Active'] = plot_df['Active'].clip(lower=0)  # Ensure no negative active cases
    
    # Calculate daily new cases
    plot_df['Daily Confirmed'] = plot_df['Confirmed'].diff().fillna(plot_df['Confirmed'].iloc[0])
    plot_df['Daily Deaths'] = plot_df['Deaths'].diff().fillna(plot_df['Deaths'].iloc[0])
    plot_df['Daily Recovered'] = plot_df['Recovered'].diff().fillna(plot_df['Recovered'].iloc[0])
    
    # Replace negative daily values with 0 (data corrections can cause negative values)
    plot_df['Daily Confirmed'] = plot_df['Daily Confirmed'].clip(lower=0)
    plot_df['Daily Deaths'] = plot_df['Daily Deaths'].clip(lower=0)
    plot_df['Daily Recovered'] = plot_df['Daily Recovered'].clip(lower=0)
    
    # Calculate 7-day rolling averages
    if len(plot_df) >= 7:
        plot_df['7-Day Avg (Confirmed)'] = plot_df['Daily Confirmed'].rolling(window=7).mean()
        plot_df['7-Day Avg (Deaths)'] = plot_df['Daily Deaths'].rolling(window=7).mean()
    
    # Calculate key metrics for dashboard
    latest_confirmed = int(plot_df['Confirmed'].iloc[-1])
    latest_deaths = int(plot_df['Deaths'].iloc[-1])
    latest_recovered = int(plot_df['Recovered'].iloc[-1])
    latest_active = int(plot_df['Active'].iloc[-1])
    
    # Calculate mortality rate
    mortality_rate = (latest_deaths / latest_confirmed * 100) if latest_confirmed > 0 else 0
    
    # Main dashboard content
    st.markdown(f"<h2 class='sub-header'>COVID-19 Stats for {selected_country}</h2>", unsafe_allow_html=True)
    
    # Key metrics section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
            <div class="metric-card metric-card-confirmed">
                <div class="metric-title">Confirmed Cases</div>
                <div class="metric-value-confirmed">{latest_confirmed:,}</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
            <div class="metric-card metric-card-deaths">
                <div class="metric-title">Deaths</div>
                <div class="metric-value-deaths">{latest_deaths:,}</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
            <div class="metric-card metric-card-recovered">
                <div class="metric-title">Recovered</div>
                <div class="metric-value-recovered">{latest_recovered:,}</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
            <div class="metric-card metric-card-mortality">
                <div class="metric-title">Mortality Rate</div>
                <div class="metric-value-mortality">{mortality_rate:.2f}%</div>
            </div>
        ''', unsafe_allow_html=True)
    
    # Create tabs for different analyses
    tabs = st.tabs(["Cases Over Time", "Daily New Cases", "Case Distribution", "Regional Data"])
    
    # Tab 1: Cumulative Cases
    with tabs[0]:
        st.subheader("Cumulative COVID-19 Cases")
        
        # Create chart based on selected type (line or bar)
        if chart_type == "Line":
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
                log_y=use_log_scale
            )
        else:  # Bar chart
            cumulative_fig = px.bar(
                plot_df, x='Date', y=['Confirmed', 'Deaths', 'Recovered', 'Active'],
                title=f"COVID-19 Cases in {selected_country}",
                labels={'value': 'Number of Cases', 'variable': 'Type'},
                color_discrete_map={
                    'Confirmed': '#1E88E5', 
                    'Deaths': '#E53935', 
                    'Recovered': '#43A047',
                    'Active': '#7E57C2'
                },
                log_y=use_log_scale
            )
        
        cumulative_fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of Cases (Log Scale)" if use_log_scale else "Number of Cases",
            yaxis_type="log" if use_log_scale else "linear",
            legend_title="Case Type",
            hovermode="x unified",
            height=500
        )
        
        st.plotly_chart(cumulative_fig, use_container_width=True)
    
    # Tab 2: Daily New Cases
    with tabs[1]:
        st.subheader("Daily New Cases")
        
        # Daily cases visualization
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Bar chart for daily cases
            daily_fig = px.bar(
                plot_df, x='Date', y=['Daily Confirmed', 'Daily Deaths', 'Daily Recovered'],
                title=f"Daily New Cases in {selected_country}",
                labels={'value': 'Daily Cases', 'variable': 'Type'},
                color_discrete_map={
                    'Daily Confirmed': '#1E88E5',
                    'Daily Deaths': '#E53935',
                    'Daily Recovered': '#43A047'
                },
                barmode='group'
            )
            
            daily_fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Number of Daily Cases",
                legend_title="Case Type",
                hovermode="x unified",
                height=400
            )
            
            st.plotly_chart(daily_fig, use_container_width=True)
        
        with col2:
            # Display summary statistics
            st.markdown("#### Summary Statistics")
            
            summary_stats = [
                {"Metric": "Average Daily Cases", "Value": f"{plot_df['Daily Confirmed'].mean():.1f}"},
                {"Metric": "Maximum Daily Cases", "Value": f"{plot_df['Daily Confirmed'].max():.0f}"},
                {"Metric": "Latest Daily Cases", "Value": f"{plot_df['Daily Confirmed'].iloc[-1]:.0f}"},
                {"Metric": "Average Daily Deaths", "Value": f"{plot_df['Daily Deaths'].mean():.1f}"},
                {"Metric": "Maximum Daily Deaths", "Value": f"{plot_df['Daily Deaths'].max():.0f}"}
            ]
            
            st.table(pd.DataFrame(summary_stats))
        
        # 7-day average chart
        if len(plot_df) >= 7 and '7-Day Avg (Confirmed)' in plot_df.columns:
            st.subheader("7-Day Rolling Average")
            
            rolling_fig = go.Figure()
            
            rolling_fig.add_trace(go.Bar(
                x=plot_df['Date'],
                y=plot_df['Daily Confirmed'],
                name='Daily Confirmed',
                marker_color='rgba(30, 136, 229, 0.3)',
                hovertemplate='%{x}<br>Daily Cases: %{y:,.0f}<extra></extra>'
            ))
            
            rolling_fig.add_trace(go.Scatter(
                x=plot_df['Date'],
                y=plot_df['7-Day Avg (Confirmed)'],
                mode='lines',
                name='7-Day Average',
                line=dict(color='#1E88E5', width=3),
                hovertemplate='%{x}<br>7-Day Avg: %{y:,.1f}<extra></extra>'
            ))
            
            rolling_fig.update_layout(
                title=f"7-Day Average of Daily Cases in {selected_country}",
                xaxis_title="Date",
                yaxis_title="Number of Cases",
                legend_title="Type",
                hovermode="x unified",
                height=400
            )
            
            st.plotly_chart(rolling_fig, use_container_width=True)
            
    # Tab 3: Case Distribution (New Tab for Pie Charts)
    with tabs[2]:
        st.subheader("COVID-19 Case Distribution")
        
        # Create data for pie charts - handle zero values
        latest_active = max(0, latest_active)
        latest_recovered = max(0, latest_recovered)
        latest_deaths = max(0, latest_deaths)
        
        # Check if we have enough data for pie charts
        total_cases = latest_active + latest_recovered + latest_deaths
        
        if total_cases > 0:  # Only show pie charts if we have cases
            col1, col2 = st.columns(2)
            
            with col1:
                # Latest case distribution pie chart
                st.markdown("### Current Case Status Distribution")
                latest_distribution = {
                    'Category': ['Active', 'Recovered', 'Deaths'],
                    'Count': [latest_active, latest_recovered, latest_deaths]
                }
                
                distribution_df = pd.DataFrame(latest_distribution)
                
                # Filter out zero values to make pie chart work better
                distribution_df = distribution_df[distribution_df['Count'] > 0]
                
                if len(distribution_df) > 0:
                    pie_fig = px.pie(
                        distribution_df,
                        names='Category',
                        values='Count',
                        title=f"Distribution in {selected_country}",
                        color='Category',
                        color_discrete_map={
                            'Active': '#7E57C2',
                            'Recovered': '#43A047',
                            'Deaths': '#E53935'
                        }
                    )
                    
                    pie_fig.update_layout(
                        height=400,
                        legend_title="Status",
                    )
                    
                    pie_fig.update_traces(
                        textposition='inside',
                        textinfo='percent+label',
                        hovertemplate='<b>%{label}</b><br>Count: %{value:,.0f}<br>Percentage: %{percent:.1%}<extra></extra>'
                    )
                    
                    st.plotly_chart(pie_fig, use_container_width=True)
                else:
                    st.info("No distribution data available for pie chart")
            
            with col2:
                # Daily composition pie chart (last 30 days)
                recent_days = min(30, len(plot_df))
                recent_daily_data = plot_df.iloc[-recent_days:]
                
                # Calculate totals for pie chart
                total_new_cases = recent_daily_data['Daily Confirmed'].sum()
                total_new_deaths = recent_daily_data['Daily Deaths'].sum()
                total_new_recovered = recent_daily_data['Daily Recovered'].sum()
                
                st.markdown("### Recent Case Activity")
                
                # Only create chart if we have data
                if total_new_cases + total_new_deaths + total_new_recovered > 0:
                    daily_distribution = {
                        'Category': ['New Cases', 'New Deaths', 'New Recoveries'],
                        'Count': [total_new_cases, total_new_deaths, total_new_recovered]
                    }
                    
                    daily_dist_df = pd.DataFrame(daily_distribution)
                    
                    # Filter out zero values
                    daily_dist_df = daily_dist_df[daily_dist_df['Count'] > 0]
                    
                    if len(daily_dist_df) > 0:
                        daily_pie_fig = px.pie(
                            daily_dist_df,
                            names='Category',
                            values='Count',
                            title=f"Last {recent_days} Days Activity",
                            color='Category',
                            color_discrete_map={
                                'New Cases': '#1E88E5',
                                'New Deaths': '#E53935',
                                'New Recoveries': '#43A047'
                            }
                        )
                        
                        daily_pie_fig.update_layout(
                            height=400,
                            legend_title="Type"
                        )
                        
                        daily_pie_fig.update_traces(
                            textposition='inside',
                            textinfo='percent+label',
                            hovertemplate='<b>%{label}</b><br>Count: %{value:,.0f}<br>Percentage: %{percent:.1%}<extra></extra>'
                        )
                        
                        st.plotly_chart(daily_pie_fig, use_container_width=True)
                    else:
                        st.info("No distribution data available for recent activity pie chart")
                else:
                    st.info("No recent activity data available for pie chart")
        else:
            st.info("No case data available for distribution analysis")
    
    # Tab 4: Regional Data
    with tabs[3]:
        st.subheader("Regional Analysis")
        
        # Get provinces data if available
        provinces = data['confirmed'][data['confirmed']['Country/Region'] == selected_country]['Province/State'].dropna().unique()
        
        if len(provinces) > 1:
            # There are multiple provinces - show breakdown
            st.write(f"Provincial/State Breakdown for {selected_country}")
            
            # Get latest date for the analysis
            latest_date = selected_date_strs[-1]
            
            # Get confirmed cases for each province
            province_data = []
            for province in provinces:
                province_row = data['confirmed'][(data['confirmed']['Country/Region'] == selected_country) & 
                                            (data['confirmed']['Province/State'] == province)]
                if len(province_row) > 0:
                    cases = province_row[latest_date].values[0]
                    province_data.append({
                        'Province': province,
                        'Cases': cases
                    })
            
            if province_data:
                province_df = pd.DataFrame(province_data)
                province_df = province_df.sort_values('Cases', ascending=False)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Create pie chart for top provinces
                    province_pie_fig = px.pie(
                        province_df.head(10),  # Show only top 10 provinces
                        names='Province',
                        values='Cases',
                        title=f"Top Provinces/States in {selected_country}"
                    )
                    
                    province_pie_fig.update_layout(height=400)
                    st.plotly_chart(province_pie_fig, use_container_width=True)
                
                with col2:
                    # Show data table of provinces
                    st.write("Provincial Data")
                    st.dataframe(province_df.head(20), height=400)
        else:
            st.info(f"No provincial/state data available for {selected_country}")
    
    # Data table view
    st.markdown("<h2 class='sub-header'>Detailed Data</h2>", unsafe_allow_html=True)
    
    with st.expander("View Raw Data Table"):
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
                '7-Day Avg (Deaths)': '{:,.1f}'
            }),
            height=300,
            use_container_width=True
        )
        
        # Download option
        csv = plot_df.to_csv(index=False)
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name=f"covid19_data_{selected_country}.csv",
            mime="text/csv"
        )

except Exception as e:
    st.error(f"Error processing data: {str(e)}")
    st.write("Please check the data structure and ensure it matches the expected JHU CSSE format.")

# Footer
st.markdown("---")
st.markdown(f"<div class='footer'>© 2025 COVID-19 Dashboard | Data from JHU CSSE<br>Last updated: {current_time} UTC<br>Created by: {current_user}</div>", unsafe_allow_html=True)