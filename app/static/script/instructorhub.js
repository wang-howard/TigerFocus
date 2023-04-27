var course_create_modal = document.getElementById("admincourse_modal");
var course_create_btn = document.getElementById("admincourse_button");
var course_span = document.getElementsByClassName("admincourse_close")[0];
course_create_btn.onclick = function () {
  course_create_modal.style.display = "block";
};
course_span.onclick = function () {
  course_create_modal.style.display = "none";
};

var editcourse_modal = document.getElementById("instructor_edit_course_modal");
var edit_course = document.getElementsByName("instructor_edited_course_id")[0];
var editcourse_btn = document.getElementsByName(
  "instructor_edit_course_button"
);
var editcourse_span = document.getElementsByClassName(
  "instructoreditcourse_close"
)[0];

editcourse_btn.forEach(
  (element) =>
    (element.onclick = function () {
      editcourse_modal.style.display = "block";
      edit_course.value = element.value;
    })
);

console.log(edit_course.value);

editcourse_span.onclick = function () {
  editcourse_modal.style.display = "none";
};

function exportCourses() {
  // get all checked checkboxes
  const checkboxes = document.querySelectorAll(".course_checkbox:checked");

  // create an array to store the titles of the checked assignments
  const selectedCourses = [];

  // iterate over each checked checkbox and add its corresponding assignment title to the array
  checkboxes.forEach((checkbox) => {
    const course_id = checkbox.getAttribute("value");
    selectedCourses.push(course_id);
  });

  // log the selected assignments
  console.log("Selected Courses:", selectedCourses);

  const hiddenInput = document.getElementById("selected_courses");
  hiddenInput.value = selectedCourses;

  console.log("Hidden Input Value:", hiddenInput.value);
}
