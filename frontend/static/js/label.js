$(document).ready(function () {

    var label_table = $('#table').DataTable({
        dom: '<"top"R<"clear">>rt<"bottom"lip<"clear">>',
        lengthMenu: [[15, 30, 50, -1], [15, 30, 50, "All"]],
        pageLength: 15,
        columnDefs: [{
            orderable: false,
            className: 'select-checkbox',
            width: "1%",
            targets: 0
        },
        {
            width: "1%",
            targets: 1
        }],
        select: {
            style: 'os',
            selector: 'td:first-child'
        },
        order: [
            [1, 'asc']
        ]
    });

    $('#table tbody').on('click', 'td.select-checkbox', function () {

        setTimeout(function () {
            if (label_table.rows({selected: true}).count() === 0) {
                $("thead tr").removeClass("selected");
            } else {
                $("thead tr").addClass("selected");
            }
        }, 100);
    });

    $('#table thead').on("click", "th.select-checkbox", function () {
        if ($("tr").hasClass("selected")) {
            label_table.rows().deselect();
            $("tr").removeClass("selected");
        } else {
            label_table.rows().select();
            $("tr").addClass("selected");
        }
    }).on("select deselect", function () {
        if (label_table.rows({selected: true}).count() !== label_table.rows().count()) {
            $("tr").removeClass("selected");
        } else {
            $("tr").addClass("selected");
        }
    });
});

function on_add_rule() {

    $(".page-content").load("/setting/type_presets_view", function() {
		$("#Label_Modal").addClass("in");
		$("#Label_Modal").css("display", "block");
		$("#waiting").addClass("modal-backdrop fade in");
	});
}

function on_edit_rule(id, sku, tp_service, tp_package, tp_warehouse, status) {

	$(".page-content").load("/setting/type_presets_view",
	{
		selectedservice: tp_service,
        selectedpackage: tp_package,
        selectedwarehouse: tp_warehouse,
		status: status
	}, function() {
		$("#Label_Modal").addClass("in");
		$("#Label_Modal").css("display", "block");
		$("#waiting").addClass("modal-backdrop fade in");

		$("#tp_dlg_id").val(id);
		$("#tp_dlg_sku").val(sku);
	});
}

function on_delete_rule(id) {

    if (!confirm("Confirm delete?"))
        return;

    var params = {
        "id": id,
    };

    $.ajax({
        type: "POST",
        url: "/setting/delete_rule/",
        data: params,
        success: function (res) {

            $(".page-content").load("/setting/type_presets_view");
        }
    });
}

function on_modal_add() {

    var tp_sku = $("#tp_dlg_sku").val();
    var tp_service = $("#tp_dlg_service").val();
    var tp_package = $("#tp_dlg_package").val();
    var tp_warehouse = $("#tp_dlg_warehouse").val();
    var status = $("#tp_dlg_status").val();

    if (tp_sku === "") {
        show_message("warning", "Add Rule", "Please Input sku.");
        $("#tp_dlg_sku").focus();
        return;
    }

    if (tp_service === "-1") {
        show_message("warning", "Add Rule", "Please choose a service.");
        $("#tp_dlg_service").focus();
        return;
    }

    if (tp_package === "-1") {
        show_message("warning", "Add Rule", "Please choose a package.");
        $("#tp_dlg_package").focus();
        return;
    }

    if (tp_warehouse === "-1") {
        show_message("warning", "Add Rule", "Please choose a warehouse.");
        $("#tp_dlg_warehouse").focus();
        return;
    }

    on_modal_close();

    var params = {
        "sku": tp_sku,
        "service": tp_service,
        "package": tp_package,
        "warehouse": tp_warehouse,
        "status": status
    };

    $.ajax({
        type: "POST",
        url: "/setting/add_rule/",
        data: params,
        success: function (res) {

            $(".page-content").load("/setting/type_presets_view");
        }
    });
}

function on_modal_save() {

	var id = $("#tp_dlg_id").val();
	var tp_sku = $("#tp_dlg_sku").val();
    var tp_service = $("#tp_dlg_service").val();
    var tp_package = $("#tp_dlg_package").val();
    var tp_warehouse = $("#tp_dlg_warehouse").val();
    var status = $("#tp_dlg_status").val();

    if (tp_sku === "") {
        show_message("warning", "Edit Rule", "Please Input sku.");
        $("#tp_dlg_sku").focus();
        return;
    }

    if (tp_service === "-1") {
        show_message("warning", "Edit Rule", "Please choose a service.");
        $("#tp_dlg_service").focus();
        return;
    }

    if (tp_package === "-1") {
        show_message("warning", "Edit Rule", "Please choose a package.");
        $("#tp_dlg_package").focus();
        return;
    }

    if (tp_warehouse === "-1") {
        show_message("warning", "Edit Rule", "Please choose a warehouse.");
        $("#tp_dlg_package").focus();
        return;
    }

    on_modal_close();

    var params = {
		"id": id,
        "sku": tp_sku,
        "service": tp_service,
        "package": tp_package,
        "warehouse": tp_warehouse,
        "status": status
    };

    $.ajax({
        type: "POST",
        url: "/setting/update_rule/",
        data: params,
        success: function (res) {

            $(".page-content").load("/setting/type_presets_view");
        }
    });
}

function on_modal_close() {

	$("#Label_Modal").removeClass("in");
	$("#Label_Modal").css("display", "None");
	$("#waiting").removeClass("modal-backdrop fade in");
}