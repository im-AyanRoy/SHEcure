import os
import django
import pandas as pd
import sys
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Set up Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # Add project directory to system path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harassment_platform.settings')
django.setup()

from reports.models import HarassmentReport  # Import your model

# Initialize geocoder
geolocator = Nominatim(user_agent="harassment_report_app")

# Function to fetch latitude & longitude from location
def get_lat_lon(location):
    try:
        geo_data = geolocator.geocode(location, timeout=10)  # 10 sec timeout for better reliability
        if geo_data:
            return geo_data.latitude, geo_data.longitude
    except GeocoderTimedOut:
        print(f"⏳ Timeout while fetching coordinates for {location}")
    return None, None  # Return None if geocoding fails

# Correct file path for the Excel file
file_path = os.path.join(BASE_DIR, "reports", "cleaned-crime-dataset.csv")

# Check if file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ File not found: {file_path}")

# Load Excel file
df = pd.read_csv(file_path)

# Ensure column names match model fields
df = df.rename(columns={
    "Location": "location",
    "Date": "date",
    "Time": "time",
    "Harassment Type": "harassment_type",
    "Reported By": "reported_by",
    "Description": "description"
})

# Add latitude & longitude columns by geocoding locations
df["latitude"], df["longitude"] = zip(*df["location"].apply(get_lat_lon))

# Filter out rows where location lookup failed
df = df.dropna(subset=["latitude", "longitude"])

# Convert to list of HarassmentReport objects
reports = [
    HarassmentReport(
        location=row["location"],
        date=row["date"],
        time=row["time"],
        harassment_type=row["harassment_type"],
        reported_by=row["reported_by"],
        description=row["description"],
        latitude=row["latitude"],
        longitude=row["longitude"]
    )
    for _, row in df.iterrows()
]

# Bulk insert records
HarassmentReport.objects.bulk_create(reports)

print(f"✅ {len(reports)} reports imported successfully!")
