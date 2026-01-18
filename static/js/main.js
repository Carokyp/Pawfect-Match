document.addEventListener("DOMContentLoaded", () => {
  const toggleBtns = document.querySelectorAll(".toggle-password");

  toggleBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const input = btn.parentElement.querySelector("input");

      if (!input) {
        return;
      }

      input.type = input.type === "password" ? "text" : "password";
    });
  });
});
