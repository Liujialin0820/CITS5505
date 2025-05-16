'use strict';
var zlajax = {
	// Send GET request using ajax
	'get':function(args) {
		args['method'] = 'get';
		this.ajax(args);
	},

	// Send POST request using ajax
	'post':function(args) {
		args['method'] = 'post';
		this.ajax(args);
	},

	// General ajax method that applies CSRF setup
	'ajax':function(args) {
		// Apply CSRF token setup before sending request
		this._ajaxSetup();
		$.ajax(args);
	},

	// Setup CSRF token for AJAX requests
	'_ajaxSetup': function() {
		$.ajaxSetup({
			'beforeSend':function(xhr,settings) {
				// Add CSRF token to the request header if method is not safe and request is not cross-domain
				if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    var csrftoken = $('meta[name=csrf-token]').attr('content');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
			}
		});
	}
};
