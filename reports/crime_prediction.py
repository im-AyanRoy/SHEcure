import numpy as np
from scipy.stats import gaussian_kde
from .models import HarassmentReport

def predict_crime_hotspot():
    # Get all reports with latitude & longitude
    reports = HarassmentReport.objects.exclude(latitude=None, longitude=None)

    if reports.count() < 3:  # Ensure enough data points for KDE
        return None  # Not enough data to predict

    # Convert data into numpy array
    locations = np.array([[report.latitude, report.longitude] for report in reports]).T  # Transpose for KDE

    # Apply Kernel Density Estimation (KDE)
    kde = gaussian_kde(locations)

    # Evaluate density at all reported locations
    densities = kde(locations)

    # Find the highest density location (the most probable next hotspot)
    max_density_index = np.argmax(densities)
    hotspot_lat, hotspot_lng = locations[:, max_density_index]

    return {'lat': hotspot_lat, 'lng': hotspot_lng}
