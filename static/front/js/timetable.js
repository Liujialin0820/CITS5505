window.addEventListener('load', function () {
  // Scroll to 9:00 AM
  const body = document.querySelector('.calendar-body');
  if (body) {
    body.scrollTop = 540;
  }

  const courses = window.coursesData;
  const grid = document.querySelector('.calendar-grid');

  const cellHeight = 60;                // Height of each hourly cell
  const timeColumnWidth = 80;           // Width of the first "Time" column
  const totalGridWidth = grid.offsetWidth;  // Total width of the calendar grid

  const dayColumnWidth = Math.floor((totalGridWidth - timeColumnWidth) / 7); // Width per day column
  const lastColumnWidth = totalGridWidth - timeColumnWidth - dayColumnWidth * 6; // Adjusted width for last column (Sunday)

  // 🎨 Automatically assign a color to each course
  const courseColors = [
    '#90caf9', '#a5d6a7', '#ffcc80',
    '#ce93d8', '#f48fb1', '#bcaaa4',
    '#fff59d', '#80cbc4', '#ef9a9a'
  ];
  const courseColorMap = {}; // Mapping of course names to colors
  let colorIndex = 0; // Used to assign colors in order

  // Loop through each course to create visual blocks
  courses.forEach(course => {
    // If the course has no color assigned yet, assign one
    if (!courseColorMap[course.course_name]) {
      courseColorMap[course.course_name] = courseColors[colorIndex % courseColors.length];
      colorIndex++;
    }
    const bgColor = courseColorMap[course.course_name];

    // Loop through the timeslots and display each as a block
    course.timeslots.forEach(ts => {
      const block = document.createElement('div');
      block.className = 'class-block';
      block.innerText = course.course_name;

      const top = ts.start_hour * cellHeight; // Top position based on start hour
      const height = ts.duration_hours * cellHeight; // Height based on duration
      const left = timeColumnWidth + (ts.day_of_week - 1) * dayColumnWidth; // Left position based on day
      const width = (ts.day_of_week === 7) ? lastColumnWidth : dayColumnWidth; // Use lastColumnWidth for Sunday

      // Set block styles
      block.style.position = 'absolute';
      block.style.top = `${top}px`;
      block.style.left = `${left}px`;
      block.style.width = `${width}px`;
      block.style.height = `${height}px`;
      block.style.backgroundColor = bgColor;
      block.style.color = '#000';
      block.style.display = 'flex';
      block.style.alignItems = 'center';
      block.style.justifyContent = 'center';
      block.style.fontSize = '12px';
      block.style.fontWeight = 'bold';
      block.style.borderRadius = '4px';
      block.style.border = '1px solid #333';
      block.style.boxSizing = 'border-box';
      block.style.zIndex = '5';

      grid.appendChild(block); // Add the block to the calendar grid
    });
  });

  // Day labels for events
  const weekdayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const eventContainer = document.getElementById('event');

  // Display upcoming events based on timeslots
  courses.forEach(course => {
  const color = courseColorMap[course.course_name];

  course.timeslots.forEach(ts => {
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

      eventContainer.appendChild(eventBox); // Add the event to the event panel
  });
  });

  // Recalculate block sizes when window is resized
  function resizeClassBlocks() {
      const grid = document.querySelector('.calendar-grid');
      const totalGridWidth = grid.offsetWidth;
      const timeColumnWidth = 80;
      const dayColumnWidth = Math.floor((totalGridWidth - timeColumnWidth) / 7);
  
      document.querySelectorAll('.class-block').forEach(block => {
          const day = parseInt(block.dataset.day); // 0–6
          const startHour = parseInt(block.dataset.startHour);
          const duration = parseInt(block.dataset.duration);
  
          const left = timeColumnWidth + day * dayColumnWidth;
          const top = startHour * 60;
          const height = duration * 60;
  
          block.style.left = `${left}px`;
          block.style.top = `${top}px`;
          block.style.width = `${dayColumnWidth}px`;
          block.style.height = `${height}px`;
      });
  }
  
  // Trigger resize logic on window load and resize
  window.addEventListener('load', resizeClassBlocks);
  window.addEventListener('resize', resizeClassBlocks);

  // Reload page completely when window is resized (fallback)
  window.addEventListener('resize', () => {
      location.reload(); // Quick and dirty: reload on window resize
  });
});
