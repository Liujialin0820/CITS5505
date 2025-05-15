window.addEventListener('DOMContentLoaded', function () {
    // Get the course data from a global variable injected via the template
    const courses = window.coursesData || [];
  
    // The container where upcoming events will be rendered
    const eventContainer = document.getElementById('event');
  
    // Weekday names to convert numeric days to readable labels
    const weekdayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  
    // Preset color palette to visually distinguish different courses
    const courseColors = [
      '#90caf9', '#a5d6a7', '#ffcc80',
      '#ce93d8', '#f48fb1', '#bcaaa4',
      '#fff59d', '#80cbc4', '#ef9a9a'
    ];
  
    // A map to assign consistent color per course
    const courseColorMap = {};
    let colorIndex = 0;
  
    // Iterate through each course
    courses.forEach(course => {
      // Assign a color if the course doesn't already have one
      if (!courseColorMap[course.course_name]) {
        courseColorMap[course.course_name] = courseColors[colorIndex % courseColors.length];
        colorIndex++;
      }
  
      const color = courseColorMap[course.course_name];
  
      // ✅ Sort the timeslots by weekday and start hour for consistent display order
      const sortedSlots = [...course.timeslots].sort((a, b) => {
        if (a.day_of_week === b.day_of_week) {
          return a.start_hour - b.start_hour;
        }
        return a.day_of_week - b.day_of_week;
      });
  
      // For each timeslot, create and insert a DOM element into the event panel
      sortedSlots.forEach(ts => {
        const eventBox = document.createElement('div');
        eventBox.className = 'event';
        eventBox.style.borderLeft = `5px solid ${color}`;  // Color indicator on the left
  
        const title = document.createElement('div');
        title.className = 'event-title';
        title.innerText = course.course_name;
  
        const day = document.createElement('div');
        day.className = 'event-day';
        day.innerText = weekdayNames[ts.day_of_week - 1];
  
        const time = document.createElement('div');
        time.className = 'event-time';
        time.innerText = `${ts.start_hour}:00 - ${ts.start_hour + ts.duration_hours}:00`;
  
        // Combine and append to the main container
        eventBox.appendChild(title);
        eventBox.appendChild(day);
        eventBox.appendChild(time);
  
        eventContainer.appendChild(eventBox);
      });
    });
  });
  