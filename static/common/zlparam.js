var zlparam = {
    // Function to set or update a query parameter in the URL
    setParam: function (href, key, value) {
        var isReplaced = false;
        var urlArray = href.split('?');

        // Check if URL already has query parameters
        if(urlArray.length > 1){
            var queryArray = urlArray[1].split('&');

            // Loop through existing parameters to find a match
            for(var i=0; i < queryArray.length; i++){
                var paramsArray = queryArray[i].split('=');
                if(paramsArray[0] == key){
                    // Replace the existing parameter value
                    paramsArray[1] = value;
                    queryArray[i] = paramsArray.join('=');
                    isReplaced = true;
                    break;
                }
            }

            // If the parameter was not found, append it
            if(!isReplaced){
                var params = {};
                params[key] = value;
                if(urlArray.length > 1){
                    href = href + '&' + $.param(params);
                }else{
                    href = href + '?' + $.param(params);
                }
            }else{
                // Rebuild the full query string with updated value
                var params = queryArray.join('&');
                urlArray[1] = params;
                href = urlArray.join('?');
            }
        }else{
            // If no query parameters exist, add one
            var param = {};
            param[key] = value;
            if(urlArray.length > 1){
                href = href + '&' + $.param(param);
            }else{
                href = href + '?' + $.param(param);
            }
        }

        return href;  // Return updated URL
    }
};
