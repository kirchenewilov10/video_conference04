function updateProfile() {
    var username = $('#mp_fullname');
    var email = $('#mp_email');
    if (validate_field(username) == false) {
        show_message("warning", "account/update_profile", "blank field is not allowed.");
        username.focus();
        return;
    }
    if (validate_field(email) == false) {
        show_message("warning", "account/update_profile", "blank field is not allowed.");
        email.focus()
        return;
    }
    var param = {'username': username.val(), 'email': email.val()};
    $.ajax({
        type: "POST",
        url: "/account/update_profile/",
        data: param,
        success: function (res) {
            if (res == "success") {
                show_message("success", "account/update_profile", "update user profile suceeded.");
                $(".page-content").load("/account/my_profile_view/");
                $("#username").text(username.val());

            } else {
                show_message("error", "account/update_profile", "update user profile failed.");
            }
        }
    });
}

function initPwdInput() {
    $('#mp_now_password').val("");
    $('#mp_new_password').val("");
    $('#mp_new_password_confirm').val("");
}

function updatePwd() {
    var curpwd = $('#mp_now_password').val();
    var newpwd = $('#mp_new_password').val();
    var confirmpwd = $('#mp_new_password_confirm').val();
    if (newpwd != confirmpwd) {
        show_message("warning", "account/updatePwd", "Verify password failed.");
        initPwdInput()
        return;
    }
    if (newpwd.length < 7) {
        show_message("warning", "account/updatePwd", "Password minimum length must be 7.");
        initPwdInput();
        return;
    }
    var param = {'curpwd': curpwd, 'newpwd': newpwd};
    $.ajax({
        type: "POST",
        url: "/account/update_password/",
        data: param,
        success: function (res) {
            if (res == "success") {
                show_message("success", "account/updatePwd", "Updating password suceeded.");
                $(".page-content").load("/account/updat_password/");
                initPwdInput();
            } else if (res == "nonCurpwdCorrect") {
                initPwdInput();
                show_message("warning", "account/updatePwd", "Current password is not correct.");
            } else if (res == "fail") {
                initPwdInput();
                show_message("error", "account/updatePwd", "Updating password failed.");
            }
        }
    });

}

