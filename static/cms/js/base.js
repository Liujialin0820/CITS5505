// Handle sidebar navigation click events
$(function () {
    $('.nav-sidebar>li>a').click(function (event) {
        var that = $(this);
        // Prevent default action if href is '#'
        if(that.children('a').attr('href') == '#'){
            event.preventDefault();
        }
        // Toggle 'unfold' class on the clicked item
        if(that.parent().hasClass('unfold')){
            that.parent().removeClass('unfold');
        }else{
            that.parent().addClass('unfold').siblings().removeClass('unfold');
        }
        console.log('coming....');  // Debug message
    });

    // Remove underline on mouse leave
    $('.nav-sidebar a').mouseleave(function () {
        $(this).css('text-decoration','none');
    });
});

// Automatically highlight menu items based on URL
$(function () {
    var url = window.location.href;

    // Profile - Info
    if(url.indexOf('profile') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(0).addClass('active').siblings().removeClass('active');
    
    // Profile - Reset Password
    } else if(url.indexOf('resetpwd') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(1).addClass('active').siblings().removeClass('active');
    
    // Profile - Reset Email
    } else if(url.indexOf('resetemail') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(2).addClass('active').siblings().removeClass('active');
    
    // Post management
    } else if(url.indexOf('posts') >= 0){
        var postManageLi = $('.post-manage');
        postManageLi.addClass('unfold').siblings().removeClass('unfold');
    
    // Board management
    }else if(url.indexOf('boards') >= 0){
        var boardManageLi = $('.board-manage');
        boardManageLi.addClass('unfold').siblings().removeClass('unfold');
    
    // Permission management
    }else if(url.indexOf('permissions') >= 0){
        var permissionManageLi = $('.permission-manage');
        permissionManageLi.addClass('unfold').siblings().removeClass('unfold');
    
    // Role management
    }else if(url.indexOf('roles') >= 0){
        var roleManageLi = $('.role-manage');
        roleManageLi.addClass('unfold').siblings().removeClass('unfold');
    
    // User management
    }else if(url.indexOf('users') >= 0){
        var userManageLi = $('.user-manage');
        userManageLi.addClass('unfold').siblings().removeClass('unfold');
    
    // CMS user management
    }else if(url.indexOf('cmsuser_manage') >= 0){
        var cmsuserManageLi = $('.cmsuser-manage');
        cmsuserManageLi.addClass('unfold').siblings().removeClass('unfold');
    
    // CMS role management
    }else if(url.indexOf('cmsrole_manage') >= 0){
        var cmsroleManageLi = $('.cmsrole-manage');
        cmsroleManageLi.addClass('unfold').siblings().removeClass('unfold');
    
    // Comment management
    }else if(url.indexOf('comments') >= 0) {
        var commentsManageLi = $('.comments-manage');
        commentsManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
});
