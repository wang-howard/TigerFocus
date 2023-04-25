var course_create_modal = document.getElementById("admincourse_modal");
var course_create_btn = document.getElementById("admincourse_button");
var course_span = document.getElementsByClassName("admincourse_close")[0];
course_create_btn.onclick = function () {
  course_create_modal.style.display = "block";
};
course_span.onclick = function () {
  course_create_modal.style.display = "none";
};
