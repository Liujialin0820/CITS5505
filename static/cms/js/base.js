// Handles sidebar navigation toggling and style adjustments
$(function () {
    $('.nav-sidebar>li>a').click(function (event) {
        var that = $(this);  // Store reference to the clicked <a> element

        // Prevent default navigation if href is "#"
        if(that.children('a').attr('href') == '#'){
            event.preventDefault();
        }

        // Toggle 'unfold' class: open submenu if closed, close if already open
        if(that.parent().hasClass('unfold')){
            that.parent().removeClass('unfold');  // Collapse current item
        } else {
            that.parent().addClass('unfold')      // Expand current item
                .siblings().removeClass('unfold'); // Collapse siblings
        }

        console.log('coming....');  // Debug message
    });

    // Remove underline on mouse leave for all sidebar links
    $('.nav-sidebar a').mouseleave(function () {
        $(this).css('text-decoration','none');
    });
});


// Automatically highlight and expand the correct sidebar section based on current URL
$(function () {
    var url = window.location.href;  // Get the current URL

    // Profile page
    if(url.indexOf('profile') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(0).addClass('active').siblings().removeClass('active');
    } 
    // Password reset page
    else if(url.indexOf('resetpwd') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(1).addClass('active').siblings().removeClass('active');
    } 
    // Email reset page
    else if(url.indexOf('resetemail') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(2).addClass('active').siblings().removeClass('active');
    } 
    // Posts management
    else if(url.indexOf('posts') >= 0){
        var postManageLi = $('.post-manage');
        postManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
    // Boards management
    else if(url.indexOf('boards') >= 0){
        var boardManageLi = $('.board-manage');
        boardManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
    // Permissions management
    else if(url.indexOf('permissions') >= 0){
        var permissionManageLi = $('.permission-manage');
        permissionManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
    // Roles management
    else if(url.indexOf('roles') >= 0){
        var roleManageLi = $('.role-manage');
        roleManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
    // User accounts management
    else if(url.indexOf('users') >= 0){
        var userManageLi = $('.user-manage');
        userManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
    // CMS user accounts
    else if(url.indexOf('cmsuser_manage') >= 0){
        var cmsuserManageLi = $('.cmsuser-manage');
        cmsuserManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
    // CMS role management
    else if(url.indexOf('cmsrole_manage') >= 0){
        var cmsroleManageLi = $('.cmsrole-manage');
        cmsroleManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
    // Comments moderation
    else if(url.indexOf('comments') >= 0) {
        var commentsManageLi = $('.comments-manage');
        commentsManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
});
