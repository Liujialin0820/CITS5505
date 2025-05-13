// -------------------------------
// 1. 加载并展示学生选课与已选时间
// -------------------------------
function loadCourses() {
  const $courseSelect = $("#existing-courses");
  $courseSelect.empty();

  $.get("/my_courses/", function (res) {
    // 接口直接返回数组
    const courses = Array.isArray(res) ? res : (res.courses || []);

    if (courses.length > 0) {
      const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

      courses.forEach(function (course) {
        let label = course.course_name;

        // 使用 course.timeslot 而不是 timeslots 数组
        const slot = course.timeslot;
        if (slot) {
          const timeStr = `${days[slot.day_of_week]} ${slot.start_hour}:00 (${slot.duration_hours}h)`;
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
// 2. 渲染右侧“修改时间”面板
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
        const label = `${days[slot.day_of_week]} ${slot.start_hour}:00 (${slot.duration_hours}h)`;
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
// 3. 所有交互放到一个 document.ready
// -------------------------------
$(function () {
  // 初始加载
  loadCourses();

  // 点击“Add Course”
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

  // 点击“Remove Selected”
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

  // 监听左侧课程选择变化，渲染右侧面板
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

  // 提交更新 timeslot
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
          // 刷新左右两边
          loadCourses();
          renderTimeslotPanel(courseId);
        } else {
          zlalert.alertErrorToast("Update failed: " + res.message);
        }
      })
      .fail(zlalert.alertNetworkError);
  });
});
