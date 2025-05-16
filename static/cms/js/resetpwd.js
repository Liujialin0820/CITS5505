$(function () {
  $("#submit").click(function (event) {
    // Prevent default form submission behavior
    event.preventDefault();

    // Get input elements for old password, new password, and confirmation
    var oldpwdE = $("input[name=oldpwd]");
    var newpwdE = $("input[name=newpwd]");
    var newpwd2E = $("input[name=newpwd2]");

    // Get the values from input fields
    var oldpwd = oldpwdE.val();
    var newpwd = newpwdE.val();
    var newpwd2 = newpwd2E.val();

    // Send POST request to reset password endpoint
    zlajax.post({
      url: "/cms/resetpwd/",
      data: {
        oldpwd: oldpwd,
        newpwd: newpwd,
        newpwd2: newpwd2,
      },
      success: function (data) {
        // If password reset is successful
        if (data["code"] == 200) {
          zlalert.alertSuccessToast("Password Changed!");
          // Clear the input fields
          oldpwdE.val("");
          newpwdE.val("");
          newpwd2E.val("");
        } else {
          // If validation or server-side error occurs
          var message = data["message"];
          zlalert.alertInfo(message);
        }
      },
      // Handle network or server failure
      fail: function (error) {
        zlalert.alertNetworkError();
      },
    });
  });
});
