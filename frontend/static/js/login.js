var pre_store_id = 0;
var pre_carrier_id = 0;
var pre_recipient_id = "all";
var pre_item_type_id = "all";
var pre_notes_id = "all";
var pre_tracking_id = "all";
var pre_warehouse_id = 0;
var pre_stp_status_id = "all";
var pre_type_id = "all";
var pre_user_id = "all";
var pre_status_id = "all";

function clear_filter_variable() {

    pre_store_id = 0;
    pre_carrier_id = 0;
    pre_recipient_id = "all";
    pre_item_type_id = "all";
    pre_notes_id = "all";
    pre_tracking_id = "all";
    pre_warehouse_id = 0;
    pre_stp_status_id = "all";
    pre_type_id = "all";
    pre_user_id = "all";
    pre_status_id = "all";
}

function on_click_topmenu(id, url){
    $(".treeview").removeClass("active");
    $(".active").removeClass("active");
    $("#topmenu_" + id).addClass("active");
    onclick_top_menu(id, url);
}

function on_click_submenu(topmenu_id, submenu_id, url){
    $(".active").removeClass("active");
    $("#topmenu_" + topmenu_id).addClass("active");
    $("#submenu_" + submenu_id).addClass("active");
    onclick_top_menu(topmenu_id, url);
}

function onclick_top_menu(id, url, value, subname, back = false) {
    if (url === "") {
        var pre_url = accessCookie("pre_url");
        if (pre_url !== "") {
            id = parseInt(accessCookie("pre_id"));
            url = pre_url;
            value = parseInt(accessCookie("pre_value"));
            subname = accessCookie("pre_subname");
        } else {
            url = "dashboard";
        }
    }

    createCookie("pre_id", id, 1);
    createCookie("pre_url", url, 1);
    createCookie("pre_value", value, 1);
    createCookie("pre_subname", subname, 1);

    //. $(".page-content").css("display", "None");
    $(".page-content").css("opacity", "0.3");
    $(".loading-content").css("display", "block");

    if (!back) {
        var page = {'menu_type': 'top_menu', 'id': id, 'url': url, 'value': value, 'subname': subname};
        history.pushState(page, '');
    }
    clear_filter_variable();
    $('.page-content').load(url, {
        view_mode: value
    }, function () {
        //. $(".page-content").css("display", "block");
        $(".page-content").css("opacity", "1");
        $(".loading-content").css("display", "None");
    });
}

function accessCookie(cookieName){
    var name = cookieName + "=";
    var allCookieArray = document.cookie.split(';');
    for (var i = 0; i < allCookieArray.length; i++) {
        var temp = allCookieArray[i].trim();
        if (temp.indexOf(name) == 0)
            return temp.substring(name.length, temp.length);
    }
    return "";
}

function createCookie(cookieName, cookieValue, daysToExpire) {
    var date = new Date();
    date.setTime(date.getTime() + (daysToExpire * 24 * 60 * 60 * 1000));
    document.cookie = cookieName + "=" + cookieValue + "; expires=" + date.toGMTString();
}

function on_privacy_policy() {

    window.location.href = "privacy_policy";
}

function on_terms_of_use() {

    window.location.href = "terms_of_use";
}

function on_click_menu(url){
    $("#main_content").load(url);
    selected_userid = 0;
}


function on_click_sign_out() {

    $.ajax({
        type: "POST",
        url: "logout",
        async: false,
        success: function (res) {
            window.location.href = "/";
        },
        error: function(){
          window.location.href = "/";
        }
    });
}


function show_loading() {

    var doc = document.documentElement;
    var left = (window.pageXOffset || doc.scrollLeft) - (doc.clientLeft || 0);
    var top = (window.pageYOffset || doc.scrollTop) - (doc.clientTop || 0);

    document.getElementById("loading").style.marginTop = top + "px";

    $("#loading").css("display", "block");
    $("#waiting").addClass("modal-backdrop fade in");
}

function hide_loading() {

    $("#loading").css("display", "None");
    $("#waiting").removeClass("modal-backdrop fade in");

    document.getElementById("loading").style.marginTop = "0px";
}


function update_table(table) {
    var curr_pos = {
        'top': $(table.settings()[0].nScrollBody).scrollTop(),
        'left': $(table.settings()[0].nScrollBody).scrollLeft()
    };

    table.ajax.reload(function () {
        $(table.settings()[0].nScrollBody).scrollTop(curr_pos.top);
        $(table.settings()[0].nScrollBody).scrollLeft(curr_pos.left);
    }, false);

    $('#table thead tr').removeClass("selected");
}


function back() {
    history.back();
}

function appendLeadingZeroes(n) {
    if (n <= 9) {
        return "0" + n;
    }
    return n;
}

function show_message(type, title, msg, size = "") {
    if (size === "") {
        Lobibox.notify(type, {
            delay: 4000,
            title: title,
            msg: msg
        });
    }

    if (size === "large") {
        Lobibox.notify(type, {
            size: 'large',
            title: title,
            msg: msg
        });
    }
}

function PrefixInteger(num, length) {
    return (Array(length).join('0') + num).slice(-length);
}