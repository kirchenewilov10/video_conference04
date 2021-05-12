function on_click_print_method(id) {
    $("#Print_Way_Modal").addClass("in");
    $("#Print_Way_Modal").css("display", "block");
    $("#waiting").addClass("modal-backdrop fade in");
    $("#p_labelsetupid").val(id);
}

function on_close_printway_modal() {
    $("#Print_Way_Modal").removeClass("in");
    $("#Print_Way_Modal").css("display", "none");
    $("#waiting").removeClass("modal-backdrop fade in");
}

function on_click_document_options(id,documenttype) {
    if (documenttype == 'Labels, Return Labels'){
        $("#label_Option_Modal").css("display", "block");
        $("#label_Option_Modal").addClass("in");
        $("#waiting").addClass("modal-backdrop fade in");
        init_label_option_modal(id);
        $("#d_labelsetupid").val(id);
    }
    if (documenttype == 'Packing Slips'){
        $("#Packingslip_Option_Modal").css("display", "block");
        $("#Packingslip_Option_Modal").addClass("in");
        $("#waiting").addClass("modal-backdrop fade in");
        $('#ps_setupid').val(id);
        init_packingslip_option_modal(id);
    }
    if (documenttype == 'Order Summary'){
        $("#Ordersummary_Option_Modal").css("display", "block");
        $("#Ordersummary_Option_Modal").addClass("in");
        $("#waiting").addClass("modal-backdrop fade in");
        $('#os_labelsetupid').val(id);
        init_ordersummary_option_modal(id);

    }
    if (documenttype == 'Pick List'){
        $("#Picklist_Option_Modal").css("display", "block");
        $("#Picklist_Option_Modal").addClass("in");
        $("#waiting").addClass("modal-backdrop fade in");
        $('#pl_labelsetupid').val(id);
        init_picklist_option_modal(id);
    }
}

function on_close_documentoption_modal() {
    $("#label_Option_Modal").removeClass("in");
    $("#label_Option_Modal").css("display", "none");
    $("#waiting").removeClass("modal-backdrop fade in");
}
function on_click_save_label_setup() {
    var id = $('#d_labelsetupid').val();
    var selected_labelformat = $("input[name='labelformat']:checked").val();
    var msg1key = $('#msg1field').val();
    var msg2key = $('#msg2field').val();
    var msg3key = $('#msg3field').val();
    var document_format = { "slf" : selected_labelformat, "lm" : {"msg1": msg1key, "msg2": msg2key, "msg3": msg3key} };
    var updating_param = { "document_format" : JSON.stringify(document_format) };
    var param = { "id": id, "updating_params" : JSON.stringify(updating_param) };

    $.ajax({
        type: "POST",
        url: "/setting/update_label_setup/",
        data: param,
        async: false,
        success: function (res) {
            on_close_documentoption_modal();
            if (res == "success") {
                show_message("success", "/setting/update_label_setup/", "Update label setup succeeded.");
                $(".page-content").load("/setting/label_setup_view/");
            } else {
                show_message("error", "/setting/update_label_setup/", "Update label setup failed.");
            }
        }
    });

}
function on_click_set_printway(print_to){
    var id = $("#p_labelsetupid").val();
    var updating_param = { "print_to" : print_to };
    var param = { "id": id, "updating_params" : JSON.stringify(updating_param) };

    console.log(param);
    $.ajax({
        type: "POST",
        url: "/setting/update_label_setup/",
        data: param,
        async: false,
        success: function (res) {
            on_close_printway_modal();
            if (res == "success") {
                show_message("success", "/setting/update_label_setup/", "Update print to succeeded.");
                $(".page-content").load("/setting/label_setup_view/");
            } else {
                show_message("error", "/setting/update_label_setup/", "Update print to failed.");
            }
        }
    });

}

function on_select_labelformat(id) {
    if (id == 1) {
        $('.labelformatpng46').css('display','');
        $('.labelformatpng46w').css('display','None');
    }
    if (id == 2) {
        $('.labelformatpng46').css('display','None');
        $('.labelformatpng46w').css('display','');
    }
}

function init_label_option_modal(id) {
    var params = {"id": id};
    $.ajax({
        type:"POST",
        url:"/setting/get_label_option_info",
        data: params,
        async:false,
        success:function (res) {
            if (res == "fail") { return; } ;
            var result = JSON.parse(res);
            if (result['document_format'].hasOwnProperty("slf")){
                if (parseInt(result['document_format']['slf'])== 1) {
                    document.getElementById('labelforamt46').checked = true;
                    $('.labelformatpng46').css('display','');
                    $('.labelformatpng46w').css('display','None');
                }
                else if (parseInt(result['document_format']['slf']) == 2) {
                    document.getElementById('labelformatw46').checked = true;
                    $('.labelformatpng46').css('display','None');
                    $('.labelformatpng46w').css('display','');
                }
            }
            if (result['document_format'].hasOwnProperty("lm")){
                var msgkeyarray = result['document_format']['lm'];
                if(msgkeyarray.hasOwnProperty("msg1")){
                    $('#msg1field').val(msgkeyarray['msg1']);
                }
                if(msgkeyarray.hasOwnProperty("msg2")){
                    $('#msg2field').val(msgkeyarray['msg2']);
                }
                if(msgkeyarray.hasOwnProperty("msg3")){
                    $('#msg3field').val(msgkeyarray['msg3']);
                }
            }
        }
    });
}
function init_packingslip_option_modal(id) {
    var params = {"id": id};
    $.ajax({
        type:"POST",
        url:"/setting/get_label_option_info",
        data: params,
        async:false,
        success:function (res) {
            if (res == "fail") { return; } ;
            var result = JSON.parse(res);
            if (result['document_format'].hasOwnProperty("slf")){
                $('#ps_format').val(result['document_format']['slf']);
            }
            if (result['document_format'].hasOwnProperty('ps')){
                $('#ps_sortby').val(result['document_format']['ps']['sortby']);
                if (result['document_format']['ps']['prices_is'] == true){
                    document.getElementById('ps_prices_is').checked = true;
                }
                else{
                    document.getElementById('ps_prices_is').checked = false;
                }
                if (result['document_format']['ps']['skus_is'] == true){
                    document.getElementById('ps_skus_is').checked = true;
                }
                else{
                    document.getElementById('ps_skus_is').checked = false;
                }
                if (result['document_format']['ps']['barcode_is'] == true){
                    document.getElementById('ps_barcode_is').checked = true;
                }
                else{
                    document.getElementById('ps_barcode_is').checked = false;
                }
            }
        }
    });

}

function init_ordersummary_option_modal(id) {
    var params = {"id": id};
    $.ajax({
        type:"POST",
        url:"/setting/get_label_option_info",
        data: params,
        async:false,
        success:function (res) {
            if (res == "fail") { return; } ;
            var result = JSON.parse(res);
            if (result['document_format'].hasOwnProperty("slf")){
                $('#os_format').val(result['document_format']['slf']);
            }
            if (result['document_format'].hasOwnProperty('os')){
                $('#os_sortby').val(result['document_format']['os']['sortby']);
                if (result['document_format']['os']['os_img_is'] == true){
                    document.getElementById('os_img_is').checked = true;
                }
                else{
                    document.getElementById('os_img_is').checked = false;
                }
                if (result['document_format']['os']['os_barcode_is'] == true){
                    document.getElementById('os_barcode_is').checked = true;
                }
                else{
                    document.getElementById('os_barcode_is').checked = false;
                }
            }
        }
    });
}
function init_picklist_option_modal(id) {
    var params = {"id": id};
    $.ajax({
        type:"POST",
        url:"/setting/get_label_option_info",
        data: params,
        async:false,
        success:function (res) {
            if (res == "fail") { return; } ;
            var result = JSON.parse(res);
            if (result['document_format'].hasOwnProperty("slf")){
                $('#pl_format').val(result['document_format']['slf']);
            }
            if (result['document_format'].hasOwnProperty('pl')){
                $('#pl_sortby').val(result['document_format']['pl']['sortby']);
                if (result['document_format']['pl']['pl_img_is'] == true){
                    document.getElementById('pl_img_is').checked = true;
                }
                else{
                    document.getElementById('pl_img_is').checked = false;
                }
                if (result['document_format']['pl']['pl_orderid_is'] == true){
                    document.getElementById('pl_orderid_is').checked = true;
                }
                else{
                    document.getElementById('pl_orderid_is').checked = false;
                }
                if (result['document_format']['pl']['pl_sku_is'] == true){
                    document.getElementById('pl_sku_is').checked = true;
                }
                else{
                    document.getElementById('pl_sku_is').checked = false;
                }
            }
        }
    });
}