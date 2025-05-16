$(function () {
	// When the 'submit' button is clicked (for password reset)
	$("#submit").click(function (event) {
	  event.preventDefault();  // Prevent default form submission behavior
  
	  // Select the input fields for old and new passwords
	  var oldpwdE = $("input[name=oldpwd]");
	  var newpwdE = $("input[name=newpwd]");
	  var newpwd2E = $("input[name=newpwd2]");
  
	  // Extract their values
	  var oldpwd = oldpwdE.val();
	  var newpwd = newpwdE.val();
	  var newpwd2 = newpwd2E.val();
  
	  // Send password change request to backend using custom AJAX wrapper
	  zlajax.post({
		url: "/cms/resetpwd/",  // API endpoint for resetting password
		data: {
		  oldpwd: oldpwd,
		  newpwd: newpwd,
		  newpwd2: newpwd2,
		},
		success: function (data) {
		  // If success, show toast and clear input fields
		  if (data["code"] == 200) {
			zlalert.alertSuccessToast("Password Changed!");  // Toast notification
			oldpwdE.val("");  // Clear fields
			newpwdE.val("");
			newpwd2E.val("");
		  } else {
			var message = data["message"];  // Extract error message from response
			zlalert.alertInfo(message);     // Show as alert
		  }
		},
		fail: function (error) {
		  // Handle network failure (e.g. timeout, disconnect)
		  zlalert.alertNetworkError();
		},
	  });
	});
  });