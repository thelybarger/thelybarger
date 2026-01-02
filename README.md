- 👋 Hi, I'm @thelybarger
- 👀 I'm interested in learing data science.  
- 🌱 I'm currently learning more on statistics using Python and Power Query within Power BI. 
- 💞️ I'm not looking to collaborate on anything right now.

## 🌅 Daily Morning Summary Email

This repository includes an automated daily morning summary that delivers:
- 🌤️ **Weather Report** - Current conditions and forecast
- 🚗 **Road Conditions** - Driving advisories based on weather
- 📰 **Political News Highlights** - Top 5 political stories

The summary is sent via email every morning at 7:00 AM UTC.

### Setup Instructions

To enable this feature:

1. **Get API Keys** (all free):
   - [OpenWeatherMap API](https://openweathermap.org/api) - for weather data
   - [NewsAPI](https://newsapi.org/) - for news headlines

2. **Configure Email**:
   - Use Gmail with an [App Password](https://myaccount.google.com/apppasswords)
   - Requires 2-factor authentication enabled

3. **Add GitHub Secrets**:
   - Go to: Settings → Secrets and variables → Actions → New repository secret
   - Add: `WEATHER_API_KEY`, `NEWS_API_KEY`, `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECIPIENT`, `LOCATION`
   - See [scripts/CONFIG.md](scripts/CONFIG.md) for detailed instructions

4. **Enable GitHub Actions**:
   - Go to the Actions tab and enable workflows
   - The workflow will run daily or can be triggered manually

For more details, see the [configuration guide](scripts/CONFIG.md).

<!---
thelybarger/thelybarger is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
