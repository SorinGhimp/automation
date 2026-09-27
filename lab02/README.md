# IW02 - Creating a Python Script to Interact with an API

## Description

This project contains a Python script that interacts with the Currency Exchange Rate API.

The script receives:
- source currency;
- target currency;
- date;

from command-line arguments, requests the exchange rate from the API and saves the response in JSON format.

The available data period is from `2025-01-01` to `2025-09-15`.

## Requirements

- Python 3
- Docker
- Docker Compose
- Python `requests` library

## Installation

Install the required Python library:

```bash
python -m pip install requests