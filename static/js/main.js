console.log("MAIN JS LOADED");

document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM READY");

  const toggleBtns = document.querySelectorAll(".toggle-password");
  console.log("Toggle buttons:", toggleBtns.length);

  toggleBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      console.log("EYE CLICKED");

      const input = btn.parentElement.querySelector("input");

      if (!input) {
        console.log("NO INPUT FOUND");
        return;
      }

      input.type = input.type === "password" ? "text" : "password";
      console.log("TOGGLED TO:", input.type);
    });
  });
});
