import csv
import os
from datetime import datetime

def load_data(file_path):
    """
    Loads data from a CSV file.
    Assumes the first row is the header.
    Returns a list of dictionaries, where each dictionary represents a row.
    """
    data = []
    if not os.path.exists(file_path):
        return data

    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='|')
        for row in reader:
            data.append(row)
    return data

def save_data(file_path, data):
    """
    Saves data (list of dictionaries) to a CSV file.
    The keys of the first dictionary are used as the header.
    """
    if not data:
        # If data is empty, create an empty file or clear existing content
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            pass
        return

    fieldnames = data[0].keys()
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        writer.writerows(data)

def validate_amount(amount_str):
    """
    Validates if a string represents a positive integer amount (in paisa/cents).
    Returns the integer amount if valid, otherwise None.
    """
    try:
        amount = int(amount_str)
        if amount > 0:
            return amount
    except ValueError:
        pass
    return None

def validate_date(date_str):
    """
    Validates and parses a date string in YYYY-MM-DD format.
    Returns a datetime object if valid, otherwise None.
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None

