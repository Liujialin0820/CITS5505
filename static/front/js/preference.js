// -------------------------------
// 1. Load and display enrolled courses and selected timeslots
// -------------------------------
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    const csrfToken = $("meta[name='csrf-token']").attr("content");
    if (csrfToken) {
      xhr.setRequestHeader("X-CSRFToken", csrfToken);
    }
  }
});



function loadCourses() {
  const $courseSelect = $("#existing-courses");
  $courseSelect.empty();

  $.get("/my_courses/", function (res) {
    // The API directly returns an array
    const courses = Array.isArray(res) ? res : (res.courses || []);

    if (courses.length > 0) {
      const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

      courses.forEach(function (course) {
        let label = course.course_name;

        // Use course.timeslot instead of a timeslots array
        const slot = course.timeslot;
        if (slot) {
          const timeStr = `${days[slot.day_of_week-1]} ${slot.start_hour}:00 (${slot.duration_hours}h)`;
          label += ` - [${timeStr}]`;
        } else {
          label += " - ⚠️ Please select a timeslot";
        }

        const $option = $("<option>")
          .val(course.course_id)
          .text(label);
        if (!slot) {
          $option.css("color", "red");
        }
        $courseSelect.append($option);
      });
    } else {
      $courseSelect.append(
        $("<option>")
          .text("No courses enrolled yet")
          .prop("disabled", true)
      );
    }
  }).fail(function () {
    zlalert.alertNetworkError();
  });
}

// -------------------------------
// 2. Render the right-side "Modify Timeslot" panel
// -------------------------------
function renderTimeslotPanel(courseId) {
  if (!courseId) {
    return $("#timeslot-panel").html(
      "<p>Please select a course to see its timeslots.</p>"
    );
  }

  $.get(`/course_timeslots/${courseId}/`, function (res) {
    if (res.code === 200 && res.timeslots.length > 0) {
      let html = `<form id="timeslot-form"><ul class="list-group">`;
      res.timeslots.forEach(function (slot) {
        const days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];
        const label = `${days[slot.day_of_week-1]} ${slot.start_hour}:00 (${slot.duration_hours}h)`;
        html += `
          <li class="list-group-item">
            <label>
              <input type="radio" name="selected_timeslot" value="${slot.id}">
              ${label}
            </label>
          </li>`;
      });
      html += `</ul>
        <button type="submit" class="btn btn-success" style="margin-top:15px">
          Update Timeslot
        </button>
      </form>`;
      $("#timeslot-panel").html(html);
    } else {
      $("#timeslot-panel").html("<p>No timeslots available for this course.</p>");
    }
  }).fail(function () {
    $("#timeslot-panel").html("<p>Failed to load timeslots.</p>");
  });
}

// -------------------------------
// 3. All interactions inside document.ready
// -------------------------------
$(function () {
  // Initial load
  loadCourses();

  // Click “Add Course”
  $("#add_course").click(function (e) {
    e.preventDefault();
    const selectedCourseId = $("#add-course").val();
    if (!selectedCourseId) {
      return zlalert.alertInfoToast("Please select a course before adding.");
    }
    $.post("/add_enrollment/", { new_course: selectedCourseId })
      .done(function (res) {
        if (res.code === 200) {
          zlalert.alertSuccessToast("Course added successfully!");
          loadCourses();
          $("#timeslot-panel").html("<p>Please select a course to see its timeslots.</p>");
        } else {
          zlalert.alertErrorToast("Failed to add course: " + res.message);
        }
      })
      .fail(zlalert.alertNetworkError);
  });

  // Click “Remove Selected”
  $("#remove-form").click(function (e) {
    e.preventDefault();
    const selected = $("#existing-courses").val();
    if (!selected || !selected.length) {
      return zlalert.alertInfoToast("Please select at least one course to remove.");
    }
    zlalert.alertConfirm({
      title: "Confirm Removal",
      msg: "Are you sure you want to remove the selected course(s)?",
      type: "warning",
      confirmCallback: function () {
        $.ajax({
          url: "/remove_enrollment/",
          method: "POST",
          contentType: "application/json",
          data: JSON.stringify({ course_ids: selected }),
        })
          .done(function (res) {
            if (res.code === 200) {
              zlalert.alertSuccessToast("Course(s) removed successfully!");
              loadCourses();
              $("#timeslot-panel").html("<p>Please select a course to see its timeslots.</p>");
            } else {
              zlalert.alertErrorToast("Failed to remove courses: " + res.message);
            }
          })
          .fail(zlalert.alertNetworkError);
      },
    });
  });

  // Listen to course selection change, update right-side panel
  $("#existing-courses").on("change", function () {
    const sel = $(this).val();
    if (sel && sel.length === 1) {
      renderTimeslotPanel(sel[0]);
    } else {
      $("#timeslot-panel").html(
        "<p>Please select one course to see its timeslots.</p>"
      );
    }
  });

  // Submit updated timeslot
  $("#timeslot-panel").on("submit", "#timeslot-form", function (e) {
    e.preventDefault();
    const courseId = $("#existing-courses").val()[0];
    const timeslotId = $("input[name='selected_timeslot']:checked").val();
    if (!timeslotId) {
      return zlalert.alertInfoToast("Please select a timeslot.");
    }
    $.post("/update_timeslot/", { course_id: courseId, timeslot_id: timeslotId })
      .done(function (res) {
        if (res.code === 200) {
          zlalert.alertSuccessToast("Timeslot updated successfully!");
          // Refresh both course list and panel
          loadCourses();
          renderTimeslotPanel(courseId);
        } else {
          zlalert.alertErrorToast("Update failed: " + res.message);
        }
      })
      .fail(zlalert.alertNetworkError);
  });
});
