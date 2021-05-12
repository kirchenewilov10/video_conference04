$(document).ready(function () {
    var table = $('#table').DataTable({
        dom: '<"top"Rlf<"clear">>rt<"bottom"ipB<"clear">>',
        lengthMenu: [[10, 20, 50, -1], [10, 20, 50, "All"]],
        pageLength: 10,
        columnDefs: [{
            orderable: false,
            className: 'select-checkbox',
            width: "1%",
            targets: 0
        }],
        select: {
            style: 'os',
            selector: 'td:first-child'
        },
        select: true,
        order: [
            [1, 'asc']
        ],
        buttons: [
            {
                extend: 'pdfHtml5',
                orientation: 'landscape',
                pageSize: 'LEGAL'
            },
            {
                extend: 'csv'
            },
            {
                extend: 'print'
            }
        ]
    });

    $(".buttons-copy").css("display", "None");
    $(".buttons-excel").css("display", "None");
    $(".buttons-csv").css("display", "None");
    $(".buttons-pdf").css("display", "None");
    $(".buttons-print").css("display", "None");
});

function on_edit_privilege(id, name) {


}

function on_delete_privilege(id, name) {

    if (!confirm("Confirm delete?"))
        return;


}