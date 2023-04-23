var create_modal = document.getElementById("admincourse_modal");
var create_btn = document.getElementById("admincourse_button");
var span = document.getElementsByClassName("admincourse_close")[0];
create_btn.onclick = function () {
    create_modal.style.display = "block";
  };
span.onclick = function () {
    create_modal.style.display = "none";
};