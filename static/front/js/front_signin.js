$(function () {
  // Handle login form submission
  $("#submit-btn").click(function (event) {
    event.preventDefault(); // Prevent default form submit behavior

    // Get input elements
    var email_input = $("input[name='email']");
    var password_input = $("input[name='password']");
    var remember_input = $("input[name='remember']");

    // Get values from the form fields
    var email = email_input.val();
    var password = password_input.val();
    var remember = remember_input.prop("checked") ? 1 : 0;  // Convert checkbox to integer

    // Send AJAX POST request to signin endpoint
    zlajax.post({
      url: "/signin/",
      data: {
        email: email,
        password: password,
        remember: remember,
      },
      success: function (data) {
        // If login successful, redirect to return URL or homepage
        if (data["code"] == 200) {
          var return_to = $("#return-to-span").text();
          if (return_to) {
            window.location = return_to;
          } else {
            window.location = "/";
          }
        } else {
          // Show error message if login fails
          zlalert.alertInfo(data["message"]);
        }
      },
    });
  });
});
