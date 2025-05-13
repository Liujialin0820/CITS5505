from exts import db


class CourseModel(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    # One course can have multiple weekly timeslots
    timeslots = db.relationship(
        "WeeklyTimeSlot", back_populates="course", cascade="all, delete-orphan"
    )
    
    @staticmethod
    def get_all_courses_with_times():
        courses = CourseModel.query.all()
        result = []
        for course in courses:
            course_data = {
                "course_id": course.id,
                "course_name": course.name,
                "timeslots": []
            }
            for ts in course.timeslots:
                course_data["timeslots"].append({
                    "day_of_week": ts.day_of_week,
                    "start_hour": ts.start_hour,
                    "duration_hours": ts.duration_hours
                })
            result.append(course_data)
        return result
    
    def add_weekly_timeslot(
        self, day_of_week: int, start_hour: int, duration_hours: int
    ):
        """
        Add a weekly timeslot for the course.

        day_of_week: 0=Monday … 6=Sunday
        start_hour: starting hour in 24h format (0–23)
        duration_hours: how many hours the class lasts
        """
        if not (0 <= day_of_week <= 6):
            raise ValueError("day_of_week must be between 0 (Monday) and 6 (Sunday)")
        if not (0 <= start_hour <= 23):
            raise ValueError("start_hour must be between 0 and 23")
        if not (1 <= duration_hours <= 24):
            raise ValueError("duration_hours must be between 1 and 24")

        end_hour = start_hour + duration_hours

        # Check for time conflicts with existing slots on the same day
        for ts in self.timeslots:
            if ts.day_of_week != day_of_week:
                continue

            existing_start = ts.start_hour
            existing_end = ts.start_hour + ts.duration_hours

            # Check if time intervals overlap
            if not (end_hour <= existing_start or start_hour >= existing_end):
                raise ValueError(
                    f"Time conflict with existing timeslot: {existing_start}:00–{existing_end}:00"
                )

        slot = WeeklyTimeSlot(
            day_of_week=day_of_week,
            start_hour=start_hour,
            duration_hours=duration_hours,
            course=self,
        )
        db.session.add(slot)
        db.session.commit()
        return slot


class WeeklyTimeSlot(db.Model):
    __tablename__ = "weekly_timeslot"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Day of the week: 0 = Monday, ..., 6 = Sunday
    day_of_week = db.Column(db.Integer, nullable=False)

    # Start hour of the class in 24h format (e.g., 14 = 2 PM)
    start_hour = db.Column(db.Integer, nullable=False)

    # Duration in hours (e.g., 2 = two-hour class)
    duration_hours = db.Column(db.Integer, nullable=False)

    # Foreign key to the course
    course_id = db.Column(
        db.Integer, db.ForeignKey("course.id", ondelete="CASCADE"), nullable=False
    )

    # Relationship to CourseModel
    course = db.relationship("CourseModel", back_populates="timeslots")

    # All enrollments linked to this timeslot
    enrollments = db.relationship(
        "Enrollment", back_populates="timeslot", cascade="all, delete-orphan"
    )
