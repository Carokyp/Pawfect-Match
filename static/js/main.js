document.addEventListener("DOMContentLoaded", () => {
  /* ===============================
     RESET MATCHES BUTTON
     =============================== */
  const resetBtn = document.getElementById("resetMatchesBtn");
  if (resetBtn) {
    resetBtn.addEventListener("click", (e) => {
      const confirmed = confirm(
        "Are you sure you want to reset all your matches? This will clear all your likes and let you start discovering again."
      );
      if (!confirmed) {
        e.preventDefault();
      }
    });
  }

  /* ===============================
     PASSWORD TOGGLE (eye icon)
     =============================== */
  const toggleBtns = document.querySelectorAll(".toggle-password");

  toggleBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const input = btn.parentElement.querySelector("input");
      if (!input) return;

      input.type = input.type === "password" ? "text" : "password";
    });
  });


  const toggleButtons = document.querySelectorAll(".toggle-btn");
  const dogView = document.querySelector(".dog-view");
  const ownerView = document.querySelector(".owner-view");

  if (dogView && ownerView) {
    toggleButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        // Reset buttons
        toggleButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        // Switch views
        if (btn.dataset.view === "dog") {
          dogView.classList.remove("hidden");
          ownerView.classList.add("hidden");
        } else {
          ownerView.classList.remove("hidden");
          dogView.classList.add("hidden");
        }
      });
    });
  }


  /* ===============================
     IMAGE UPLOAD PREVIEW
     (Owner + Dog)
     =============================== */
  const fileInputs = document.querySelectorAll(".upload-box input[type='file']");
  console.log('Found file inputs:', fileInputs.length);

  fileInputs.forEach((input) => {
    console.log('Setting up listener for input:', input);
    
    input.addEventListener("change", (e) => {
      console.log('File input changed!', e.target.files);
      const file = input.files[0];
      if (!file) {
        console.log('No file selected');
        return;
      }

      console.log('File selected:', file.name, file.type);
      
      const uploadBox = input.closest(".upload-box");
      console.log('Upload box:', uploadBox);
      
      const preview = uploadBox.querySelector(".image-preview");
      const placeholder = uploadBox.querySelector(".upload-placeholder");
      console.log('Preview element:', preview);
      console.log('Placeholder element:', placeholder);

      if (!preview || !placeholder) {
        console.log('Missing preview or placeholder!');
        return;
      }

      const reader = new FileReader();
      reader.onload = () => {
        console.log('File loaded, setting preview src');
        preview.src = reader.result;
        uploadBox.classList.add("has-image");
        preview.style.display = "block";
        placeholder.style.display = "none";
        console.log('Preview should now be visible');
      };

      reader.readAsDataURL(file);
    });
  });

  // Optional: enable basic drag-and-drop onto the upload box
  const uploadBoxes = document.querySelectorAll(".upload-box");
  uploadBoxes.forEach((box) => {
    const input = box.querySelector("input[type='file']");
    const preview = box.querySelector(".image-preview");
    const placeholder = box.querySelector(".upload-placeholder");
    const removeBtn = box.querySelector(".upload-remove");
    if (!input) return;

    const resetImage = () => {
      if (preview) {
        preview.src = "";
        preview.style.display = "none";
      }
      if (placeholder) {
        placeholder.style.display = "block";
      }
      box.classList.remove("has-image");
      input.value = ""; // Clear file selection
    };

    box.addEventListener("dragover", (e) => {
      e.preventDefault();
      box.style.borderColor = "#ffb6c1";
      box.style.background = "rgba(255,182,193,0.2)";
    });

    box.addEventListener("dragleave", () => {
      box.style.borderColor = "#ccc";
      box.style.background = "transparent";
    });

    box.addEventListener("drop", (e) => {
      e.preventDefault();
      box.style.borderColor = "#ccc";
      box.style.background = "transparent";
      const files = e.dataTransfer.files;
      if (files && files[0]) {
        input.files = files;
        input.dispatchEvent(new Event("change"));
      }
    });

    if (removeBtn) {
      removeBtn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        resetImage();
      });
    }
  });


  /* ===============================
     CHARACTER COUNTER (About me)
     =============================== */
  const textareas = document.querySelectorAll("textarea[maxlength]");

  textareas.forEach((textarea) => {
    const counter = textarea.parentElement.querySelector(".char-counter");
    if (!counter) return;

    const maxLength = textarea.getAttribute("maxlength");

    const updateCounter = () => {
      counter.textContent = `${textarea.value.length} / ${maxLength}`;
    };

    textarea.addEventListener("input", updateCounter);
    updateCounter();
  });

  const modal = document.getElementById("matchModal");
  const closeBtn = document.getElementById("closeMatchModal");


  /* ===============================
     MODAL POP UP
     =============================== */

  if (modal) {
    // Block body scroll when modal is open
    const checkAndBlockScroll = () => {
      if (modal.classList.contains("is-open")) {
        document.body.classList.add("modal-open");
      }
    };
    checkAndBlockScroll();

    const close = () => {
      modal.classList.remove("is-open");
      document.body.classList.remove("modal-open"); // Unblock scroll
    };

    // Close only with X button (not by clicking outside)
    if (closeBtn) {
      closeBtn.addEventListener("click", close);
    }
  }

});


