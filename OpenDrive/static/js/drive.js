var isUploading = false;

$(document).ready(function () {
  // <!-- {# include "drive/drive.js" | safe #} -->

  if ($(".card").length <= 0) {
    showDropLayout();
  }

  $(".upload-button").click(function () {
    $("form input[type='file']").trigger("click");
  });

  $("form input[type='file']").change(function () {
    loadFile(this.files);
  });

  $(document).on("keyup", "#nav-filter", function () {
    let search = $(this).val().toLocaleLowerCase();
    $(".searchable-card").filter(function () {
      $(this).toggle($(this).text().toLocaleLowerCase().indexOf(search) > -1);
    });
  });

  $(".closing-button").click(function () {
    let id = $(this).attr("data-id");
    var card = $(this);
    let csrf_token = $("#csrf_token").val();
    if (!isNaN(id)) {
      let request = $.ajax({
        headers: {
          "x-csrf-token": csrf_token,
        },
        url: `/drive/file/${id}`,
        method: "DELETE",
      }).done(function (res) {
        if (res.status === true) {
          card.closest(".card").closest(".col").remove();
          showDropLayout();
        }
      });
    }
  });

  const dropZoneElement = "#dropLayout";
  const viewDropZone = "#page-drive .container";
  $(viewDropZone).on("drop dragover", (e) => {
    e.preventDefault();
    e.stopPropagation();
    $("#dropLayout").css("visibility", "visible");
  });

  $("#page-drive").on("drop", (e) => {
    e.preventDefault();
  });

  $(dropZoneElement).on("dragover", (e) => {
    // necessario per far si che non mi
    // apra il file in un altra tab
    e.preventDefault();
  });

  ["dragleave", "dragend"].forEach((type) => {
    $(dropZoneElement).on(type, (e) => {
      $("#dropLayout").css("visibility", "hidden");
    });
  });

  document.addEventListener(
    "drop",
    function (event) {
      event.preventDefault();
      if (event.target.id === dropZoneElement.replace("#", "")) {
        if (event.dataTransfer.files.length > 0) {
          loadFile(event.dataTransfer.files);
        }
        $("#dropLayout").css("visibility", "hidden");
      }
    },
    false
  );

  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  $('img[data-src]').each(function (e) {
    let img = $(this);
    img
      .attr('src', img.attr('data-src'))
      .removeAttr('data-src')
      .on("load", function () {
        onImageLoad(this)
      })
      .on('error', function () {
        handleMissingImage(this)
      });
  })
});

/**
 * Uploads file with progress bar
 *
 * @param {Array<File>} files
 */
function loadFile(files) {
  if (isUploading) return;

  var ajaxData = new FormData();
  [...files].forEach(file => {
    ajaxData.append($("form input[type='file']").attr("name"), file);
  });

  $.ajax({
    headers: {
      "x-csrf-token": $("#csrf_token").val()
    },
    url: $("form").attr("action"),
    type: $("form").attr("method"),
    method: "POST",
    data: ajaxData,
    dataType: "json",
    cache: false,
    contentType: false,
    processData: false,
    beforeSend: function (xhr) {
      isUploading = true;
    },
    xhr: function () {
      var xhr = new window.XMLHttpRequest();
      xhr.upload.addEventListener("progress", function (progress) {
        if (progress.lengthComputable) {
          var percentage = Math.floor((progress.loaded / progress.total) * 100);

          $("#progressBar").show();
          $("#progressBar .progress-bar")
            .css("width", percentage + "%")
            .attr("aria-valuenow", percentage)
            .text(percentage + "%");
        }
      });

      return xhr;
    },
  }).done(function (res) {
    if (res.status === true) {
      // TODO: mettere un flash tipo
      $("#progressBar").hide();
      $("#progressBar .progress-bar")
        .css("width", "0%")
        .attr("aria-valuenow", 0)
        .text("0%");

      isUploading = false;
      location.reload();
    }
  });
}

/**
 * Change missing image to a default
 *
 * @param {HTMLImageElement} img
 */
function handleMissingImage(img) {
  img.onerror = null;
  $(img)
    .removeClass("d-flex")
    .addClass("d-none");
  $(img).siblings(".icon-placeholder")
    .removeClass("d-none")
    .addClass("d-flex");
  $(img).siblings(".spinner-placeholder")
    .removeClass("d-flex")
    .addClass("d-none");
}

/**
 * When the image loads it hide the spinner and shows the image
 *
 * @param {HTMLImageElement} img
 */
function onImageLoad(img) {
  $(img)
    .removeClass("d-none")
    .addClass("d-flex")
    .animate({ opacity: 1 });

  $(img).siblings(".spinner-placeholder")
    .removeClass("d-flex")
    .addClass("d-none");
}

/**
 * Show drop layout
 */
function showDropLayout() {
  if (
    !/Android|webOS|iPhone|iPad|Mac|Macintosh|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
      navigator.userAgent
    ) &&
    $(".card").length <= 0
  ) {
    $("#dropLayout").css("visibility", "visible");
  }
}
