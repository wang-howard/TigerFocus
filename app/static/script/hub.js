// Get the modal
var create_modal = document.getElementById("create_new_modal");
var edit_assignment_modal = document.getElementById("edit_assignment_modal");
var edit_assignment = document.getElementsByName("edited_assignment_id")[0];

var course_modal = document.getElementById("add_course_modal");
var coursenew_modal = document.getElementById("add_coursenew_modal");
var editcourse_modal = document.getElementById("edit_course_modal");
var edit_course = document.getElementsByName("edited_course_id")[0];

// Get the button that opens the modal
var create_btn = document.getElementById("create_new_button");
var course_btn = document.getElementById("add_course_button");
var coursenew_btn = document.getElementById("add_coursenew_button");
var editcourse_btn = document.getElementsByName("edit_course_button");
var edit_assignment_btn = document.getElementsByName("edit_assignment_button");
var status_btn = document.getElementsByName("status-button");

status_btn.forEach((element) => {
  let isClicked = false;
  element.addEventListener("click", function () {
    if (isClicked) {
      element.style.background = "#94AC74";
      var id = element.id;
      var str = "assignment-wrapper-" + id;
      var wrapper_div = document.getElementById(str);
      wrapper_div.style.opacity = 0.5;
      element.value = false;
    } else {
      element.style.background = "#FFBC79";
      var id = element.id;
      var str = "assignment-wrapper-" + id;
      var wrapper_div = document.getElementById(str);
      wrapper_div.style.opacity = 1;
      element.value = true;
    }
    isClicked = !isClicked;
  });
});

editcourse_btn.forEach(
  (element) =>
    (element.onclick = function () {
      editcourse_modal.style.display = "block";
      edit_course.value = element.value;
    })
);

edit_assignment_btn.forEach(
  (element) =>
    (element.onclick = function () {
      edit_assignment_modal.style.display = "block";
      edit_assignment.value = element.value;
    })
);

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
var course_span = document.getElementsByClassName("course-close")[0];
var coursenew_span = document.getElementsByClassName("add-course-close")[0];
var editcourse_span = document.getElementsByClassName("edit-course-close")[0];
var edit_assignment_span = document.getElementsByClassName("edit_assignment_close")[0];

// When the user clicks on the button, open the modal
create_btn.onclick = function () {
  create_modal.style.display = "block";
};

course_btn.onclick = function () {
  course_modal.style.display = "block";
};

coursenew_btn.onclick = function () {
  coursenew_modal.style.display = "block";
};

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  create_modal.style.display = "none";
};

course_span.onclick = function () {
  course_modal.style.display = "none";
};

coursenew_span.onclick = function () {
  coursenew_modal.style.display = "none";
};

editcourse_span.onclick = function () {
  editcourse_modal.style.display = "none";
};

edit_assignment_span.onclick = function () {
  edit_assignment_modal.style.display = "none";
};

function startSession() {

  console.log("button clicked ");
 
  const checkboxes = document.querySelectorAll(".assignment-checkbox:checked");

  const selectedAssignments = [];

  console.log(checkboxes);

  
  checkboxes.forEach((checkbox) => {
    const assignmentId = checkbox.getAttribute("value");
    const assignmentTitle = document.querySelector(`#assignment-wrapper-${assignmentId} .assignment-text`).innerText;
    selectedAssignments.push(assignmentTitle);
  });

  const hiddenInput = document.getElementById("selected_assignments");
  hiddenInput.value = selectedAssignments.join(',');

  if(selectedAssignments.length === 0)
    alert("You have not selected any assignments!") 

}

