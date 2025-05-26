# 🌤️ Weather Forecaster

A user-friendly Streamlit application to get current weather conditions and a 5-day forecast for any city worldwide. This enhanced version provides interactive charts, detailed weather metrics, and insightful analysis.


## ⚙️Structure
auracast-weather-app/
├── .gitignore
├── README.md
├── LICENSE
├── requirements.txt
├── app.py
└── assets/
    ├── auracast_screenshot.png
    └── app_icon.png

## ✨ Features

* **Current Weather Display:** Get real-time temperature, "feels like" temperature, detailed status (e.g., "scattered clouds"), humidity, wind speed, cloud cover, and atmospheric pressure.
* **5-Day Forecast:** View temperature (min/max), humidity, wind, and pressure forecasts for the next five days.
* **Interactive Charts:** Visualize forecast data with interactive Plotly graphs for a comprehensive overview.
* **Traditional Graphs:** Option to display temperature forecasts using classic Matplotlib bar or line graphs.
* **Weather Alerts:** Receive notifications for anticipated rain, snow, storms, fog, or cloudy conditions.
* **Sunrise & Sunset Times:** See precise sunrise and sunset times for the selected location, along with daylight duration.
* **Humidity Analysis:** Dedicated chart for 5-day humidity forecast.
* **Customizable Units:** Switch between Celsius and Fahrenheit for temperature display.
* **Responsive Design:** Optimized for various screen sizes using Streamlit's layout features.

## 🚀 How to Run Locally

1.  **Clone the repository (if applicable):**
    ```bash
    git clone [https://github.com/divyaraj-vihol/weather-forecaster.git](https://github.com/divyaraj-vihol/weather-forecaster.git)
    cd weather-forecaster
    ```
    (If you don't have a repository yet, just save `app.py` and `requirements.txt` in a folder.)

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate 
    ```

3.  **Install dependencies:**
    Create a `requirements.txt` file in the same directory as `app.py` with the following content:
    ```
    streamlit
    pyowm
    matplotlib
    plotly
    ```
    Then, install them:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Get an OpenWeatherMap API Key:**
    * Go to [https://openweathermap.org/api](https://openweathermap.org/api)
    * Sign up for a free account.
    * After signing up, you'll find your API key on your account page.
    * **Replace `"77025ea152471af6d9a883d472946967"` in `app.py` with your actual API key.**
        ```python
        API_KEY = "YOUR_API_KEY_HERE"
        ```
        *Note: The key in the provided `app.py` is a demo key and might have limitations or expire.*

5.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
    This will open the app in your default web browser.

## 🛠️ Technologies Used

* **Streamlit:** For creating the interactive web application.
* **PyOWM:** Python wrapper for the OpenWeatherMap API.
* **Matplotlib:** For traditional static graphs.
* **Plotly:** For interactive and visually appealing data visualizations.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<p align="center">Made by <b>Divyaraj Vihol</b></p>