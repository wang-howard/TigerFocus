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

var edit_assignment_modal = document.getElementById("edit_assignment_modal");
var edit_assignment = document.getElementsByName("edited_assignment_id")[0];
var edit_assignment_btn = document.getElementsByName("edit_assignment_button");
var edit_assignment_span = document.getElementsByClassName("edit_assignment_close")[0];

edit_assignment_btn.forEach(
  (element) =>
    (element.onclick = function () {
      edit_assignment_modal.style.display = "block";
      edit_assignment.value = element.value;
    })
);

edit_assignment_span.onclick = function () {
  edit_assignment_modal.style.display = "none";
};
