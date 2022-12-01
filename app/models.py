from app import db

class Reviews(db.Model):
    """Model which stores the information of the reviews submitted"""
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(64), index=True, nullable=False)
    locations = db.Column(db.String(120), index=True, nullable=False)
    job_title = db.Column(db.String(64), index=True, nullable=False)
    job_description = db.Column(db.String(120), index=True, nullable=False)
    hourly_pay = db.Column(db.Integer, nullable=False)
    benefits = db.Column(db.String(120), index=True, nullable=False)
    review = db.Column(db.String(120), index=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    recommendation = db.Column(db.Integer, nullable=False)
