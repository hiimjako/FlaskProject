$(document).ready(function () {
  // <!-- {# include "drive/drive.js" | safe #} -->

  if ($(".card").length <= 0) {
    showDropLayout();
  }

  $(".upload-button").click(function () {
    $("form input[type='file']").trigger("click");
  });

  $("form input[type='file']").change(function () {
    var file = this.files[0];
    loadFile(file);
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
  const viewDropZone = "#index-drive .container";
  $(viewDropZone).on("drop dragover", (e) => {
    e.preventDefault();
    e.stopPropagation();
    $("#dropLayout").css("visibility", "visible");
  });

  $("#index-drive").on("drop", (e) => {
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
          loadFile(event.dataTransfer.files[0]);
        }
        $("#dropLayout").css("visibility", "hidden");
      }
    },
    false
  );
});

/**
 * Uploads file with progress bar
 *
 * @param {File} file
 */
function loadFile(file) {
  var reader = new FileReader();

  // reader.addEventListener("loadstart", handleEvent);
  // reader.addEventListener("load", handleEvent);
  reader.addEventListener("loadend", function () {
    let percentage = 0;

    var ajaxData = new FormData($("form").get(0));
    ajaxData.append($("form input[type='file']").attr("name"), file);

    $.ajax({
      headers: {
        "x-csrf-token": csrf_token,
      },
      url: $("form").attr("action"),
      type: $("form").attr("method"),
      method: "POST",
      data: ajaxData,
      dataType: "json",
      cache: false,
      contentType: false,
      processData: false,
    }).done(function (res) {
      if (res.status === true) {
        // TODO: mettere un flash tipo
        setTimeout(function () {
          $("#progressBar").hide();
          $("#progressBar .progress-bar")
            .css("width", percentage + "%")
            .attr("aria-valuenow", percentage)
            .text(percentage + "%");

          location.reload();
        }, 2500);
      }
    });
  });

  reader.addEventListener("progress", function (e) {
    if (e.lengthComputable) {
      var percentage = Math.round((e.loaded * 100) / e.total);
      $("#progressBar").show();
      $("#progressBar .progress-bar")
        .css("width", percentage + "%")
        .attr("aria-valuenow", percentage)
        .text(percentage + "%");
    }
  });
  // reader.addEventListener("error", handleEvent);
  // reader.addEventListener("abort", handleEvent);

  reader.readAsDataURL(file);
}

/**
 * Change missing image to a default
 *
 * @param {HTMLImageElement} img
 */
function handleMissingImage(img) {
  img.onerror = null;
  img.style = "display: none";
  $(img).siblings(".image-placeholder").toggleClass("d-none d-flex");
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
    $("#index-drive > .container").css("height", "80vh");
    $("#dropLayout").css("visibility", "visible");
  }
}
