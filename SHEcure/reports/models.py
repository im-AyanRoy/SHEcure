from django.db import models

class HarassmentReport(models.Model):
    HARASSMENT_TYPE_CHOICES = [
    ('arson', 'Arson'),
    ('assault', 'Assault'),
    ('burglary', 'Burglary'),
    ('counterfeiting', 'Counterfeiting'),
    ('cybercrime', 'Cybercrime'),
    ('domestic_violence', 'Domestic Violence'),
    ('drug_offense', 'Drug Offense'),
    ('extortion', 'Extortion'),
    ('firearm_offense', 'Firearm Offense'),
    ('fraud', 'Fraud'),
    ('homicide', 'Homicide'),
    ('identity_theft', 'Identity Theft'),
    ('illegal_possession', 'Illegal Possession'),
    ('kidnapping', 'Kidnapping'),
    ('public_intoxication', 'Public Intoxication'),
    ('robbery', 'Robbery'),
    ('sexual_assault', 'Sexual Assault'),
    ('shoplifting', 'Shoplifting'),
    ('traffic_violation', 'Traffic Violation'),
    ('vandalism', 'Vandalism'),
    ('vehicle_stolen', 'Vehicle - Stolen'),
]
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    harassment_type = models.CharField(max_length=100, choices=HARASSMENT_TYPE_CHOICES)
    REPORTER_TYPE_CHOICES = [
        ('victim', 'Victim'),
        ('non-victim', 'Non-Victim'), 
    ]
    reported_by = models.CharField(max_length=50, choices=REPORTER_TYPE_CHOICES, default='victim')
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)  # New field for latitude
    longitude = models.FloatField(null=True, blank=True)  # New field for longitude
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.location} - {self.harassment_type}"

class PredictedHotspot(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    prediction_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Predicted Hotspot at ({self.latitude}, {self.longitude})"

class Upvote(models.Model):
    ip_address = models.GenericIPAddressField(blank=True, null=True)  # Store the user's IP address
    report = models.ForeignKey(HarassmentReport, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('ip_address', 'report')  # Ensure one IP can only upvote a report once

class Comment(models.Model):
    report = models.ForeignKey(HarassmentReport, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.report.location} at {self.created_at}"