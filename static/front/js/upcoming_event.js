window.addEventListener('DOMContentLoaded', function () {
    const courses = window.coursesData || [];
    const eventContainer = document.getElementById('event');
    const weekdayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  
    const courseColors = [
      '#90caf9', '#a5d6a7', '#ffcc80',
      '#ce93d8', '#f48fb1', '#bcaaa4',
      '#fff59d', '#80cbc4', '#ef9a9a'
    ];
    const courseColorMap = {};
    let colorIndex = 0;
  
    courses.forEach(course => {
      if (!courseColorMap[course.course_name]) {
        courseColorMap[course.course_name] = courseColors[colorIndex % courseColors.length];
        colorIndex++;
      }
  
      const color = courseColorMap[course.course_name];
  
      // ✅ 排序一下 timeslots，保证显示顺序统一（星期 + 时间）
      const sortedSlots = [...course.timeslots].sort((a, b) => {
        if (a.day_of_week === b.day_of_week) {
          return a.start_hour - b.start_hour;
        }
        return a.day_of_week - b.day_of_week;
      });
  
      sortedSlots.forEach(ts => {
        const eventBox = document.createElement('div');
        eventBox.className = 'event';
        eventBox.style.borderLeft = `5px solid ${color}`;
  
        const title = document.createElement('div');
        title.className = 'event-title';
        title.innerText = course.course_name;
  
        const day = document.createElement('div');
        day.className = 'event-day';
        day.innerText = weekdayNames[ts.day_of_week - 1];
  
        const time = document.createElement('div');
        time.className = 'event-time';
        time.innerText = `${ts.start_hour}:00 - ${ts.start_hour + ts.duration_hours}:00`;
  
        eventBox.appendChild(title);
        eventBox.appendChild(day);
        eventBox.appendChild(time);
  
        eventContainer.appendChild(eventBox);
      });
    });
  });
  