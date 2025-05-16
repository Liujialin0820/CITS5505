let chatTargetId = null;
let currentUserId = null;


// Setup global CSRF token for all AJAX requests
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    const token = $('meta[name="csrf-token"]').attr('content');
    if (token) {
      xhr.setRequestHeader('X-CSRFToken', token);
    }
  }
});

// Load chat messages between current user and selected user
function loadMessages() {
  if (!chatTargetId || currentUserId === null) return;

  $.get("/api/messages", { with: chatTargetId }, function (response) {
    const data = response.data;
    if (!data || !Array.isArray(data.messages)) {
      console.warn("Invalid message response format");
      return;
    }

    const box = $("#chat-box");
    box.empty();

    // Render each message bubble
    data.messages.forEach(function (msg) {
      const sender = msg.sender || "Unknown";
      const content = msg.content || "";
      const msgClass = (sender === $("#current-user").data("user-name")) ? 'sent' : 'received';

      const bubble = `<div class="chat-message ${msgClass}">
                        <strong>${sender}:</strong><br>${content}
                      </div>`;
      box.append(bubble);
    });

    // Auto scroll to bottom
    box.scrollTop(box[0].scrollHeight);
  }).fail(function (xhr) {
    console.error("Failed to fetch /api/messages", xhr.responseText);
  });
}

// Load list of users and open selection popup
function openUserSelector() {
  $.get("/api/users", function (response) {
    const users = response.data && response.data.users;
    const ul = $("#user-list");
    ul.empty();

    if (!Array.isArray(users) || users.length === 0) {
      ul.append("<li>No users available</li>");
      return;
    }

    // Render each user option as clickable list item
    users.forEach(function (user) {
      const li = $("<li>").text(user.username).css("cursor", "pointer");
      li.click(function () {
        chatTargetId = user.id;
        $("#current-target").text("Chatting with: " + user.username);
        $("#user-selector").hide(); // Close popup
        loadMessages(); // Load conversation
      });
      ul.append(li);
    });

    $("#user-selector").removeClass("hidden").show(); // Show popup
  }).fail(function (xhr) {
    console.error("Failed to fetch /api/users", xhr.responseText);
  });
}

$(function () {
  // Initialize current user ID from HTML data attribute
  const idData = $("#current-user").data("user-id");
  currentUserId = idData;

  if (!currentUserId || typeof currentUserId !== 'string') {
    currentUserId = null;
    console.error("Invalid user ID");
  } else {
    console.log("currentUserId =", currentUserId);
  }

  // Open user selector when button clicked
  $("#select-user-btn").click(function () {
    openUserSelector();
  });

  // Close the user selector popup
  $("#close-user-popup").click(function () {
    $("#user-selector").addClass("hidden").hide();
  });

  // Handle message sending
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
        console.log("Message sent!");
        $("#message-input").val('');
        loadMessages();
      },
      error: function (xhr, status, error) {
        console.error("Failed to send message:", xhr.responseText);
      }
    });
  });

  // Share timetable as a clickable message
  $("#share-timetable-btn").click(function () {
    if (!chatTargetId || currentUserId === null) return;

    const timetableLink = `http://127.0.0.1:5000/timetable/${currentUserId}`;
    $.ajax({
      url: "/api/send_message",
      type: "POST",
      data: JSON.stringify({
        receiver_id: chatTargetId,
        content: `Here is my timetable: <a href="${timetableLink}" class="timetable_link" target="_blank">${timetableLink}</a>`
      }),
      contentType: "application/json",
      success: function () {
        console.log("Timetable shared.");
        loadMessages();
      },
      error: function (xhr) {
        console.error("Failed to share timetable:", xhr.responseText);
      }
    });
  });

  // Periodically refresh messages every second
  setInterval(loadMessages, 1000);
});
