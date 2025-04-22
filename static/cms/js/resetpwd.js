$(function () {
    $("#submit").click(function (event) {
        // event.preventDefault
        event.preventDefault();

        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        zlajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {
                console.log(data);
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    });
});