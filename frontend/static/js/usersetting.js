function on_edit_user(id, username, firstname, lastname, email, v_account, status, permission, password) {
    $('#user_Modal_Edit').addClass("in");
    $("#user_Modal_Edit").css("display", "block");
    $("#waiting").addClass("modal-backdrop fade in");


    $('.edituserbtn').attr('onclick', 'edit_user(' + id + ',"' + username + '","' + password + '","' + email + '");');
    $('#v_account_adjust').attr('onkeyup', 'on_keyup_accountadjust(' + v_account + ');');
    $('#g_username').val(username);
    $('#g_password').val(password);
    $('#firstname').val(firstname);
    $('#lastname').val(lastname);
    $('#g_email').val(email);
    $('#v_account').val(v_account);
    $('#v_account_adjust').val('');
    $('#deposit_notes').val('');

    if (status === 1) {
        document.getElementById("status").checked = true;
    } else {
        document.getElementById("status").checked = false;
    }

    var cl_permission = $('#user_Modal_Edit .cl_permission');
    permission = permission.split("");
    for (var i = 0; i < permission.length; i++) {
        var p_index = parseInt(permission[i]);
        if (p_index == 1) {
            cl_permission[i].checked = true;
        } else {
            cl_permission[i].checked = false;
        }
    }
    $('#all_pm_set')[0].checked = false;
}

function all_set_user_pm() {
    var cl_permission = $('#user_Modal_Edit .cl_permission');
    var all_pm_set = $('#all_pm_set')[0];

    for (var i = 0; i < cl_permission.length; i++) {
        if (all_pm_set.checked === true) {
            if (cl_permission[i].checked === false) {
                cl_permission[i].click();
            }
        } else {
            if (cl_permission[i].checked === true) {
                cl_permission[i].click();
            }
        }
    }

}

function on_delete_user(id, username) {

    if (!confirm("Confirm delete?"))
        return;

    var params = {
        "id": id,
        "username": username,
    };

    $.ajax({
        type: "POST",
        url: "/api/v2/delete_user",
        data: params,
        success: function (res) {
            if (res === "success") {

                alert("Deleted successfully.");
                $(".page-content").load("/api/v2/users_view");

            } else {

                alert("Error.");

            }
        }
    });
}

function on_keyup_accountadjust(current_money) {
    var account_adjsut_str = $('#v_account_adjust').val();
    var account_adjsut = parseFloat(account_adjsut_str);
    if (isNaN(account_adjsut)) {
        if (account_adjsut_str !== '' && account_adjsut_str !== '-') {
            show_message("warning", "Admin/User", "Input should be number type.");
            $('#v_account_adjust').val('');
            return;
        } else {
            account_adjsut = 0;
        }
    }
    current_money = parseFloat(current_money);
    if (isNaN(current_money)) {
        show_message("warning", "Admin/User", "Current money is not number type.");
        return;
    }
    var total_money = current_money + account_adjsut;
    var total_money_fixed = total_money.toFixed(2);
    $('#v_account').val(total_money_fixed);
}

function on_keyup_rebate_rate() {
    var rebate_rate_str = $('#g_rebate_rate').val();
    var rebate_rate = parseFloat(rebate_rate_str);
    if (isNaN(rebate_rate) && rebate_rate_str !== '') {
        show_message("warning", "Admin/User", "Rebate rate should be number type.");
        $('#g_rebate_rate').val('');
        return;
    }
    if (rebate_rate > 1 || rebate_rate < 0) {
        show_message("warning", "Admin/User", "Rebate rate should be between 0 and 1.");
        $('#g_rebate_rate').val('');
        return;
    }
}

function edit_user(id, priorusername, origin_password, prioremail) {

    var username = $("#g_username").val();
    var password = $("#g_password").val();
    var firstname = $("#firstname").val();
    var lastname = $("#lastname").val();
    var email = $("#g_email").val();
    var checked = document.getElementById("status").checked;
    var status = -1;
    if (checked === true) {
        status = 1;
    } else {
        status = 0;
    }

    var total_money = $('#v_account').val();
    if (total_money === ""){
        total_money = 0;
    }
    else {
        total_money = parseFloat(total_money);
    }

    var cl_permission = $('#user_Modal_Edit .cl_permission');
    var cl_permission_str = '';
    for (var i = 0; i < cl_permission.length; i++) {
        var checkvalue = 0;
        if (cl_permission[i].checked === true) {
            checkvalue = 1;
        }
        cl_permission_str += checkvalue.toString();
    }

    var password_update = 'true';
    if (password === origin_password && password !== ""){
        password_update = 'false';
    }

    var username_update = 'true';
    if (priorusername === username && priorusername !== "") {
        username_update = 'false';
    }

    var email_update = 'true';
    if (prioremail === email && prioremail !== "") {
        email_update = 'false';
    }

    var url = "/api/v2/update_user";
    if (id === 0){
        url = "/api/v2/add_user";
    }
    var params = {
        "id": id,
        "username": username,
        "password": password,
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "status": status,
        "total_money": total_money,
        "deposit_money": $('#v_account_adjust').val(),
        "deposit_notes": $('#deposit_notes').val(),
        "permission": cl_permission_str,
        'password_update': password_update,
        'username_update': username_update,
        'email_update': email_update
    };

    $.ajax({
        type: "POST",
        url: url,
        data: params,
        success: function (res) {
            if (res === "success") {
                on_close_edit_user_modal();
                if (id === 0)
                    show_message("success", "Admin/User", "User Added Successfully.");
                else
                    show_message("success", "Admin/User", "User Updated Successfully.");

                $(".page-content").css("opacity", "0.3");
                $(".loading-content").css("display", "block");

                $(".page-content").load("/api/v2/users_view", function () {
                    $(".page-content").css("opacity", "1");
                    $(".loading-content").css("display", "None");
                });
            } else if (res === "fail") {
                if (id === 0)
                    show_message("error", "Admin/User", "Adding user failed.");
                else
                    show_message("error", "Admin/User", "Updating user failed.");

            } else if (res === "existedname") {
                show_message("error", "Admin/User", "name already existed.");

            } else if (res === "existedemail") {
                show_message("error", "Admin/User", "email already existed.");
            }
        }
    });
}

function on_close_edit_user_modal() {
    $("#user_Modal_Edit").removeClass("in");
    $("#user_Modal_Edit").css("display", "None");
    $("#waiting").removeClass("modal-backdrop fade in");
}

function on_discard_user() {
    $(".page-content").load("/api/v2/users_view");
}

function on_click_user(userid, back = false) {
    var param = {'userid': userid};
    var url = '/api/v2/user_detail_view';
    $(".page-content").css("display", "None");
    $(".loading-content").css("display", "block");

    if (!back) {
        var page = {'menu_type': 'user_link_from_nm', 'id': userid};
        history.pushState(page, '');
    }

    $('.page-content').load(url, param, function () {
        $(".page-content").css("display", "block");
        $(".loading-content").css("display", "None");

    });
}

function onclick_export_usersinfo() {
    $("#available_fields_ul").selectable({filter: "li", cancel: ".ui-selected"}).sortable();
    $("#exporting_fields_ul").selectable({filter: "li", cancel: ".ui-selected"}).sortable();
    $("#ed_available_fields_ul").selectable({filter: "li", cancel: ".ui-selected"}).sortable();
    $("#ed_exporting_fields_ul").selectable({filter: "li", cancel: ".ui-selected"}).sortable();

    $("#Export_User_Modal").addClass("in");
    $("#Export_User_Modal").css("display", "block");
    $("#waiting").addClass("modal-backdrop fade in");
    $("#export_order_firstpage").css("display", "block");
    $("#export_order_editformat_page").css("display", "none");
    $("#export_order_createformat_page").css("display", "none");

    $("#exportbtn").css("display", "block");
    $("#cancelbtn").css("display", "block");
    $("#ftbackbtn").css("display", "none");
    $("#savfombtn").css("display", "none");
    $("#updfombtn").css("display", "none");
    $("#sebackbtn").css("display", "none");

    get_select_u2();
    var total_cn_str = $('#table_info').text();
    var total_cn = get_total_cn_from_str(total_cn_str);
    $('#p_selected_cn').text(selected_count);
    $('#p_all_cn').text(total_cn);
    if (selected_count === 0) {
        document.getElementById('all_record').checked = true;
    } else {
        document.getElementById('selected_record').checked = true;
    }

    //add select or all option here
    if ($('#export_format_ul')[0].children.length > 0) {
        var firstformatid = $('#export_format_ul')[0].children[0].id;
        document.getElementById('format_' + firstformatid).checked = true;
    }
}

function on_status_change(uid) {
    var buttonstatus = $("#switch_" + uid)[0].checked;
    var status = 0;
    if (buttonstatus == true) {
        status = 1;
    }
    var params = {"status": status, "userid": uid};
    $.ajax({
        type: "POST",
        url: "/api/v2/update_user_status",
        data: params,
        success: function (res) {
            if (res == "success") {
                show_message("success", "Admin/User", "User Updated Successfully.");
                on_discard_user();
            } else {
                show_message("error", "Admin/User", "Updating user failed.");
            }
        }
    });
}

function onclick_broadcast_email_modal() {
    get_select_u2();
    var items = selected_items;
    var usernames = selected_usernames;
    if (items.length == 0){
        show_message("error","Admin/User","There is no any users selected.");
        return;
    }
    $('#en_users_select option').remove();
    var htm = '';
    for (var i = 0; i < usernames.length;i++){
        htm += ('<option selected value="' + items[i] + '">' + usernames[i] + '</option>');
    }
    $('#en_users_select').html(htm);
    $('.select2').select2();
    $('#email_content').val('');

    $("#Broadcast_Email_Modal").addClass("in");
    $("#Broadcast_Email_Modal").css("display", "block");
    $("#waiting").addClass("modal-backdrop fade in");
}

function onclick_broadcast_email(){
    var en_users_selected = $('div[role = "en_users_form"] li[class = "select2-selection__choice"]');
    var en_users = $('#en_users_select');
    var userids = get_select2_selected_users(en_users, en_users_selected);
    var params = {
        'id' : JSON.stringify(userids),
        'text': $('#email_content').val()
    };
    $(".page-content").css("opacity", "0.3");
    $(".loading-content").css("display", "block");

    $.ajax({
        type: "POST",
        url: "/api/v2/broadcast_email",
        data: params,
        success: function (res) {
            $(".page-content").css("opacity", "1");
            $(".loading-content").css("display", "none");

            on_close_en_modal();
            if (res == "success") {
                show_message("success", "Admin/User", "Emails broadcasted successfully.");
            } else {
                show_message("error", "Admin/User", "Email broadcasting failed.");
            }
        }
    });
}
function get_select2_selected_users(en_users, en_users_selected){
    var en_userids_selected = new Array();
    var en_userids_selected_cn = 0;
    for (var i=0; i < en_users[0].children.length; i++){
        for(var j =0;j < en_users_selected.length; j++){
            if (en_users[0].children[i].text == en_users_selected[j].title){
                en_userids_selected[en_userids_selected_cn++] = en_users[0][i].value;
            }
        }
    }
    return en_userids_selected;
}
function onclick_simple_add_fund() {
    get_select_u2();
    var items = selected_items;
    if (items.length == 0){
        show_message("warning","Add Funds","Please select the user.");
        return;
    }
    if (items.length > 1){
        show_message("warning","Add Funds","You have to select only one user.");
        return;
    }
    var selected_userid = items[0];
    var params = {'selected_userid': selected_userid};
    $.ajax({
        type: "POST",
        url: "/api/v2/getuserfordeposit",
        data: params,
        success: function (res) {
            if(res === "child"){
                show_message("warning", "Add Funds", "Child account can not be updated with fund.");
            }else if (res === "fail"){
                show_message("warning", "Add Funds", "Updating user info not gotten.");
            }else{
                var result = JSON.parse(res);
                $("#Private_Fund_Modal").addClass("in");
                $("#Private_Fund_Modal").css("display", "block");
                $("#waiting").addClass("modal-backdrop fade in");

                $('.pvedituserbtn').attr('onclick', 'private_addfund(' + result.id + ');');
                $('#p_v_account_adjust').attr('onkeyup', 'on_keyup_pv_accountadjust(' + result.current_money + ');');
                $('#p_v_account').val(result.current_money);
                $('#p_v_account_adjust').val('');
                $('#p_deposit_notes').val('');
                $('#p_g_rebate_rate').val(result.rebate_rate);
            }
        }
    });
}