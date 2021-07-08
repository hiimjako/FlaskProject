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
  const dropZoneFolder = ".folder-card";
  const viewDropZone = "#page-drive .row";
  var selectedItem = null;

  $(".file-card .card > a").on("drag", (event) => {
    event.preventDefault();
    event.stopPropagation();
    selectedItem = $(event.target).closest("[data-id]").attr("data-id");
  });

  $(viewDropZone).on("drop dragover", (e) => {
    e.preventDefault();
    e.stopPropagation();
    let card = $(dropZoneFolder);
    // FIXME: non so se è il modo migliore, ma funziona
    const isNewFile = [...e.originalEvent.dataTransfer.items].every(x => x?.kind === "file")
    card.each((cardIndex, el) => {
      if (card.get(cardIndex).contains(e.target) && !isNewFile) {
        $(dropZoneFolder+".border.border-primary").removeClass("border border-primary")
        card.eq(cardIndex).addClass("border border-primary")
        return false;
      }
    })

    // if ($(e.target).hasClass("file-row") || $(e.target).hasClass("file-card")) {
    if (isNewFile) {
      $("#dropLayout").css("visibility", "visible");
    }
    // }
  });

  $("#page-drive").on("drop", (event) => {
    event.preventDefault();
    event.stopPropagation();
  });

  $(dropZoneElement).on("dragover", (event) => {
    // necessario per far si che non mi
    // apra il file in un altra tab
    event.preventDefault();
    event.stopPropagation();
  });

  ["dragleave", "dragend"].forEach((type) => {
    $(dropZoneElement).on(type, (event) => {
      event.preventDefault();
      event.stopPropagation();
      $("#dropLayout").css("visibility", "hidden");
    });

    $(dropZoneFolder).on(type, (e) => {
      e.preventDefault();
      e.stopPropagation();
      let card = $(e.target);
      if (card.hasClass("folder-card")) {
        card.removeClass("border border-primary")
      }
    });
  });

  $(dropZoneElement).on("drop", function (event) {
    event.preventDefault();
    event.stopPropagation();
    if (event.originalEvent.dataTransfer.files.length > 0) {
      loadFile(event.originalEvent.dataTransfer.files);
    }
    $("#dropLayout").css("visibility", "hidden");
  });

  $(dropZoneFolder).on("drop", function (event) {
    event.preventDefault();
    event.stopPropagation();
    let folderCard = $(event.target).closest(".folder-card").eq(0);
    folderCard.removeClass("border border-primary")
    let folder = folderCard.attr("data-folder");
    if (folder && selectedItem !== null) {
      let csrf_token = $("#csrf_token").val();
      let request = $.ajax({
        headers: {
          "x-csrf-token": csrf_token,
        },
        url: `/drive/file/${selectedItem}/folder?api=1`,
        data: {
          folder: folder
        },
        method: "POST",
      }).done(function (res) {
        location.reload()
      });
    }
    selectedItem = null;
  }
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
