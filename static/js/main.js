document.addEventListener("DOMContentLoaded", () => {
  "use strict";

  /* ===============================
     CONFIRMATIONS
     =============================== */

  /**
   * Ask confirmation before resetting matches.
   * @returns {void}
   */
  const setupResetMatches = () => {
    const resetBtn = document.getElementById("resetMatchesBtn");
    if (!resetBtn) return;

    resetBtn.addEventListener("click", (event) => {
      const confirmed = confirm(
        "Are you sure you want to reset all your matches? This will clear all your likes and let you start discovering again."
      );
      if (!confirmed) {
        event.preventDefault();
      }
    });
  };

  /* ===============================
     AUTH UI
     =============================== */

  /**
   * Toggle password visibility for inputs with an eye icon.
   * @returns {void}
   */
  const setupPasswordToggle = () => {
    const toggleButtons = document.querySelectorAll(".toggle-password");
    toggleButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const input = button.parentElement.querySelector("input");
        if (!input) return;
        input.type = input.type === "password" ? "text" : "password";
      });
    });
  };

  /* ===============================
     PROFILE TOGGLE
     =============================== */

  /**
   * Switch between dog and owner views.
   * @returns {void}
   */
  const setupProfileToggle = () => {
    const toggleButtons = document.querySelectorAll(".toggle-btn");
    const dogView = document.querySelector(".dog-view");
    const ownerView = document.querySelector(".owner-view");
    if (!dogView || !ownerView || !toggleButtons.length) return;

    toggleButtons.forEach((button) => {
      button.addEventListener("click", () => {
        toggleButtons.forEach((btn) => btn.classList.remove("active"));
        button.classList.add("active");

        if (button.dataset.view === "dog") {
          dogView.classList.remove("hidden");
          ownerView.classList.add("hidden");
        } else {
          ownerView.classList.remove("hidden");
          dogView.classList.add("hidden");
        }
      });
    });
  };

  /* ===============================
     IMAGE UPLOADS
     =============================== */

  /**
   * Read a file input and display the preview.
   * @param {HTMLInputElement} input - File input element.
   * @param {HTMLElement} uploadBox - Container element.
   * @returns {void}
   */
  const handleImagePreview = (input, uploadBox) => {
    const file = input.files[0];
    if (!file) return;

    const preview = uploadBox.querySelector(".image-preview");
    const placeholder = uploadBox.querySelector(".upload-placeholder");
    if (!preview || !placeholder) return;

    const reader = new FileReader();
    reader.onload = () => {
      preview.src = reader.result;
      uploadBox.classList.add("has-image");
      preview.style.display = "block";
      placeholder.style.display = "none";
    };

    reader.readAsDataURL(file);
  };

  /**
   * Enable image previews and optional drag-and-drop uploads.
   * @returns {void}
   */
  const setupImageUploads = () => {
    const uploadBoxes = document.querySelectorAll(".upload-box");
    if (!uploadBoxes.length) return;

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
        input.value = "";
      };

      input.addEventListener("change", () => handleImagePreview(input, box));

      box.addEventListener("dragover", (event) => {
        event.preventDefault();
        box.style.borderColor = "#ffb6c1";
        box.style.background = "rgba(255,182,193,0.2)";
      });

      box.addEventListener("dragleave", () => {
        box.style.borderColor = "#ccc";
        box.style.background = "transparent";
      });

      box.addEventListener("drop", (event) => {
        event.preventDefault();
        box.style.borderColor = "#ccc";
        box.style.background = "transparent";

        const files = event.dataTransfer.files;
        if (files && files[0]) {
          input.files = files;
          input.dispatchEvent(new Event("change"));
        }
      });

      if (removeBtn) {
        removeBtn.addEventListener("click", (event) => {
          event.preventDefault();
          event.stopPropagation();
          resetImage();
        });
      }
    });
  };

  /* ===============================
     TEXT HELPERS
     =============================== */

  /**
   * Display a live character counter for textareas with maxlength.
   * @returns {void}
   */
  const setupCharacterCounters = () => {
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
  };

  /* ===============================
     MODALS
     =============================== */

  /**
   * Handle the match modal open/close and body scroll lock.
   * @returns {void}
   */
  const setupMatchModal = () => {
    const modal = document.getElementById("matchModal");
    if (!modal) return;

    const closeBtn = document.getElementById("closeMatchModal");
    const close = () => {
      modal.classList.remove("is-open");
      document.body.classList.remove("modal-open");
    };

    if (modal.classList.contains("is-open")) {
      document.body.classList.add("modal-open");
    }

    if (closeBtn) {
      closeBtn.addEventListener("click", close);
    }
  };

  /* ===============================
     FORM CACHE
     =============================== */

  /**
   * Cache form inputs in sessionStorage to preserve progress.
   * @param {string} formType - Data attribute value for the form.
   * @returns {void}
   */
  const setupFormCache = (formType) => {
    const form = document.querySelector(`form[data-form-type="${formType}"]`);
    if (!form) return;

    const inputs = form.querySelectorAll("input, textarea, select");
    const handledCheckboxGroups = new Set();
    const cacheKey = (name) => `${formType}_${name}`;

    const getCheckboxGroup = (name) =>
      Array.from(
        form.querySelectorAll(
          `input[type="checkbox"][name="${CSS.escape(name)}"]`
        )
      );

    const restoreCheckboxGroup = (name) => {
      const checkboxes = getCheckboxGroup(name);
      const savedValue = sessionStorage.getItem(cacheKey(name));
      if (!savedValue) return;

      let values = [];
      try {
        values = JSON.parse(savedValue);
      } catch (error) {
        values = [];
      }

      checkboxes.forEach((cb) => {
        cb.checked = values.includes(cb.value);
      });
    };

    const saveCheckboxGroup = (name) => {
      const checkboxes = getCheckboxGroup(name);
      const values = checkboxes.filter((cb) => cb.checked).map((cb) => cb.value);
      sessionStorage.setItem(cacheKey(name), JSON.stringify(values));
    };

    inputs.forEach((input) => {
      if (!input.name || input.type === "file") return;

      if (input.type === "checkbox") {
        if (handledCheckboxGroups.has(input.name)) return;
        handledCheckboxGroups.add(input.name);

        restoreCheckboxGroup(input.name);
        const checkboxes = getCheckboxGroup(input.name);
        checkboxes.forEach((cb) => {
          cb.addEventListener("change", () => saveCheckboxGroup(input.name));
        });
        return;
      }

      const key = cacheKey(input.name);
      const savedValue = sessionStorage.getItem(key);
      if (savedValue !== null) {
        input.value = savedValue;
      }

      const save = () => {
        sessionStorage.setItem(key, input.value);
      };

      input.addEventListener("input", save);
      input.addEventListener("change", save);
    });
  };

  /* ===============================
     PILL OPTIONS
     =============================== */

  /**
   * Enforce max selections on pill-style checkbox groups.
   * @returns {void}
   */
  const setupPillOptions = () => {
    const groups = document.querySelectorAll(".pill-options[data-max]");
    groups.forEach((group) => {
      const max = parseInt(group.dataset.max || "0", 10);
      const checkboxes = Array.from(
        group.querySelectorAll("input[type='checkbox']")
      );
      if (!checkboxes.length || !max) return;

      const helper = group.parentElement.querySelector(".pill-helper");
      const update = () => {
        const selected = checkboxes.filter((cb) => cb.checked);
        const limitReached = selected.length >= max;

        checkboxes.forEach((cb) => {
          cb.disabled = limitReached && !cb.checked;
          cb.parentElement.classList.toggle("is-disabled", cb.disabled);
        });

        if (helper) {
          helper.textContent = `Select up to ${max} (${selected.length}/${max})`;
        }
      };

      checkboxes.forEach((cb) => cb.addEventListener("change", update));
      update();
    });
  };

  /* ===============================
     INIT
     =============================== */

  /**
   * Initialize all UI behaviors when the DOM is ready.
   * @returns {void}
   */
  const init = () => {
    setupResetMatches();
    setupPasswordToggle();
    setupProfileToggle();
    setupImageUploads();
    setupCharacterCounters();
    setupMatchModal();
    setupFormCache("owner");
    setupFormCache("dog");
    setupPillOptions();
  };

  init();
});


