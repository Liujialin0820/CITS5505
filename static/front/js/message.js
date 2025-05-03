let chatTargetId = null;
let currentUserId = null;

function loadMessages() {
  if (!chatTargetId || currentUserId === null) return;

  $.get("/api/messages", { with: chatTargetId }, function (data) {
    let box = $("#chat-box");
    box.empty();
    data.messages.forEach(function (msg) {
      box.append("<p>" + msg.sender + ": " + msg.content + "</p>");
    });
    box.scrollTop(box[0].scrollHeight);
  });
}

function openUserSelector() {
  $.get("/api/users", function (data) {
    let ul = $("#user-list");
    ul.empty();
    data.users.forEach(function (user) {
      let li = $("<li>").text(user.username).css("cursor", "pointer");
      li.click(function () {
        chatTargetId = user.id;
        $("#current-target").text("Chatting with: " + user.username);
        $("#user-selector").hide();
        loadMessages();
      });
      ul.append(li);
    });
    $("#user-selector").show();
  });
}

$(function () {
  // 从隐藏 div 中获取用户 ID
  currentUserId = parseInt($("#current-user").data("user-id")) || null;

  $("#message-form").submit(function (e) {
    e.preventDefault();
    if (!chatTargetId || currentUserId === null) return;

    let message = $("#message-input").val();

    zlajax.post({
      url: "/api/send_message",
      data: {
        receiver_id: chatTargetId,
        content: message,
      },
      success: function () {
        $("#message-input").val("");
        loadMessages();
      },
    });
  });

  setInterval(loadMessages, 1000);
});
