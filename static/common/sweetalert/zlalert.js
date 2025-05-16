var zlalert = {
  /*
        Function: Show error alert
        Parameters:
            - msg: The message to display (optional)
    */
  alertError: function (msg) {
    swal("Notice", msg, "error");
  },
  /*
        Function: Show info/warning alert
        Parameters:
            - msg: The message to display (optional)
    */
  alertInfo: function (msg) {
    swal("Notice", msg, "warning");
  },
  /*
        Function: Show an info alert with custom title
        Parameters:
            - title: The alert title
            - msg: The message to display (optional)
    */
  alertInfoWithTitle: function (title, msg) {
    swal(title, msg);
  },
  /*
        Function: Show a success alert
        Parameters:
            - msg: The success message (required)
            - confirmCallback: Function to execute on confirmation (optional)
    */
  alertSuccess: function (msg, confirmCallback) {
    args = {
      title: "Notice",
      text: msg,
      type: "success",
    };
    swal(args, confirmCallback);
  },
  /*
        Function: Show a success alert with a custom title
        Parameters:
            - title: The alert title (required)
            - msg: The success message (required)
    */
  alertSuccessWithTitle: function (title, msg) {
    swal(title, msg, "success");
  },
  /*
        Function: Show a confirmation alert
        Parameters: A dictionary
            - title: Alert title (optional)
            - type: Alert type (optional)
            - confirmText: Confirm button text (optional)
            - cancelText: Cancel button text (optional)
            - msg: Alert message (required)
            - confirmCallback: Function for confirm button (optional)
            - cancelCallback: Function for cancel button (optional)
    */
  alertConfirm: function (params) {
    swal(
      {
        title: params["title"] ? params["title"] : "Notice",
        showCancelButton: true,
        showConfirmButton: true,
        type: params["type"] ? params["type"] : "",
        confirmButtonText: params["confirmText"] ? params["confirmText"] : "OK",
        cancelButtonText: params["cancelText"]
          ? params["cancelText"]
          : "Cancel",
        text: params["msg"] ? params["msg"] : "",
      },
      function (isConfirm) {
        if (isConfirm) {
          if (params["confirmCallback"]) {
            params["confirmCallback"]();
          }
        } else {
          if (params["cancelCallback"]) {
            params["cancelCallback"]();
          }
        }
      }
    );
  },
  /*
        Function: Show an alert with an input box
        Parameters: A dictionary
            - title: Alert title (optional)
            - text: Alert message (optional)
            - placeholder: Input placeholder (optional)
            - confirmText: Confirm button text (optional)
            - cancelText: Cancel button text (optional)
            - confirmCallback: Function to run with the input value
    */
  alertOneInput: function (params) {
    swal(
      {
        title: params["title"] ? params["title"] : "Please enter",
        text: params["text"] ? params["text"] : "",
        type: "input",
        showCancelButton: true,
        animation: "slide-from-top",
        closeOnConfirm: false,
        showLoaderOnConfirm: true,
        inputPlaceholder: params["placeholder"] ? params["placeholder"] : "",
        confirmButtonText: params["confirmText"] ? params["confirmText"] : "OK",
        cancelButtonText: params["cancelText"]
          ? params["cancelText"]
          : "Cancel",
      },
      function (inputValue) {
        if (inputValue === false) return false;
        if (inputValue === "") {
          swal.showInputError("Input cannot be empty!");
          return false;
        }
        if (params["confirmCallback"]) {
          params["confirmCallback"](inputValue);
        }
      }
    );
  },
  /*
        Function: Show network error
        Parameters: None
    */
  alertNetworkError: function () {
    this.alertErrorToast("Network error");
  },
  /*
        Function: Show info toast (disappears after 1s)
        Parameters:
            - msg: Message to display
    */
  alertInfoToast: function (msg) {
    this.alertToast(msg, "info");
  },
  /*
        Function: Show error toast (disappears after 1s)
        Parameters:
            - msg: Message to display
    */
  alertErrorToast: function (msg) {
    this.alertToast(msg, "error");
  },
  /*
        Function: Show success toast (disappears after 1s)
        Parameters:
            - msg: Message to display
    */
  alertSuccessToast: function (msg) {
    if (!msg) {
      msg = "Success!";
    }
    this.alertToast(msg, "success");
  },
  /*
        Function: Core toast method (disappears after 1s)
        Parameters:
            - msg: Message to display
            - type: Type of toast (info/success/error)
    */
  alertToast: function (msg, type) {
    swal({
      title: msg,
      text: "",
      type: type,
      showCancelButton: false,
      showConfirmButton: false,
      timer: 1000,
    });
  },
  // Function: Close the current dialog
  close: function () {
    swal.close();
  },
};
