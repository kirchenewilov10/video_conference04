(function ($) {
    "use strict";


    var $image = $(".image-crop > img");
    $($image).cropper({
        aspectRatio: 1.0,
        preview: ".img-preview",
        done: function (data) {
            // Output the result data for cropping image.
        }
    });

    var $inputImage = $("#inputImage");
    if (window.FileReader) {
        alert("a");
        $inputImage.change(function () {
            alert(this.files);
            var fileReader = new FileReader(),
                files = this.files,
                file;
            alert("c");
            if (!files.length) {
                return;
            }

            file = files[0];

            if (/^image\/\w+$/.test(file.type)) {
                fileReader.readAsDataURL(file);
                fileReader.onload = function () {
                    $inputImage.val("");
                    $image.cropper("reset", true).cropper("replace", this.result);
                };
            }
        });
    } else {
        $inputImage.addClass("hide");
    }

    $("#download").on('click', function () {
        window.open($image.cropper("getDataURL"));
    });

    $("#zoomIn").on('click', function () {
        $image.cropper("zoom", 0.1);
    });

    $("#zoomOut").on('click', function () {
        $image.cropper("zoom", -0.1);
    });

    $("#rotateLeft").on('click', function () {
        $image.cropper("rotate", 90);
    });

    $("#rotateRight").on('click', function () {
        $image.cropper("rotate", -90);
    });

    $("#setDrag").on('click', function () {
        $image.cropper("setDragMode", "crop");
    });

})(jQuery); 