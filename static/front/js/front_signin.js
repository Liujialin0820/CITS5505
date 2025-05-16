/**
 * Created by hynev on 2017/12/26.
 */

$(function () {
  // When the login 'submit' button is clicked
  $("#submit-btn").click(function (event) {
    event.preventDefault();  // Prevent default form submission behavior

    // Grab input elements
    var email_input = $("input[name='email']");
    var password_input = $("input[name='password']");
    var remember_input = $("input[name='remember']");

    // Extract values from input fields
    var email = email_input.val();
    var password = password_input.val();
    var remember = remember_input.prop("checked") ? 1 : 0;  // Convert checkbox to 0 or 1

    // Send login request using custom AJAX utility
    zlajax.post({
      url: "/signin/",  // Backend endpoint for sign-in
      data: {
        email: email,
        password: password,
        remember: remember,  // Whether 'remember me' is checked
      },
      success: function (data) {
        // If login is successful (code 200)
        if (data["code"] == 200) {
          var return_to = $("#return-to-span").text();  // Optional redirect target
          if (return_to) {
            window.location = return_to;  // Redirect to original destination if provided
          } else {
            window.location = "/";  // Default redirect to homepage
          }
        } else {
          // Show error message from backend
          zlalert.alertInfo(data["message"]);
        }
      },
    });
  });
});

