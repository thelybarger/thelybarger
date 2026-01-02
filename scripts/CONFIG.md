# Daily Morning Summary Email - Configuration Template

This file shows the environment variables needed for the morning summary script.
Do not commit actual API keys or passwords to the repository!

## Required GitHub Secrets

To use this automation, configure the following secrets in your GitHub repository:
Settings → Secrets and variables → Actions → New repository secret

### Weather API (OpenWeatherMap)
- **WEATHER_API_KEY**: Your OpenWeatherMap API key
  - Sign up for free at: https://openweathermap.org/api
  - Free tier includes current weather and 5-day forecast

### News API
- **NEWS_API_KEY**: Your NewsAPI key
  - Sign up for free at: https://newsapi.org/
  - Free tier includes 100 requests per day

### Email Configuration
- **EMAIL_SENDER**: Your Gmail address (e.g., yourname@gmail.com)
- **EMAIL_PASSWORD**: Gmail App Password (not your regular password!)
  - Generate at: https://myaccount.google.com/apppasswords
  - Requires 2-factor authentication enabled
- **EMAIL_RECIPIENT**: Email address to receive the summary

### Location
- **LOCATION**: City name for weather report (e.g., "New York", "Los Angeles", "Chicago")

## Local Testing

For local testing, create a `.env` file (DO NOT commit this file):

```
WEATHER_API_KEY=your_weather_api_key_here
NEWS_API_KEY=your_news_api_key_here
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_RECIPIENT=recipient@email.com
LOCATION=Your City
```

Then run:
```bash
pip install -r scripts/requirements.txt
python scripts/morning_summary.py
```

## Notes

- The workflow runs daily at 7:00 AM UTC (adjust in `.github/workflows/daily-summary.yml`)
- You can manually trigger the workflow from the Actions tab
- If email sending fails, the summary will be printed to the workflow logs
