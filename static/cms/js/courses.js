/**
 * Created by hynev on 2017/12/29.
 */

$(function () {
  $("#add-course-btn").click(function (event) {
    event.preventDefault();
    zlalert.alertOneInput({
      text: "add new course name",
      placeholder: "course name",
      confirmCallback: function (inputValue) {
        zlajax.post({
          url: "/cms/acourse/",
          data: {
            name: inputValue,
          },
          success: function (data) {
            if (data["code"] == 200) {
              window.location.reload();
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
  $(".edit-course-btn").click(function () {
    var self = $(this);
    var tr = self.parent().parent();
    var name = tr.attr("data-name");
    var course_id = tr.attr("data-id");

    zlalert.alertOneInput({
      text: "change name",
      placeholder: name,
      confirmCallback: function (inputValue) {
        zlajax.post({
          url: "/cms/ucourse/",
          data: {
            course_id: course_id,
            name: inputValue,
          },
          success: function (data) {
            if (data["code"] == 200) {
              window.location.reload();
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
  $(".delete-course-btn").click(function (event) {
    var self = $(this);
    var tr = self.parent().parent();
    var course_id = tr.attr("data-id");
    zlalert.alertConfirm({
      msg: "Delete?",
      confirmCallback: function () {
        zlajax.post({
          url: "/cms/dcourse/",
          data: {
            course_id: course_id,
          },
          success: function (data) {
            if (data["code"] == 200) {
              window.location.reload();
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
  // 打开“添加时段”模态框
  $('.add-timeslot-btn').click(function () {
    var tr = $(this).closest('tr');
    $('#modal-course-id').val(tr.data('id'));
    $('#modal-timeslot-id').val('');
    $('#modal-day').val(1);
    $('#modal-hour').val(0);
    $('#timeslotModal').modal('show');
  });

  // 打开“编辑时段”模态框
  $('.edit-timeslot-btn').click(function () {
    var btn = $(this);
    $('#modal-timeslot-id').val(btn.data('id'));
    $('#modal-course-id').val(btn.closest('tr').data('id'));
    $('#modal-day').val(btn.data('day'));
    $('#modal-hour').val(btn.data('hour'));
    $('#timeslotModal').modal('show');
  });

  // 删除时段
  $('.delete-timeslot-btn').click(function () {
    var id = $(this).data('id');
    zlalert.alertConfirm({
      text: "Confirm delete this timeslot?",
      confirmCallback: function () {
        zlajax.post({
          url: '/cms/dtimeslot/',
          data: { timeslot_id: id },
          success: function (data) {
            if (data.code == 200) window.location.reload();
            else zlalert.alertInfo(data.message);
          }
        });
      }
    });
  });

  // 保存（添加或更新）时段
  $('#save-timeslot-btn').click(function () {
    var formData = $('#timeslot-form').serialize();
    var url = $('#modal-timeslot-id').val() ? '/cms/utimeslot/' : '/cms/add_timeslot/';
    zlajax.post({
      url: url,
      data: formData,
      success: function (data) {
        if (data.code == 200) window.location.reload();
        else zlalert.alertInfo(data.message);
      }
    });
  });
});
