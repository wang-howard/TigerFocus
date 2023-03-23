// Get the modal
var create_modal = document.getElementById("create_new_modal");
var course_modal = document.getElementById("add_course_modal");

// Get the button that opens the modal
var create_btn = document.getElementById("create_new_button");
var course_btn = document.getElementById("add_course_button");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
var course_span = document.getElementsByClassName("course_close")[0];

// When the user clicks on the button, open the modal
create_btn.onclick = function () {
  create_modal.style.display = "block";
};

course_btn.onclick = function () {
  course_modal.style.display = "block";
};

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  create_modal.style.display = "none";
};

course_span.onclick = function () {
  course_modal.style.display = "none";
};
