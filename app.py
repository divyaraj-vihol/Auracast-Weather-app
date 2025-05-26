from datetime import datetime
import pyowm
import streamlit as st
from matplotlib import dates
from matplotlib import pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="AuraCast", # Changed page title
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
    }

    .main-header {
        font-size: 3.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.3rem;
        color: #A23B72;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        margin: 0.7rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-card h3 {
        color: rgba(255,255,255,0.9);
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    .metric-card h2 {
        font-size: 2.2rem;
        margin-bottom: 0.3rem;
        font-weight: 700;
    }
    .metric-card p {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.7);
    }
    .weather-icon-large {
        text-align: center;
        font-size: 6rem; /* Larger icon for current weather */
        margin: 1rem 0;
        line-height: 1;
    }
    .alert-box {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #ff6b6b;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .success-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #4ecdc4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.1rem;
        font-weight: 600;
    }
    /* Dynamic background placeholder */
    .stApp {
        transition: background-image 1s ease-in-out;
    }
    .sidebar-github-link {
        text-align: center;
        margin-top: 2rem; /* More space to separate it from controls */
        margin-bottom: 1rem;
        padding-top: 1rem; /* Padding for visual separation */
        border-top: 1px solid rgba(255,255,255,0.2); /* Subtle line for separation */
    }
    .sidebar-github-link a {
        color: #F63366; /* Streamlit's primary color */
        font-size: 1.1rem;
        font-weight: bold;
        text-decoration: none;
        transition: color 0.2s ease-in-out;
    }
    .sidebar-github-link a:hover {
        color: #FF4B4B; /* A slightly brighter red */
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenWeatherMap

API_KEY = "77025ea152471af6d9a883d472946967" # Replaced with a placeholder API key. REMEMBER TO USE YOUR OWN.
owm = pyowm.OWM(API_KEY)
mgr = owm.weather_manager()

sign = u"\N{DEGREE SIGN}" # Degree symbol

# Header
st.markdown('<h1 class="main-header">🌤️ AuraCast</h1>', unsafe_allow_html=True) # Changed application name here
st.markdown('<p class="sub-header">Made By Dv - Enhanced Version</p>', unsafe_allow_html=True)

# Sidebar inputs
with st.sidebar:
    st.header("🌍 Location & Settings")
    location = st.text_input("🏙️ Enter City Name:", placeholder="e.g., London, GB or New York, US")

    col1, col2 = st.columns(2)
    with col1:
        units = st.selectbox("🌡️ Temperature Unit:", ('celsius', 'fahrenheit'))
    with col2:
        graph_type = st.selectbox("📊 Forecast Graph:", ('Interactive', 'Bar Graph', 'Line Graph'))

    st.header("📋 Display Options")
    show_current = st.checkbox("Current Weather", value=True)
    show_hourly = st.checkbox("Today's Hourly Forecast", value=True)
    show_forecast = st.checkbox("5-Day Forecast", value=True)
    show_alerts = st.checkbox("Weather Alerts", value=True)
    show_sun = st.checkbox("Sunrise/Sunset", value=True)
    show_humidity = st.checkbox("Humidity Analysis", value=True)

    # Main "Get Weather" button for the sidebar. This is the *only* one.
    get_weather_button = st.button('🔍 Get Weather', type='primary')

    # GitHub link moved to the very bottom of the sidebar
    st.markdown("---") # A horizontal rule for clear separation
    st.markdown("""
    <div class="sidebar-github-link">
        <p>Project by Divyaraj Vihol</p>
        <a href="https://github.com/divyaraj-vihol" target="_blank">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="30" height="30" style="vertical-align:middle; margin-right: 5px;">
            View on GitHub
        </a>
    </div>
    """, unsafe_allow_html=True)


degree = 'C' if units == 'celsius' else 'F'

# --- Utility Functions ---

def get_weather_icon(weather_id):
    """Maps OpenWeatherMap condition codes to emojis."""
    weather_icons = {
        # Thunderstorm
        200: "⛈️", 201: "⛈️", 202: "⛈️", 210: "🌩️", 211: "🌩️", 212: "🌩️", 221: "⛈️", 230: "⛈️", 231: "⛈️", 232: "⛈️",
        # Drizzle
        300: "🌧️", 301: "🌧️", 302: "🌧️", 310: "🌧️", 311: "🌧️", 312: "🌧️", 313: "🌧️", 314: "🌧️", 321: "🌧️",
        # Rain
        500: "🌦️", 501: "🌧️", 502: "🌧️", 503: "🌧️", 504: "🌧️", 511: "🌨️", 520: "🌧️", 521: "🌧️", 522: "🌧️", 531: "🌧️",
        # Snow
        600: "❄️", 601: "❄️", 602: "🌨️", 611: "🌨️", 612: "🌨️", 613: "🌨️", 615: "🌨️", 616: "🌨️", 620: "🌨️", 621: "🌨️", 622: "🌨️",
        # Atmosphere
        701: "🌫️", 711: "💨", 721: "🌫️", 731: "🌪️", 741: "🌫️", 761: "🌪️", 762: "🌋", 771: "🌬️", 781: "🌪️",
        # Clear
        800: "☀️",
        # Clouds
        801: "🌤️", 802: "⛅", 803: "☁️", 804: "☁️",
    }
    return weather_icons.get(weather_id, "❓") # Default icon if ID not found

def set_dynamic_background(weather_condition_id):
    """Sets the Streamlit app's background image based on weather."""
    background_images = {
        'clear': 'https://images.unsplash.com/photo-1558485233-0498a4d4b1a4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1974&q=80',
        'clouds': 'https://images.unsplash.com/photo-1506042459194-d558b90c0a37?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1974&q=80',
        'rain': 'https://images.unsplash.com/photo-1519692933481-e162a24b67d5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1974&q=80',
        'snow': 'https://images.unsplash.com/photo-1549445100-3023e1e93891?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1974&q=80',
        'thunderstorm': 'https://images.unsplash.com/photo-1563725515328-98e3b5e4c84a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1974&q=80',
        'mist': 'https://images.unsplash.com/photo-1542478465-b44f24300e84?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1974&q=80',
    }
    
    # Map weather code to a general condition for background image selection
    condition_map = {
        '2': 'thunderstorm', # 2xx Thunderstorm
        '3': 'rain',         # 3xx Drizzle
        '5': 'rain',         # 5xx Rain
        '6': 'snow',         # 6xx Snow
        '7': 'mist',         # 7xx Atmosphere
        '800': 'clear',      # 800 Clear
        '80': 'clouds',      # 80x Clouds
    }
    
    first_digit = str(weather_condition_id)[0]
    if str(weather_condition_id) == '800':
        condition = 'clear'
    elif first_digit == '8':
        condition = 'clouds'
    else:
        condition = condition_map.get(first_digit, 'clear') # Default to clear if not explicitly mapped

    bg_image = background_images.get(condition, background_images['clear']) # Fallback to clear
    
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

def get_forecast_data(location, units):
    """Retrieves and processes 5-day / 3-hour forecast data."""
    forecaster = mgr.forecast_at_place(location, '3h')
    forecast = forecaster.forecast

    daily_data = {}
    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())
        date = day.date()

        if date not in daily_data:
            daily_data[date] = {
                'temp_min': float('inf'),
                'temp_max': float('-inf'),
                'humidity_max': 0,
                'wind_max': 0,
                'pressure': [],
                'weather_ids': []
            }

        temp = weather.temperature(unit=units)['temp']
        daily_data[date]['temp_min'] = min(daily_data[date]['temp_min'], temp)
        daily_data[date]['temp_max'] = max(daily_data[date]['temp_max'], temp)
        daily_data[date]['humidity_max'] = max(daily_data[date]['humidity_max'], weather.humidity)

        if 'speed' in weather.wind():
            daily_data[date]['wind_max'] = max(daily_data[date]['wind_max'], weather.wind()['speed'])

        daily_data[date]['pressure'].append(weather.pressure['press'])
        daily_data[date]['weather_ids'].append(weather.weather_code)

    # Sort by date and take the next 5 days
    sorted_dates = sorted(daily_data.keys())
    days = sorted_dates[:5]
    
    temp_min = [daily_data[day]['temp_min'] for day in days]
    temp_max = [daily_data[day]['temp_max'] for day in days]
    humidity = [daily_data[day]['humidity_max'] for day in days]
    wind = [daily_data[day]['wind_max'] for day in days]
    pressure = [sum(daily_data[day]['pressure'])/len(daily_data[day]['pressure']) for day in days]
    
    # Get representative weather icon for each day (e.g., from the first observation of the day)
    daily_weather_icons = []
    for day in days:
        for weather in forecast:
            if datetime.utcfromtimestamp(weather.reference_time()).date() == day:
                daily_weather_icons.append(get_weather_icon(weather.weather_code))
                break
        else:
            daily_weather_icons.append("❓") # Fallback icon

    return days, temp_min, temp_max, humidity, wind, pressure, forecaster, daily_weather_icons

def get_hourly_forecast_data(location, units):
    """Retrieves hourly forecast data for the current day."""
    forecaster = mgr.forecast_at_place(location, '3h')
    forecast = forecaster.forecast

    today = datetime.now().date()
    hourly_data = {
        'time': [],
        'temp': [],
        'humidity': [],
        'wind_speed': [],
        'status': [],
        'weather_icon': []
    }

    for weather in forecast:
        timestamp = datetime.utcfromtimestamp(weather.reference_time())
        if timestamp.date() == today:
            hourly_data['time'].append(timestamp.strftime('%H:%M'))
            hourly_data['temp'].append(weather.temperature(unit=units)['temp'])
            hourly_data['humidity'].append(weather.humidity)
            hourly_data['wind_speed'].append(weather.wind().get('speed', 0))
            hourly_data['status'].append(weather.detailed_status.title())
            hourly_data['weather_icon'].append(get_weather_icon(weather.weather_code))
    return hourly_data

# --- Display Functions ---

def display_current_weather(weather, location_info):
    """Displays current weather conditions."""
    st.markdown("## 🌡️ Current Weather")
    
    temp = weather.temperature(unit=units)['temp']
    temp_felt = weather.temperature(unit=units)['feels_like']
    current_icon = get_weather_icon(weather.weather_code)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f'<div class="weather-icon-large">{current_icon}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f"### 📍 {location_info.name}, {location_info.country}")
        st.markdown(f"## {round(temp)}{sign}{degree}")
        st.markdown(f"**Feels like: {round(temp_felt)}{sign}{degree}**")
        st.markdown(f"**{weather.detailed_status.title()}**")
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💧 Humidity", f"{weather.humidity}%")
    with col2:
        wind_speed = weather.wind().get('speed', 0)
        st.metric("💨 Wind Speed", f"{wind_speed} m/s")
    with col3:
        st.metric("☁️ Cloud Cover", f"{weather.clouds}%")
    with col4:
        st.metric("⏲️ Pressure", f"{weather.pressure['press']} hPa")

def display_hourly_forecast(hourly_data):
    """Displays today's hourly forecast using Plotly."""
    st.markdown("## ⏰ Today's Hourly Forecast")

    if not hourly_data['time']:
        st.info("No hourly forecast available for today.")
        return

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hourly_data['time'], y=hourly_data['temp'], mode='lines+markers', name='Temperature',
                             line=dict(color='#ff5349', width=3), marker=dict(size=8)))

    for i in range(len(hourly_data['time'])):
        fig.add_annotation(x=hourly_data['time'][i], y=hourly_data['temp'][i],
                           text=f"{round(hourly_data['temp'][i])}{sign}",
                           showarrow=False, yshift=10)

    fig.update_layout(
        title_text="Temperature by Hour Today",
        xaxis_title="Time",
        yaxis_title=f"Temperature ({sign}{degree})",
        height=400,
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Hourly Details:")
    # Display hourly details in a dynamic number of columns
    num_cols = min(len(hourly_data['time']), 5)
    cols_per_row = st.columns(num_cols)
    
    for i, _time in enumerate(hourly_data['time']):
        with cols_per_row[i % num_cols]:
            st.markdown(f"**{_time}**")
            st.markdown(f"{hourly_data['weather_icon'][i]}")
            st.markdown(f"{round(hourly_data['temp'][i])}{sign}{degree}")
            st.markdown(f"💧 {hourly_data['humidity'][i]}%")
            st.markdown(f"💨 {hourly_data['wind_speed'][i]} m/s")


def create_interactive_forecast(days, temp_min, temp_max, humidity, wind, pressure, daily_weather_icons):
    """Creates and displays interactive 5-day forecast charts using Plotly."""
    st.markdown("## 📊 Interactive 5-Day Forecast")

    tab1, tab2, tab3 = st.tabs(["Temperature & Overview", "Humidity & Wind", "Pressure"])

    with tab1:
        fig_temp_overview = go.Figure()
        fig_temp_overview.add_trace(
            go.Scatter(x=days, y=temp_min, name='Min Temp',
                       line=dict(color='#42bff4', width=3), marker=dict(size=8), mode='lines+markers')
        )
        fig_temp_overview.add_trace(
            go.Scatter(x=days, y=temp_max, name='Max Temp',
                       line=dict(color='#ff5349', width=3), marker=dict(size=8), mode='lines+markers')
        )
        
        annotations = []
        for i, day in enumerate(days):
            annotations.append(dict(
                x=day, y=temp_max[i] + 5,
                text=daily_weather_icons[i],
                showarrow=False,
                font=dict(size=24)
            ))
        fig_temp_overview.update_layout(annotations=annotations)

        fig_temp_overview.update_layout(
            height=450,
            title_text="5-Day Temperature Forecast with Weather Overview",
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title=f"Temperature ({sign}{degree})",
            hovermode="x unified",
            legend_title_text="Temperature"
        )
        st.plotly_chart(fig_temp_overview, use_container_width=True)

    with tab2:
        fig_hum_wind = make_subplots(rows=1, cols=2, subplot_titles=('Humidity Levels', 'Wind Speed'))

        fig_hum_wind.add_trace(
            go.Bar(x=days, y=humidity, name='Humidity', marker_color='#4ecdc4'),
            row=1, col=1
        )
        fig_hum_wind.add_trace(
            go.Scatter(x=days, y=wind, name='Wind Speed',
                       line=dict(color='#95e1d3', width=3), marker=dict(size=8), mode='lines+markers'),
            row=1, col=2
        )
        fig_hum_wind.update_yaxes(title_text="Humidity (%)", row=1, col=1)
        fig_hum_wind.update_yaxes(title_text="Wind Speed (m/s)", row=1, col=2)
        fig_hum_wind.update_layout(height=450, showlegend=True, title_text="Humidity and Wind Forecast", title_x=0.5)
        st.plotly_chart(fig_hum_wind, use_container_width=True)

    with tab3:
        fig_pressure = go.Figure()
        fig_pressure.add_trace(
            go.Bar(x=days, y=pressure, name='Pressure', marker_color='#f38ba8')
        )
        fig_pressure.update_layout(
            height=450,
            title_text="Atmospheric Pressure Forecast",
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Pressure (hPa)",
            showlegend=False
        )
        st.plotly_chart(fig_pressure, use_container_width=True)


def create_traditional_graphs(days, temp_min, temp_max, graph_type):
    """Creates and displays traditional Matplotlib graphs for temperature forecast."""
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 6))

    if graph_type == 'Bar Graph':
        x_pos = range(len(days))
        width = 0.35

        bars1 = ax.bar([x - width/2 for x in x_pos], temp_min, width,
                      label='Min Temp', color='#42bff4', alpha=0.8, edgecolor='black')
        bars2 = ax.bar([x + width/2 for x in x_pos], temp_max, width,
                      label='Max Temp', color='#ff5349', alpha=0.8, edgecolor='black')

        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{int(height)}{sign}', ha='center', va='bottom', fontsize=9, color='white',
                        bbox=dict(facecolor='black', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))

        ax.set_xticks(x_pos)
        ax.set_xticklabels([day.strftime('%m/%d') for day in days], rotation=45, ha='right')

    else:  # Line Graph
        ax.plot(days, temp_min, label='Min Temp', color='#42bff4',
                marker='o', linewidth=3, markersize=8, linestyle='--')
        ax.plot(days, temp_max, label='Max Temp', color='#ff5349',
                marker='o', linewidth=3, markersize=8, linestyle='-')

        for i, txt in enumerate(temp_min):
            ax.annotate(f'{int(txt)}{sign}', (days[i], temp_min[i]), textcoords="offset points", xytext=(0,-15), ha='center', color='#42bff4')
        for i, txt in enumerate(temp_max):
            ax.annotate(f'{int(txt)}{sign}', (days[i], temp_max[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#ff5349')

        ax.xaxis.set_major_formatter(dates.DateFormatter('%m/%d'))
        fig.autofmt_xdate()

    ax.set_xlabel('Date', fontsize=12, color='#333')
    ax.set_ylabel(f'Temperature ({sign}{degree})', fontsize=12, color='#333')
    ax.set_title('5-Day Temperature Forecast', fontsize=18, fontweight='bold', color='#333')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.5, linestyle=':')
    ax.tick_params(axis='x', colors='#333')
    ax.tick_params(axis='y', colors='#333')
    ax.set_facecolor('#f8f8f8')
    fig.patch.set_facecolor('white')

    st.pyplot(fig)
    plt.close()

def display_weather_alerts(forecaster):
    """Displays weather alerts based on forecast data."""
    st.markdown("## ⚠️ Weather Alerts")

    alerts = []
    if forecaster.will_have_rain():
        alerts.append(("🌧️", "Rain Alert", "Rain expected in the forecast period."))
    if forecaster.will_have_snow():
        alerts.append(("❄️", "Snow Alert", "Snow expected in the forecast period."))
    if forecaster.will_have_storm():
        alerts.append(("🌩️", "Storm Alert", "Storms expected in the forecast period."))
    if forecaster.will_have_fog():
        alerts.append(("🌫️", "Fog Alert", "Foggy conditions expected."))
    
    # Check for significant clouds
    cloudy_entries = 0
    total_entries = 0
    for weather in forecaster.forecast:
        total_entries += 1
        if weather.clouds > 50:
            cloudy_entries += 1
    
    if total_entries > 0 and (cloudy_entries / total_entries) > 0.5:
        alerts.append(("☁️", "Cloud Alert", "Predominantly cloudy conditions expected."))

    if not alerts:
        alerts.append(("☀️", "Sunny Outlook", "Mostly sunny and clear conditions are expected."))

    if alerts:
        for emoji, title, description in alerts:
            box_class = "success-box" if "Sunny Outlook" in title else "alert-box"
            st.markdown(f"""
            <div class="{box_class}">
                <h4>{emoji} {title}</h4>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
            <h4>✅ No Major Weather Alerts</h4>
            <p>Clear weather conditions expected for the forecast period.</p>
        </div>
        """, unsafe_allow_html=True)

def display_sun_times(weather):
    """Displays sunrise and sunset times."""
    st.markdown("## 🌅 Sunrise & Sunset")
    
    sunrise_time = datetime.fromtimestamp(weather.sunrise_time())
    sunset_time = datetime.fromtimestamp(weather.sunset_time())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌅 Sunrise</h3>
            <h2>{sunrise_time.strftime('%H:%M:%S')}</h2>
            <p>{sunrise_time.strftime('%B %d, %Y')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌇 Sunset</h3>
            <h2>{sunset_time.strftime('%H:%M:%S')}</h2>
            <p>{sunset_time.strftime('%B %d, %Y')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    daylight_duration = sunset_time - sunrise_time
    hours, remainder = divmod(daylight_duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    st.info(f"☀️ **Daylight Duration:** {hours} hours and {minutes} minutes")

def create_humidity_chart(days, humidity):
    """Creates and displays a humidity forecast chart."""
    st.markdown("## 💧 Humidity Analysis")
    
    fig = go.Figure(data=[
        go.Bar(x=days, y=humidity,
                marker_color='rgba(66, 191, 244, 0.8)',
                marker_line_color='rgba(66, 191, 244, 1.0)',
                marker_line_width=2)
    ])
    
    fig.update_layout(
        title="5-Day Humidity Forecast",
        xaxis_title="Date",
        yaxis_title="Humidity (%)",
        showlegend=False,
        height=400,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    for i, v in enumerate(humidity):
        fig.add_annotation(
            x=days[i], y=v,
            text=f"{v}%",
            showarrow=False,
            yshift=10
        )
    
    st.plotly_chart(fig, use_container_width=True)

# --- Main App Logic with Tabs ---

weather_tab, about_tab = st.tabs(["🌤️ Weather Forecast", "ℹ️ About This Project"])

with weather_tab:
    # This logic now correctly references the single 'get_weather_button'
    if get_weather_button:
        if not location:
            st.warning('⚠️ Please provide a city name!')
        else:
            with st.spinner('🌤️ Fetching weather data...'):
                try:
                    # Get current weather
                    obs = mgr.weather_at_place(location)
                    current_weather = obs.weather
                    location_info = obs.location
                    
                    # Set dynamic background based on current weather
                    set_dynamic_background(current_weather.weather_code)

                    # Get forecast data
                    days, temp_min, temp_max, humidity, wind, pressure, forecaster, daily_weather_icons = get_forecast_data(location, units)

                    # Get hourly forecast data
                    hourly_data = get_hourly_forecast_data(location, units)
                    
                    # Display sections based on sidebar checkboxes
                    if show_current:
                        display_current_weather(current_weather, location_info)
                        st.markdown("---")
                    
                    if show_hourly:
                        display_hourly_forecast(hourly_data)
                        st.markdown("---")

                    if show_forecast:
                        if graph_type == 'Interactive':
                            create_interactive_forecast(days, temp_min, temp_max, humidity, wind, pressure, daily_weather_icons)
                        else:
                            st.markdown("## 📈 Temperature Forecast")
                            create_traditional_graphs(days, temp_min, temp_max, graph_type)
                        st.markdown("---")
                    
                    if show_alerts:
                        display_weather_alerts(forecaster)
                        st.markdown("---")
                    
                    if show_sun:
                        display_sun_times(current_weather)
                        st.markdown("---")
                    
                    if show_humidity:
                        create_humidity_chart(days, humidity)
                        st.markdown("---")
                    
                    st.success("✅ Weather data loaded successfully!")
                    
                except pyowm.commons.exceptions.NotFoundError:
                    st.error("🔍 Location not found! Try adding country code (e.g., 'London, GB')")
                except Exception as e:
                    st.error(f"❌ Error fetching weather data: {str(e)}")

with about_tab:
    st.markdown("## 📖 About This Project")
    st.markdown("""
    Welcome to **AuraCast**, a comprehensive web application designed to provide you with up-to-date and future weather information for any city worldwide. Built with **Streamlit** for the interactive user interface and powered by the **OpenWeatherMap API** through the **`pyowm`** Python library, this tool offers a rich visual experience.

    ### Key Features:
    * **Current Weather Conditions:** Get real-time temperature, humidity, wind speed, cloud cover, and atmospheric pressure.
    * **Today's Hourly Forecast:** See detailed hourly predictions for the current day to plan your immediate activities.
    * **5-Day Temperature Forecast:** Visualize temperature trends for the next five days using interactive Plotly charts or traditional Matplotlib graphs.
    * **Comprehensive Weather Alerts:** Receive warnings for rain, snow, storms, fog, and significant cloud cover, or a "Sunny Outlook" when conditions are clear.
    * **Sunrise & Sunset Times:** Know the exact times for dawn and dusk, along with total daylight duration.
    * **Humidity Analysis:** Track humidity levels over the forecast period.
    * **Dynamic Backgrounds:** Experience a visually engaging interface with backgrounds that change based on current weather conditions.

    ### Technologies Used:
    * **Streamlit:** For building the interactive web application with minimal code.
    * **PyOWM:** A Python wrapper for the OpenWeatherMap API, simplifying data retrieval.
    * **Plotly:** For creating interactive and detailed charts.
    * **Matplotlib:** For traditional statistical plotting.
    * **Python:** The core programming language.

    This project aims to demonstrate the power of combining modern web frameworks with robust weather APIs to create a user-friendly and informative application.

    ---
    """)

# Footer with your name
st.markdown("""
    ---
    <p style="text-align:center; font-size:20px; color:#00bfff;">
        Made by <a href="https://github.com/divyaraj-vihol" style="color:#00bfff; text-decoration:none;"><b>Divyaraj Vihol</b></a>
    </p>
""", unsafe_allow_html=True)