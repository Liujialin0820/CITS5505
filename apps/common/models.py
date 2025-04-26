from exts import db


class CourseModel(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    # One course can have multiple weekly timeslots
    timeslots = db.relationship(
        "WeeklyTimeSlot", back_populates="course", cascade="all, delete-orphan"
    )

    def add_weekly_timeslot(self, day_of_week: int, hour: int):
        """
        day_of_week: 0=Monday … 6=Sunday
        hour: hour in 24h format (0–23)
        """
        # Simple validation
        if not (1 <= day_of_week <= 7):
            raise ValueError("day_of_week must be between 1 (Monday) and 7 (Sunday)")
        if not (0 <= hour <= 23):
            raise ValueError("hour must be between 0 and 23")

        slot = WeeklyTimeSlot(day_of_week=day_of_week, hour=hour, course=self)
        db.session.add(slot)
        db.session.commit()
        return slot


class WeeklyTimeSlot(db.Model):
    __tablename__ = "weekly_timeslot"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 0 = Monday, …, 6 = Sunday
    day_of_week = db.Column(db.Integer, nullable=False)

    # Hour of the day in 24h format
    hour = db.Column(db.Integer, nullable=False)

    course_id = db.Column(
        db.Integer, db.ForeignKey("course.id", ondelete="CASCADE"), nullable=False
    )
    course = db.relationship("CourseModel", back_populates="timeslots")
