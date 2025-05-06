let chatTargetId = null;
let currentUserId = null;

// ✅ 设置全局 AJAX 的 CSRF Token 请求头
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    const token = $('meta[name="csrf-token"]').attr('content');
    if (token) {
      xhr.setRequestHeader('X-CSRFToken', token);
    }
  }
});

function loadMessages() {
  if (!chatTargetId || currentUserId === null) return;

  $.get("/api/messages", { with: chatTargetId }, function (response) {
    const data = response.data;
    if (!data || !Array.isArray(data.messages)) {
      console.warn("⚠️ Invalid message response format");
      return;
    }

    const box = $("#chat-box");
    box.empty();

    data.messages.forEach(function (msg) {
      const sender = msg.sender || "Unknown";
      const content = msg.content || "";
      box.append(`<p><strong>${sender}:</strong> ${content}</p>`);
    });

    box.scrollTop(box[0].scrollHeight);
  }).fail(function (xhr) {
    console.error("❌ Failed to fetch /api/messages", xhr.responseText);
  });
}

function openUserSelector() {
  $.get("/api/users", function (response) {
    const users = response.data && response.data.users;
    const ul = $("#user-list");
    ul.empty();

    if (!Array.isArray(users) || users.length === 0) {
      ul.append("<li>No users available</li>");
      return;
    }

    users.forEach(function (user) {
      const li = $("<li>").text(user.username).css("cursor", "pointer");
      li.click(function () {
        chatTargetId = user.id;
        $("#current-target").text("Chatting with: " + user.username);
        $("#user-selector").hide();
        loadMessages();
      });
      ul.append(li);
    });

    $("#user-selector").show();
  }).fail(function (xhr) {
    console.error("❌ Failed to fetch /api/users", xhr.responseText);
  });
}

$(function () {
  const idData = $("#current-user").data("user-id");
  currentUserId = idData;

  if (!currentUserId || typeof currentUserId !== 'string') {
    currentUserId = null;
    console.error("❌ Invalid user ID");
  } else {
    console.log("🔐 currentUserId =", currentUserId);
  }

  $("#select-user-btn").click(function () {
    openUserSelector();
  });

  $("#message-form").submit(function (e) {
    e.preventDefault();

    if (!chatTargetId || currentUserId === null) return;

    const message = $("#message-input").val().trim();
    if (!message) return;

    $.ajax({
      url: "/api/send_message",
      type: "POST",
      data: JSON.stringify({
        sender_id: currentUserId,
        receiver_id: chatTargetId,
        content: message
      }),
      contentType: "application/json",
      success: function () {
        console.log("✅ Message sent!");
        $("#message-input").val('');
        loadMessages();
      },
      error: function (xhr, status, error) {
        console.error("❌ Failed to send message:", xhr.responseText);
      }
    });
  });

  setInterval(loadMessages, 1000);
});
