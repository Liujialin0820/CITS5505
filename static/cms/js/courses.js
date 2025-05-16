/**
 * Created by hynev on 2017/12/29.
 */

$(function () {
  // Handle click on 'Add Course' button
  $("#add-course-btn").click(function (event) {
    event.preventDefault();  // Prevent default form submission

    zlalert.alertOneInput({
      text: "add new course name",       // Dialog message
      placeholder: "course name",        // Input placeholder text
      confirmCallback: function (inputValue) {
        zlajax.post({
          url: "/cms/acourse/",          // Backend route for adding a course
          data: { name: inputValue },    // Send course name entered
          success: function (data) {
            if (data["code"] == 200) {
              window.location.reload();  // Reload on success
            } else {
              zlalert.alertInfo(data["message"]);  // Show error message
            }
          },
        });
      },
    });
  });
});


$(function () {
  // Handle click on 'Edit Course' button
  $(".edit-course-btn").click(function () {
    var self = $(this);
    var tr = self.parent().parent();           // Get the parent <tr>
    var name = tr.attr("data-name");           // Original course name
    var course_id = tr.attr("data-id");        // Course ID

    zlalert.alertOneInput({
      text: "change name",                     // Prompt message
      placeholder: name,                       // Pre-fill current name
      confirmCallback: function (inputValue) {
        zlajax.post({
          url: "/cms/ucourse/",                // Backend route for updating course
          data: {
            course_id: course_id,
            name: inputValue,
          },
          success: function (data) {
            if (data["code"] == 200) {
              window.location.reload();        // Reload page on success
            } else {
              zlalert.alertInfo(data["message"]);  // Show error message
            }
          },
        });
      },
    });
  });
});


$(function () {
  // Handle click on 'Delete Course' button
  $(".delete-course-btn").click(function (event) {
    var self = $(this);
    var tr = self.parent().parent();
    var course_id = tr.attr("data-id");

    zlalert.alertConfirm({
      msg: "Delete?",  // Confirmation prompt
      confirmCallback: function () {
        zlajax.post({
          url: "/cms/dcourse/",  // Backend route for deleting course
          data: {
            course_id: course_id,
          },
          success: function (data) {
            if (data["code"] == 200) {
              window.location.reload();  // Reload if deletion successful
            } else {
              zlalert.alertInfo(data["message"]);
            }
          },
        });
      },
    });
  });
});


$(function () {
  // Open modal to add new timeslot
  $('.add-timeslot-btn').click(function () {
    var tr = $(this).closest('tr');
    $('#modal-course-id').val(tr.data('id'));       // Set course ID
    $('#modal-timeslot-id').val('');                // Clear timeslot ID
    $('#modal-day').val(1);                         // Default: Monday
    $('#modal-hour').val(0);                        // Default: 00:00
    $('#timeslotModal').modal('show');              // Open modal
  });

  // Open modal to edit existing timeslot
  $('.edit-timeslot-btn').click(function () {
    var btn = $(this);
    $('#modal-timeslot-id').val(btn.data('id'));            // Set timeslot ID
    $('#modal-course-id').val(btn.closest('tr').data('id')); // Set course ID
    $('#modal-day').val(btn.data('day'));                   // Fill day
    $('#modal-hour').val(btn.data('hour'));                 // Fill hour
    $('#timeslotModal').modal('show');                      // Show modal
  });

  // Confirm deletion of a timeslot
  $('.delete-timeslot-btn').click(function () {
    var id = $(this).data('id');
    zlalert.alertConfirm({
      text: "Confirm delete this timeslot?",
      confirmCallback: function () {
        zlajax.post({
          url: '/cms/dtimeslot/',      // Backend route to delete timeslot
          data: { timeslot_id: id },
          success: function (data) {
            if (data.code == 200) window.location.reload();  // Refresh on success
            else zlalert.alertInfo(data.message);            // Show error message
          }
        });
      }
    });
  });

  // Submit form to save (add or update) timeslot
  $('#save-timeslot-btn').click(function () {
    var formData = $('#timeslot-form').serialize();  // Gather form data
    var url = $('#modal-timeslot-id').val() ? '/cms/utimeslot/' : '/cms/add_timeslot/';  // Choose endpoint based on whether editing or adding
    zlajax.post({
      url: url,
      data: formData,
      success: function (data) {
        if (data.code == 200) window.location.reload();  // Reload page
        else zlalert.alertInfo(data.message);            // Show error message
      }
    });
  });
});