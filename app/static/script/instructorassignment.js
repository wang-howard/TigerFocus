var assignment_create_modal = document.getElementById("admin_create_new_modal");
var assignment_create_btn = document.getElementById("admin_create_new_button");
var assignment_span = document.getElementsByClassName("admin_create_close")[0];
var id = document.getElementById("current_id");
var current = document.getElementById("current_course_id");

id.value = current.value;

assignment_create_btn.onclick = function () {
  assignment_create_modal.style.display = "block";
};
assignment_span.onclick = function () {
  assignment_create_modal.style.display = "none";
};
