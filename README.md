# Reddit & Stock Scraper

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

**Reddit & Stock Scraper** is a Python application that allows you to scrape comments from Reddit subs and organize them into a clear conversation structure in JSON format. Additionally, it provides fundamental stock data using the Alpha Vantage API. The application features a console menu for selecting between Reddit scraping and Alpha Vantage stock data retrieval. Configuration for Reddit subs and other parameters are managed through a config file.

## Features

- **Reddit Scraping**: Scrape comments from specified subreddits and organize them in a conversational format.
- **Alpha Vantage API**: Retrieve fundamental stock data for specified symbols.
- **Configurable Parameters**: Manage parameters and subreddit selections via a config file.
- **Console Menu**: Select between Reddit scraping and stock data retrieval through an easy-to-use console menu.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/aleodev/bot-scraper.git
    cd bot-scraper
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the configuration**:
    - Edit `definitions.py` & `config.json` to include your Reddit sub preferences and Alpha Vantage API keys and other preferences.

## Usage

1. **Run the application**:
    ```bash
    python main.py
    ```

2. **Navigate the Console Menu**:
    - Select `1` to scrape comments from Reddit subs.
    - Select `2` to use the Alpha Vantage API for stock data.

## Configuration

The application uses a configuration file (`config.ini`) & (`definitions.py`) to manage settings.
