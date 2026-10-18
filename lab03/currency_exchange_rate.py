import argparse
import json
import logging
import os
import sys
from datetime import datetime

import requests


# Adresa API-ului
API_URL = os.getenv(
    "API_URL",
    "http://host.docker.internal:8080/"
)

# Directorul principal al proiectului
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directorul pentru rezultatele JSON
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Fișierul pentru erori
ERROR_LOG = os.path.join(PROJECT_ROOT, "error.log")


# Configurarea fișierului de log
logging.basicConfig(
    filename=ERROR_LOG,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_arguments():
    """
    Citește parametrii transmiși din linia de comandă.
    """
    parser = argparse.ArgumentParser(
        description="Get currency exchange rate for a specific date."
    )

    parser.add_argument(
        "from_currency",
        help="Currency to convert from, e.g. USD"
    )

    parser.add_argument(
        "to_currency",
        help="Currency to convert to, e.g. EUR"
    )

    parser.add_argument(
        "date",
        help="Date in YYYY-MM-DD format"
    )

    return parser.parse_args()


def validate_date(date_string):
    """
    Verifică formatul și perioada datei.
    """

    try:
        date = datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(
            "Invalid date format. Use YYYY-MM-DD."
        )

    min_date = datetime.strptime(
        "2025-01-01",
        "%Y-%m-%d"
    ).date()

    max_date = datetime.strptime(
        "2025-09-15",
        "%Y-%m-%d"
    ).date()

    if date < min_date or date > max_date:
        raise ValueError(
            "Date must be between 2025-01-01 and 2025-09-15."
        )


def get_api_key():
    """
    Obține API key-ul din variabila de mediu.
    """

    api_key = os.getenv("API_KEY")

    if not api_key:
        raise RuntimeError(
            "API_KEY environment variable is not set."
        )

    return api_key


def get_exchange_rate(from_currency, to_currency, date):
    """
    Trimite cererea către API și returnează răspunsul.
    """

    api_key = get_api_key()

    params = {
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "date": date
    }

    data = {
        "key": api_key
    }

    try:
        response = requests.post(
            API_URL,
            params=params,
            data=data,
            timeout=10
        )

        response.raise_for_status()

    except requests.RequestException as error:
        raise RuntimeError(
            f"API request failed: {error}"
        )

    try:
        result = response.json()
    except ValueError:
        raise RuntimeError(
            "API returned invalid JSON."
        )

    # API-ul poate întoarce o eroare în câmpul "error"
    if result.get("error"):
        raise RuntimeError(
            result["error"]
        )

    return result


def save_result(result, from_currency, to_currency, date):
    """
    Salvează rezultatul primit de la API în format JSON.
    """

    # Creează folderul data dacă nu există
    os.makedirs(DATA_DIR, exist_ok=True)

    filename = (
        f"{from_currency.upper()}_"
        f"{to_currency.upper()}_"
        f"{date}.json"
    )

    filepath = os.path.join(
        DATA_DIR,
        filename
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False
        )

    return filepath


def main():
    """
    Funcția principală a programului.
    """

    args = parse_arguments()

    from_currency = args.from_currency
    to_currency = args.to_currency
    date = args.date

    try:

        # Verificăm data
        validate_date(date)

        # Cerem cursul de schimb de la API
        result = get_exchange_rate(
            from_currency,
            to_currency,
            date
        )

        # Salvăm rezultatul
        filepath = save_result(
            result,
            from_currency,
            to_currency,
            date
        )

        print("Exchange rate received successfully.")
        print(json.dumps(result, indent=4))
        print(f"Data saved to: {filepath}")

    except Exception as error:

        # Afișăm eroarea în terminal
        print(f"ERROR: {error}")

        # Salvăm eroarea în error.log
        logging.error(str(error))

        sys.exit(1)


if __name__ == "__main__":
    main()