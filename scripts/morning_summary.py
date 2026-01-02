#!/usr/bin/env python3
"""
Daily Morning Summary Script

This script fetches:
1. Weather report and road conditions
2. Political highlights from news
3. Sends a comprehensive summary email
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import requests


def get_weather_data(location, api_key):
    """
    Fetch weather data from OpenWeatherMap API
    
    Args:
        location: City name or coordinates
        api_key: OpenWeatherMap API key
    
    Returns:
        dict: Weather data
    """
    if not api_key:
        return {"error": "No Weather API key provided. Sign up at https://openweathermap.org/api"}
    
    try:
        # Current weather
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        current = response.json()
        
        # 5-day forecast
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=imperial"
        forecast_response = requests.get(forecast_url, timeout=10)
        forecast_response.raise_for_status()
        forecast = forecast_response.json()
        
        return {
            "current": current,
            "forecast": forecast,
            "error": None
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Weather API error: {str(e)}"}


def get_news_data(api_key):
    """
    Fetch political news from NewsAPI
    
    Args:
        api_key: NewsAPI key
    
    Returns:
        dict: News articles
    """
    if not api_key:
        return {"error": "No News API key provided. Sign up at https://newsapi.org/"}
    
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": api_key,
            "country": "us",
            "category": "politics",
            "pageSize": 5
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"News API error: {str(e)}"}


def format_weather_summary(weather_data):
    """
    Format weather data into readable text
    
    Args:
        weather_data: Weather data from API
    
    Returns:
        str: Formatted weather summary
    """
    if weather_data.get("error"):
        return f"⚠️ Weather Update:\n{weather_data['error']}\n\n"
    
    current = weather_data.get("current", {})
    
    if not current:
        return "⚠️ Weather Update:\nNo weather data available\n\n"
    
    summary = "🌤️ WEATHER REPORT\n"
    summary += "=" * 50 + "\n\n"
    
    # Current conditions
    temp = current.get("main", {}).get("temp", "N/A")
    feels_like = current.get("main", {}).get("feels_like", "N/A")
    description = current.get("weather", [{}])[0].get("description", "N/A").title()
    humidity = current.get("main", {}).get("humidity", "N/A")
    wind_speed = current.get("wind", {}).get("speed", "N/A")
    
    summary += f"Location: {current.get('name', 'Unknown')}\n"
    summary += f"Current Temperature: {temp}°F (feels like {feels_like}°F)\n"
    summary += f"Conditions: {description}\n"
    summary += f"Humidity: {humidity}%\n"
    summary += f"Wind Speed: {wind_speed} mph\n\n"
    
    # Road conditions advisory
    summary += "🚗 ROAD CONDITIONS:\n"
    if "rain" in description.lower() or "snow" in description.lower():
        summary += "⚠️ Wet/slippery conditions expected. Drive carefully!\n"
    elif "fog" in description.lower() or "mist" in description.lower():
        summary += "⚠️ Reduced visibility. Use caution while driving!\n"
    elif wind_speed > 25:
        summary += "⚠️ High winds. Be careful with high-profile vehicles!\n"
    else:
        summary += "✅ Normal driving conditions expected.\n"
    
    summary += "\n"
    
    # Forecast preview
    forecast = weather_data.get("forecast", {})
    if forecast and "list" in forecast:
        summary += "📅 TODAY'S FORECAST:\n"
        today_forecasts = forecast["list"][:3]  # Next 9 hours (3-hour intervals)
        for item in today_forecasts:
            time = datetime.fromtimestamp(item["dt"]).strftime("%I:%M %p")
            temp = item["main"]["temp"]
            desc = item["weather"][0]["description"].title()
            summary += f"  {time}: {temp}°F - {desc}\n"
    
    return summary + "\n"


def format_news_summary(news_data):
    """
    Format news data into readable text
    
    Args:
        news_data: News data from API
    
    Returns:
        str: Formatted news summary
    """
    if news_data.get("error"):
        return f"⚠️ News Update:\n{news_data['error']}\n\n"
    
    articles = news_data.get("articles", [])
    
    if not articles:
        return "⚠️ News Update:\nNo political news available\n\n"
    
    summary = "📰 POLITICAL HIGHLIGHTS\n"
    summary += "=" * 50 + "\n\n"
    
    for i, article in enumerate(articles, 1):
        title = article.get("title", "No title")
        source = article.get("source", {}).get("name", "Unknown source")
        description = article.get("description", "No description available")
        url = article.get("url", "")
        
        summary += f"{i}. {title}\n"
        summary += f"   Source: {source}\n"
        summary += f"   {description}\n"
        if url:
            summary += f"   Read more: {url}\n"
        summary += "\n"
    
    return summary


def send_email(subject, body, sender, password, recipient):
    """
    Send email via SMTP
    
    Args:
        subject: Email subject
        body: Email body
        sender: Sender email address
        password: Sender email password/app password
        recipient: Recipient email address
    """
    if not all([sender, password, recipient]):
        print("❌ Email credentials not configured. Printing summary instead:\n")
        print(body)
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send via Gmail SMTP (adjust for other providers)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent successfully to {recipient}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        print("\nSummary that would have been sent:\n")
        print(body)
        return False


def main():
    """Main function to orchestrate the morning summary"""
    
    print("🌅 Starting Daily Morning Summary Generation...")
    print("=" * 50)
    
    # Get configuration from environment variables
    weather_api_key = os.getenv('WEATHER_API_KEY', '')
    news_api_key = os.getenv('NEWS_API_KEY', '')
    email_sender = os.getenv('EMAIL_SENDER', '')
    email_password = os.getenv('EMAIL_PASSWORD', '')
    email_recipient = os.getenv('EMAIL_RECIPIENT', '')
    location = os.getenv('LOCATION', 'New York')
    
    print(f"\n📍 Location: {location}")
    print(f"📧 Recipient: {email_recipient or 'Not configured - will print to console'}\n")
    
    # Fetch weather data
    print("Fetching weather data...")
    weather_data = get_weather_data(location, weather_api_key)
    
    # Fetch news data
    print("Fetching political news...")
    news_data = get_news_data(news_api_key)
    
    # Create summary
    today = datetime.now().strftime("%A, %B %d, %Y")
    
    summary = f"""
{'=' * 50}
DAILY MORNING SUMMARY
{today}
{'=' * 50}

{format_weather_summary(weather_data)}

{format_news_summary(news_data)}

{'=' * 50}
Have a great day!
{'=' * 50}
"""
    
    # Send email
    subject = f"Daily Morning Summary - {today}"
    print("\nSending email...")
    send_email(subject, summary, email_sender, email_password, email_recipient)
    
    print("\n✅ Morning summary process completed!")


if __name__ == "__main__":
    main()
