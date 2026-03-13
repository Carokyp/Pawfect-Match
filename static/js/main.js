document.addEventListener("DOMContentLoaded", () => {
  "use strict";

  /* ===============================
     NAVBAR AUTO-COLLAPSE
     =============================== */

  /**
   * Initializes the mobile Bootstrap navbar behaviour.
   *
   * This function:
   * - closes the navbar when a navigation link is clicked
   * - closes the navbar when the user clicks outside the drop down menu
   *
   * @returns {void}
   */
  const setupNavbarCollapse = () => {
    const navbar = document.querySelector(".navbar-collapse");
    const toggler = document.querySelector(".navbar-toggler");
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");

    // Stop execution if required elements are missing
    if (!navbar || !toggler) return;

    /**
     * Closes the mobile navbar if it is currently open.
     *
     * @returns {void}
     */
    const closeNavbar = () => {
      if (!navbar.classList.contains("show")) return;
      toggler.click();
    };

    // Close navbar when a navigation link is clicked
    navLinks.forEach((link) => {
      link.addEventListener("click", closeNavbar);
    });

    /**
     * Detects clicks outside the navbar and closes it if open.
     *
     * @param {MouseEvent} event - The click event triggered by the user.
     * @returns {void}
     */
    document.addEventListener("click", (event) => {
      const target = event.target;

      // Ensure the event target is a DOM element
      if (!(target instanceof Element)) return;

      // Close navbar if the click occurred outside the menu and toggler
      if (
        !target.closest(".navbar-collapse") &&
        !target.closest(".navbar-toggler")
      ) {
        closeNavbar();
      }
    });
  };

  /* ===============================
     AUTH UI
     =============================== */

  /**
   * Toggle password visibility for inputs with an eye icon.
   * Allows users to show/hide password text by clicking the toggle button.
   * Searches for all elements with the "toggle-password" class and attaches click handlers.
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
     IMAGE UPLOADS
     =============================== */

  /**
   * Reads the selected file from an input and displays a preview image.
   * Uses the FileReader API to convert the image file into a data URL
   * that can be displayed in the preview <img> element.
   *
   * @param {HTMLInputElement} input - The file input element containing the selected image.
   * @param {HTMLElement} uploadBox - The container element that holds the preview and placeholder.
   * @returns {void}
   */
  const handleImagePreview = (input, uploadBox) => {
    // Get the first selected file from the input
    const file = input.files[0];
    if (!file) return; // Stop if no file is selected

    // Find the preview image element and placeholder inside the upload box
    const preview = uploadBox.querySelector(".image-preview");
    const placeholder = uploadBox.querySelector(".upload-placeholder");

    // If required elements are missing, stop execution
    if (!preview || !placeholder) return;

    // Create a FileReader to read the local file
    const reader = new FileReader();

    // When the file has been read, update the preview image
    reader.onload = () => {
      preview.src = reader.result; // Set image source to the file data
      preview.style.display = "block"; // Show the preview image
      placeholder.style.display = "none"; // Hide the placeholder text
      uploadBox.classList.add("has-image"); // Add a class indicating an image is present
    };

    // Start reading the file as a data URL
    reader.readAsDataURL(file);
  };

  /**
   * Initializes all image upload boxes on the page.
   *
   * Features supported:
   * - Image preview after file selection
   * - Drag-and-drop image upload
   * - Visual feedback while dragging files
   * - Remove button to clear the image
   * - Hidden flag to indicate when an image has been removed (used for backend logic)
   *
   * @returns {void}
   */
  const setupImageUploads = () => {
    // Find all upload containers on the page
    const uploadBoxes = document.querySelectorAll(".upload-box");

    // Stop if no upload boxes exist
    if (!uploadBoxes.length) return;

    // Initialize behaviour for each upload box
    uploadBoxes.forEach((box) => {
      // Find important elements inside the upload box
      const input = box.querySelector("input[type='file']");
      const preview = box.querySelector(".image-preview");
      const placeholder = box.querySelector(".upload-placeholder");
      const removeBtn = box.querySelector(".upload-remove");
      const removeFlagInput = box.querySelector(".upload-remove-flag");

      // Stop if the file input does not exist
      if (!input) return;

      /**
       * Updates the visual style of the drop zone when dragging files.
       *
       * @param {boolean} active - Whether the drag state is active.
       */
      const setDropzoneStyles = (active) => {
        box.style.borderColor = active ? "#ffb6c1" : "#ccc";
        box.style.background = active ? "rgba(255,182,193,0.2)" : "transparent";
      };

      /**
       * Resets the upload box to its initial state.
       * Clears the preview image, shows the placeholder,
       * and marks the image as removed using the hidden flag.
       */
      const resetImage = () => {
        // Clear preview image
        if (preview) {
          preview.src = "";
          preview.style.display = "none";
        }

        // Show placeholder again
        if (placeholder) {
          placeholder.style.display = "block";
        }

        // Reset input and remove "has-image" styling
        input.value = "";
        box.classList.remove("has-image");

        // Update hidden removal flag for backend logic
        if (removeFlagInput) {
          removeFlagInput.value = "1";
        }
      };

      /**
       * Handle file selection through the file input.
       * Updates the removal flag and generates a preview.
       */
      input.addEventListener("change", () => {
        // Update removal flag depending on whether a file exists
        if (removeFlagInput) {
          removeFlagInput.value = input.files?.length ? "0" : "1";
        }

        // Generate preview
        handleImagePreview(input, box);
      });

      /**
       * Highlight the drop zone when a file is dragged over it.
       */
      box.addEventListener("dragover", (event) => {
        event.preventDefault();
        setDropzoneStyles(true);
      });

      /**
       * Reset drop zone style when dragging leaves the area.
       */
      box.addEventListener("dragleave", () => {
        setDropzoneStyles(false);
      });

      /**
       * Handle dropping a file into the upload box.
       * Simulates a normal file selection by assigning the files
       * to the input element and triggering the change event.
       */
      box.addEventListener("drop", (event) => {
        event.preventDefault();
        setDropzoneStyles(false);

        const files = event.dataTransfer.files;

        if (files?.[0]) {
          input.files = files;
          input.dispatchEvent(new Event("change"));
        }
      });

      /**
       * Remove button behaviour.
       * Clears the preview and marks the image as removed.
       */
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
   * Display a live character counter for textareas with maxlength attribute.
   * Updates the counter on every input event to show current length vs maximum.
   * Requires a sibling element with class "char-counter" to display the count.
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
   PROFILE TOGGLE
   =============================== */

  /**
   * Switch between dog and owner views on profile cards.
   * Manages the visibility of dog/owner information sections within each profile card.
   * Handles button states and view transitions.
   * @returns {void}
   */
  const setupProfileToggle = () => {
    // Cards can be either profile cards or match cards, both need the toggle
    document.querySelectorAll(".profile-card, .matches-card").forEach((card) => {
      const toggleButtons = card.querySelectorAll(".toggle-btn");
      const dogView = card.querySelector(".dog-view");
      const ownerView = card.querySelector(".owner-view");

      // If any required element is missing, skip this card
      if (!dogView || !ownerView || !toggleButtons.length) return;

      toggleButtons.forEach((button) => {
        button.addEventListener("click", () => {
          // Reset all buttons then activate only the clicked one
          toggleButtons.forEach((btn) => btn.classList.remove("active"));
          button.classList.add("active");

          // Show the selected view and hide the other
          if (button.dataset.view === "dog") {
            dogView.classList.remove("hidden");
            ownerView.classList.add("hidden");
          }
          else {
            ownerView.classList.remove("hidden");
            dogView.classList.add("hidden");
          }
        });
      });
    });
  };

  /* ===============================
     MODALS
     =============================== */

  /**
   * Handle the match modal open/close and body scroll lock.
   * Prevents body scrolling when modal is open by adding "modal-open" class.
   * Sets up close button event handler.
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
   * Cache form inputs in sessionStorage to preserve user progress.
   * Automatically saves and restores form field values including text inputs, textareas,
   * selects, and checkbox groups. Excludes file inputs for security reasons.
   * @param {string} formType - Data attribute value identifying the form (e.g., "owner", "dog").
   * @returns {void}
   */
  const setupFormCache = (formType) => {
    const form = document.querySelector(`form[data-form-type="${formType}"]`);
    if (!form) return;

    const inputs = form.querySelectorAll("input, textarea, select");
    const handledCheckboxGroups = new Set();
    const cacheKey = (name) => `${formType}_${name}`;

    /**
     * Get all checkboxes with the specified name.
     * @param {string} name - The name attribute of checkbox inputs.
     * @returns {Array<HTMLInputElement>} Array of checkbox elements.
     */
    const getCheckboxGroup = (name) =>
      Array.from(
        form.querySelectorAll(
          `input[type="checkbox"][name="${CSS.escape(name)}"]`,
        ),
      );

    /**
     * Restore checkbox group selections from sessionStorage.
     * @param {string} name - The name attribute of checkbox group.
     */
    const restoreCheckboxGroup = (name) => {
      const checkboxes = getCheckboxGroup(name);
      const savedValue = sessionStorage.getItem(cacheKey(name));
      if (!savedValue) return;

      let values = [];
      try {
        values = JSON.parse(savedValue);
      } catch (error) {
        // If JSON parsing fails, reset to empty array
        values = [];
      }

      checkboxes.forEach((cb) => {
        cb.checked = values.includes(cb.value);
      });
    };

    /**
     * Save checkbox group selections to sessionStorage.
     * @param {string} name - The name attribute of checkbox group.
     */
    const saveCheckboxGroup = (name) => {
      const checkboxes = getCheckboxGroup(name);
      const values = checkboxes
        .filter((cb) => cb.checked)
        .map((cb) => cb.value);
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
   * Enforce maximum selection limits on pill-style checkbox groups.
   * Disables unchecked options when the limit is reached and updates helper text.
   * Reads the max limit from the data-max attribute on the container.
   * @returns {void}
   */
  const setupPillOptions = () => {
    const groups = document.querySelectorAll(".pill-options[data-max]");
    groups.forEach((group) => {
      const max = parseInt(group.dataset.max || "0", 10);
      const checkboxes = Array.from(
        group.querySelectorAll("input[type='checkbox']"),
      );
      if (!checkboxes.length || !max) return;

      const helper = group.parentElement.querySelector(".pill-helper");

      /**
       * Update UI state based on current selections.
       * Disables checkboxes when limit is reached and updates counter text.
       */
      const update = () => {
        const selected = checkboxes.filter((cb) => cb.checked);
        const limitReached = selected.length >= max;

        // Disable unchecked options when limit is reached
        checkboxes.forEach((cb) => {
          cb.disabled = limitReached && !cb.checked;
          cb.parentElement.classList.toggle("is-disabled", cb.disabled);
        });

        // Update helper text with current selection count
        if (helper) {
          helper.textContent = `Select up to ${max} (${selected.length}/${max})`;
        }
      };

      checkboxes.forEach((cb) => cb.addEventListener("change", update));
      update();
    });
  };

  /* ===============================
     RESET MATCHES
     =============================== */

  /**
   * Setup reset matches modal and functionality.
   * Allows users to clear all their match history with a confirmation modal.
   * Handles modal open/close and form submission.
   * @returns {void}
   */
  const setupResetMatches = () => {
    const resetBtn = document.getElementById("resetMatchesBtn");
    if (!resetBtn) return;

    resetBtn.addEventListener("click", () => {
      const resetModal = document.getElementById("resetConfirmModal");
      if (resetModal) {
        resetModal.classList.add("is-open");
        document.body.classList.add("modal-open");
      }
    });

    // Close modal
    const closeResetModal = document.getElementById("closeResetModal");
    if (closeResetModal) {
      closeResetModal.addEventListener("click", () => {
        document
          .getElementById("resetConfirmModal")
          .classList.remove("is-open");
        document.body.classList.remove("modal-open");
      });
    }

    const cancelResetBtn = document.getElementById("cancelResetBtn");
    if (cancelResetBtn) {
      cancelResetBtn.addEventListener("click", () => {
        document
          .getElementById("resetConfirmModal")
          .classList.remove("is-open");
        document.body.classList.remove("modal-open");
      });
    }

    // Confirm reset
    const confirmResetBtn = document.getElementById("confirmResetBtn");
    if (confirmResetBtn) {
      confirmResetBtn.addEventListener("click", () => {
        document.getElementById("resetMatchesForm").submit();
      });
    }

    // Close modal on backdrop click
    const resetConfirmModal = document.getElementById("resetConfirmModal");
    if (resetConfirmModal) {
      resetConfirmModal.addEventListener("click", (e) => {
        if (e.target.id === "resetConfirmModal") {
          document
            .getElementById("resetConfirmModal")
            .classList.remove("is-open");
          document.body.classList.remove("modal-open");
        }
      });
    }
  };

  /* ===============================
     MESSAGES INBOX
     =============================== */

  /**
   * Setup inbox interactions for split-view messaging.
   * Implements a two-panel messaging interface on desktop (>=992px):
   * - Left panel: conversation list
   * - Right panel: message thread
   * Fetches and displays messages via AJAX, handles message sending,
   * and maintains active conversation state.
   * @returns {void}
   */
  /**
   * Setup messaging inbox functionality for desktop split-view.
   * Handles conversation selection via AJAX, message loading, and form submission.
   * Only activates on desktop screens (992px+) to avoid conflicts with mobile thread view.
   * @returns {void}
   */
  const setupMessagesInbox = () => {
    const inboxCard = document.querySelector(".messages-container-card");
    if (!inboxCard) return;

    // Prevent duplicate listener attachment
    if (inboxCard._messagesInboxListenerAttached) return;
    inboxCard._messagesInboxListenerAttached = true;

    const myDogAvatar = inboxCard.dataset.myDogAvatar || "";
    const myDogName = inboxCard.dataset.myDogName || "You";

    const conversationCards = document.querySelectorAll(".conversation-card");
    conversationCards.forEach((card) => {
      card.addEventListener("click", function (e) {
        const threadPanel = document.querySelector(".messages-thread-panel");
        // Only use split-view behavior on desktop screens
        if (
          window.innerWidth >= 992 &&
          threadPanel &&
          getComputedStyle(threadPanel).display !== "none"
        ) {
          e.preventDefault();

          // Extract conversation details from card data attributes
          const dogId = this.dataset.dogId;
          const dogName = this.dataset.name;
          const dogBreed = this.dataset.breed;
          const dogPhoto = this.dataset.photo;

          document.getElementById("thread-name").textContent = dogName;
          document.getElementById("thread-breed").textContent = dogBreed;
          document.getElementById("thread-avatar").src = dogPhoto;
          document.getElementById("receiver-dog-id").value = dogId;

          // Fetch message thread via API
          fetch(`/messages/api/${dogId}/`)
            .then((response) => response.json())
            .then((data) => {
              const messagesContainer =
                document.getElementById("messages-thread");
              messagesContainer.innerHTML = "";

              // Render messages if available
              if (data.messages && data.messages.length > 0) {
                data.messages.forEach((msg) => {
                  const messageRow = document.createElement("div");
                  messageRow.className = `message-row d-flex align-items-end gap-2 ${msg.is_sent ? "justify-content-end sent" : "justify-content-start received"}`;

                  const avatar = msg.is_sent ? myDogAvatar : dogPhoto;
                  const avatarAlt = msg.is_sent ? myDogName : dogName;

                  if (!msg.is_sent) {
                    messageRow.innerHTML += `<img class="message-avatar" src="${avatar}" alt="${avatarAlt}">`;
                  }

                  messageRow.innerHTML += `
                    <div class="message-bubble d-flex flex-column gap-1 px-3 py-2">
                      <p class="message-content m-0">${msg.content}</p>
                      <span class="message-time">${msg.time}</span>
                    </div>
                  `;

                  if (msg.is_sent) {
                    messageRow.innerHTML += `<img class="message-avatar" src="${avatar}" alt="${avatarAlt}">`;
                  }

                  messagesContainer.appendChild(messageRow);
                });
              } else {
                messagesContainer.innerHTML =
                  '<div class="empty-thread"><p>No messages yet. Send your first message!</p></div>';
              }

              // Auto-scroll to bottom to show latest message
              messagesContainer.scrollTop = messagesContainer.scrollHeight;
            });

          document.querySelectorAll(".conversation-item").forEach((item) => {
            item.classList.remove("active");
          });
          this.closest(".conversation-item").classList.add("active");
        }
      });
    });

    // Handle Enter key to send message (Shift+Enter for new line)
    const messageTextarea = document.querySelector("#message-form textarea");
    if (
      messageTextarea &&
      !messageTextarea._enterKeyListenerAttached &&
      window.innerWidth >= 992
    ) {
      messageTextarea._enterKeyListenerAttached = true;
      messageTextarea.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          const form = this.closest("form");
          if (form) {
            form.dispatchEvent(
              new Event("submit", { bubbles: true, cancelable: true }),
            );
          }
        }
      });
    }

    // Handle message form submission via AJAX on desktop
    const messageForm = document.getElementById("message-form");
    if (
      messageForm &&
      !messageForm._messagesInboxSubmitListenerAttached &&
      window.innerWidth >= 992
    ) {
      messageForm._messagesInboxSubmitListenerAttached = true;
      messageForm.addEventListener("submit", function (e) {
        const threadPanel = document.querySelector(".messages-thread-panel");
        // Only use AJAX submission on desktop split-view
        if (
          window.innerWidth >= 992 &&
          threadPanel &&
          getComputedStyle(threadPanel).display !== "none"
        ) {
          e.preventDefault();

          const formData = new FormData(this);
          const receiverDogId =
            document.getElementById("receiver-dog-id").value;
          const messagesContainer = document.getElementById("messages-thread");
          const isFirstMessage =
            messagesContainer.querySelector(".message-row") === null;

          fetch(`/messages/send/${receiverDogId}/`, {
            method: "POST",
            body: formData,
            headers: {
              "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
              "X-Requested-With": "XMLHttpRequest",
            },
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.success) {
                if (isFirstMessage) {
                  // First message: reload to show conversation in sidebar
                  window.location.reload();
                } else {
                  // Append message without reload
                  const messageRow = document.createElement("div");
                  messageRow.className =
                    "message-row d-flex align-items-end gap-2 justify-content-end sent";

                  // Use avatar from response if available, otherwise fall back to stored value
                  const avatarSrc = data.message.avatar || myDogAvatar;

                  messageRow.innerHTML = `
                  <div class="message-bubble d-flex flex-column gap-1 px-3 py-2">
                    <p class="message-content m-0">${data.message.content}</p>
                    <span class="message-time">${data.message.time}</span>
                  </div>
                  <img class="message-avatar" src="${avatarSrc}" alt="${myDogName}">
                `;
                  messagesContainer.appendChild(messageRow);
                  messagesContainer.scrollTop = messagesContainer.scrollHeight;

                  // Clear and refocus textarea
                  const textarea = this.querySelector("textarea");
                  textarea.value = "";
                  textarea.focus();
                }
              }
            });
        }
      });
    }

    const firstConversation = document.querySelector(".conversation-item");
    if (firstConversation) {
      firstConversation.classList.add("active");
    }

    // Auto-scroll to bottom of messages on page load
    const messagesThread = document.getElementById("messages-thread");
    if (messagesThread) {
      messagesThread.scrollTop = messagesThread.scrollHeight;
    }

    // Auto-focus textarea on page load (desktop only)
    if (window.innerWidth >= 992 && messageTextarea) {
      messageTextarea.focus();
    }
  };

  /* ===============================
     MESSAGE THREAD (Mobile)
     =============================== */

  /**
   * Setup message thread functionality for mobile/tablet messaging.
   * Handles Enter key to send messages, AJAX form submission, and auto-scroll.
   * Only activates on small screens (below 992px) and when on the thread.html page.
   * Mutually exclusive with setupMessagesInbox to prevent duplicate message sending.
   * @returns {void}
   */
  const setupMessageThread = () => {
    const messageForm = document.getElementById("message-form");
    const receiverDogIdInput = document.getElementById("receiver-dog-id");

    // Only run on mobile thread page (has receiver-dog-id input) and only on small screens
    if (!receiverDogIdInput || window.innerWidth >= 992) return;

    // Prevent duplicate listener attachment
    if (messageForm._messageThreadListenerAttached) return;
    messageForm._messageThreadListenerAttached = true;

    const messagesContainer = document.getElementById("messages-thread");
    if (!messagesContainer) return;

    // Get dog info from page data attributes for message display
    const threadPageEl =
      document.getElementById("message-thread-page") ||
      document.querySelector(".message-thread-page");
    const myDogName = threadPageEl?.dataset.myDogName || "You";
    const myDogAvatar = threadPageEl?.dataset.myDogAvatar || "";

    // Handle Enter key to send message (Shift+Enter for new line)
    const messageTextarea = messageForm?.querySelector("textarea");
    if (messageTextarea) {
      messageTextarea.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          const form = this.closest("form");
          if (form) {
            form.dispatchEvent(
              new Event("submit", { bubbles: true, cancelable: true }),
            );
          }
        }
      });
    }

    // Handle message form submission via AJAX
    if (messageForm) {
      messageForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const receiverDogId = receiverDogIdInput.value;
        const isFirstMessage =
          messagesContainer.querySelector(".message-row") === null;

        fetch(`/messages/send/${receiverDogId}/`, {
          method: "POST",
          body: formData,
          headers: {
            "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
            "X-Requested-With": "XMLHttpRequest",
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              if (isFirstMessage) {
                // First message: reload to show conversation in sidebar
                window.location.reload();
              } else {
                // Append message without reload
                const messageRow = document.createElement("div");
                messageRow.className =
                  "message-row d-flex align-items-end gap-2 justify-content-end sent";

                // Use avatar from response if available, otherwise fall back to stored value
                const avatarSrc = data.message.avatar || myDogAvatar;

                messageRow.innerHTML = `
                <div class="message-bubble d-flex flex-column gap-1 px-3 py-2">
                  <p class="message-content m-0">${data.message.content}</p>
                  <span class="message-time">${data.message.time}</span>
                </div>
                <img class="message-avatar" src="${avatarSrc}" alt="${myDogName}">
              `;
                messagesContainer.appendChild(messageRow);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;

                // Clear and refocus textarea
                messageTextarea.value = "";
                messageTextarea.focus();
              }
            }
          })
          .catch((error) => console.error("Error sending message:", error));
      });
    }

    // Auto-scroll to bottom of messages on page load
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Auto-focus textarea on page load
    if (messageTextarea) {
      messageTextarea.focus();
    }
  };

  /* ===============================
     DELETE CONVERSATION
     =============================== */

  /**
   * Setup delete conversation modal and functionality.
   * Allows users to delete an entire conversation thread with confirmation.
   * Handles modal display, close actions, and form submission to backend.
   * @returns {void}
   */
  const setupDeleteConversation = () => {
    const deleteButtons = document.querySelectorAll(".btn-delete-conversation");
    if (deleteButtons.length === 0) return;

    let selectedDogId = null;

    deleteButtons.forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation(); // Prevent conversation card click
        const dogId = btn.dataset.dogId;
        const dogName = btn
          .closest(".conversation-item")
          .querySelector(".dog-details h3").textContent;

        // Store selected conversation and show confirmation modal
        selectedDogId = dogId;
        document.getElementById("deleteDogName").textContent = dogName;
        document.getElementById("deleteConfirmModal").classList.add("is-open");
        document.body.classList.add("modal-open");
      });
    });

    // Close modal
    const closeDeleteModal = document.getElementById("closeDeleteModal");
    if (closeDeleteModal) {
      closeDeleteModal.addEventListener("click", () => {
        document
          .getElementById("deleteConfirmModal")
          .classList.remove("is-open");
        document.body.classList.remove("modal-open");
      });
    }

    const cancelDeleteBtn = document.getElementById("cancelDeleteBtn");
    if (cancelDeleteBtn) {
      cancelDeleteBtn.addEventListener("click", () => {
        document
          .getElementById("deleteConfirmModal")
          .classList.remove("is-open");
        document.body.classList.remove("modal-open");
      });
    }

    // Confirm delete - submit via AJAX to backend
    const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
    if (confirmDeleteBtn) {
      confirmDeleteBtn.addEventListener("click", () => {
        if (selectedDogId) {
          // Get CSRF token
          const csrfToken = document.querySelector(
            "[name=csrfmiddlewaretoken]",
          )?.value;

          // Submit delete request via fetch
          fetch(`/messages/delete/${selectedDogId}/`, {
            method: "POST",
            headers: {
              "X-CSRFToken": csrfToken || "",
              "Content-Type": "application/json",
            },
          })
            .then((response) => {
              if (response.ok) {
                // Redirect to inbox after successful delete
                window.location.href = "/messages/";
              }
            })
            .catch((error) =>
              console.error("Error deleting conversation:", error),
            );
        }
      });
    }

    // Close modal on backdrop click
    const deleteConfirmModal = document.getElementById("deleteConfirmModal");
    if (deleteConfirmModal) {
      deleteConfirmModal.addEventListener("click", (e) => {
        if (e.target.id === "deleteConfirmModal") {
          document
            .getElementById("deleteConfirmModal")
            .classList.remove("is-open");
          document.body.classList.remove("modal-open");
        }
      });
    }
  };

  /* ===============================
     DELETE MATCH
     =============================== */

  /**
   * Setup delete match modal and functionality.
   * Allows users to unmatch with another dog profile via a confirmation modal.
   * Makes an AJAX request to delete the match and removes the card from UI.
   * @returns {void}
   */
  const setupDeleteMatch = () => {
    let selectedDogId = null;
    const deleteButtons = document.querySelectorAll(".btn-delete-match");
    const modal = document.getElementById("deleteMatchModal");
    const cancelBtn = document.getElementById("cancelDeleteMatchBtn");
    const confirmBtn = document.getElementById("confirmDeleteMatchBtn");
    if (!deleteButtons.length || !modal) return;

    deleteButtons.forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        selectedDogId = btn.dataset.dogId;
        modal.classList.add("is-open");
        document.body.classList.add("modal-open");
      });
    });

    cancelBtn.addEventListener("click", () => {
      modal.classList.remove("is-open");
      document.body.classList.remove("modal-open");
      selectedDogId = null;
    });

    confirmBtn.addEventListener("click", () => {
      if (!selectedDogId) return;

      // Get CSRF token for secure POST request
      const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");

      fetch("/connections/delete_match/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrfToken ? csrfToken.value : "",
        },
        body: `dog_id=${selectedDogId}`,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            // Remove match card from UI
            const card = document.querySelector(
              `.matches-card[data-dog-id="${selectedDogId}"]`,
            );
            if (card) card.remove();

            // Check if any match cards remain
            const remainingCards = document.querySelectorAll(".matches-card");
            if (remainingCards.length === 0) {
              // Reload page to show "No matches yet" empty state
              window.location.reload();
            }
          }
          modal.classList.remove("is-open");
          document.body.classList.remove("modal-open");
          selectedDogId = null;
        });
    });

    // Close modal on backdrop click
    modal.addEventListener("click", (e) => {
      if (e.target.id === "deleteMatchModal") {
        modal.classList.remove("is-open");
        document.body.classList.remove("modal-open");
        selectedDogId = null;
      }
    });
  };

  /* ===============================
     DELETE PROFILE
     =============================== */

  /**
   * Setup delete profile modal and functionality.
   * Handles the critical action of permanently deleting a user profile.
   * Exposes global functions for modal control (open/close/confirm).
   * @returns {void}
   */
  const setupDeleteProfile = () => {
    const deleteModal = document.getElementById("deleteModal");
    if (!deleteModal) return;

    // Expose global functions for template onclick handlers

    /**
     * Open the delete profile confirmation modal.
     */
    window.openDeleteModal = function () {
      deleteModal.classList.add("is-open");
      document.body.classList.add("modal-open");
    };

    /**
     * Close the delete profile confirmation modal.
     */
    window.closeDeleteModal = function () {
      deleteModal.classList.remove("is-open");
      document.body.classList.remove("modal-open");
    };

    /**
     * Submit the delete profile form after confirmation.
     */
    window.confirmDelete = function () {
      document.body.classList.remove("modal-open");
      document.getElementById("deleteForm").submit();
    };

    // Close modal on backdrop click
    deleteModal.addEventListener("click", function (e) {
      if (e.target === this) {
        window.closeDeleteModal();
      }
    });
  };

  /* ===============================
     INITIALIZATION
     =============================== */

  /**
   * Initialize all UI components and behaviors.
   * Called automatically when DOM is fully loaded.
   * Sets up all event listeners and interactive features for the application.
   * @returns {void}
   */
  const init = () => {
    setupNavbarCollapse();
    setupPasswordToggle();
    setupProfileToggle();
    setupImageUploads();
    setupCharacterCounters();
    setupMatchModal();
    setupFormCache("owner");
    setupFormCache("dog");
    setupPillOptions();
    setupResetMatches();
    setupMessagesInbox();
    setupMessageThread();
    setupDeleteConversation();
    setupDeleteMatch();
    setupDeleteProfile();
  };

  // Start initialization
  init();
});
