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
    var file = this.files[0];
    loadFile(file);
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
          loadFile(event.dataTransfer.files[0]);
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

  // Context menu
  let onClickOutside = (e) => {
    e.preventDefault();
    e.stopPropagation();
    $("#context_menu").hide();
    $(document).off("click", "body", onClickOutside);
  };

  $(".card").contextmenu(function (e) {
    e.preventDefault();
    e.stopPropagation();
    const itemId = $(this).attr("data-id");
    let cardItem = $(this).find(".card-text > a").attr("href");
    let contextmenu = $("#context_menu");
    contextmenu.find("#rename").attr("href", `file/${itemId}/rename`);
    contextmenu.find("#download").attr("href", `file/${itemId}?as_attachment=True`);
    contextmenu.find("#share").attr("href", `file/${itemId}/share`);
    $(document).on("click", "body", onClickOutside);
    const x = e.pageX;
    const y = e.pageY - 15;
    contextmenu.css({
      display: "block",
      zIndex: 5000,
      left: x + "px",
      top: y + "px",
    });
  });

  // FIXME: a tag normale non funziona
  $(document).on('click', '#context_menu a', function () {
    window.location = $(this).attr("href");
  })

  $('img[data-src]').each(function (e) {
    let img = $(this);
    img.attr('src', img.attr('data-src'))
    img.removeAttr('data-src')
    img.on('error', function () {
      handleMissingImage(this)
    });
  })
});

/**
 * Uploads file with progress bar
 *
 * @param {File} file
 */
function loadFile(file) {
  if (isUploading) return;

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
  img.style = "display: none";
  $(img).siblings(".icon-placeholder").toggleClass("d-none d-flex");
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
    $("#page-drive > .container").css("height", "80vh");
    $("#dropLayout").css("visibility", "visible");
  }
}
