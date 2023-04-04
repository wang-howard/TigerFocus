// Get the modal
var create_modal = document.getElementById("create_new_modal");
var course_modal = document.getElementById("add_course_modal");
var coursenew_modal = document.getElementById("add_coursenew_modal");
var editcourse_modal = document.getElementById("edit_course_modal");

// Get the button that opens the modal
var create_btn = document.getElementById("create_new_button");
var course_btn = document.getElementById("add_course_button");
var coursenew_btn = document.getElementById("add_coursenew_button");
var editcourse_btn = document.getElementById("edit_course_button");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
var course_span = document.getElementsByClassName("course_close")[0];
var coursenew_span = document.getElementsByClassName("coursenew_close")[0];
var editcourse_span = document.getElementsByClassName("editcourse_close")[0];

// var list = {};
// var checked_list = {};

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

editcourse_btn.onclick = function () {
  editcourse_modal.style.display = "block";
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
  editcourse_modal.style.displasy = "none";
};


  function startSession() {
    const checkboxes = document.querySelectorAll('.assignment_checkbox');
    const selectedAssignments = [];
  
    checkboxes.forEach((checkbox) => {
      if (checkbox.checked) {
        var assignmentId = checkbox.data-id;
        selectedAssignments.push(assignmentId);
      }
    });
  
    if (selectedAssignments.length === 0) {
      alert('Please select at least one assignment to start a session');
    } else {
      const assignmentsParagraph = document.createElement('p');
      assignmentsParagraph.textContent = `Selected Assignments: ${selectedAssignments.join(', ')}`;
      const sessionDiv = document.querySelector('#session_div');
      sessionDiv.appendChild(assignmentsParagraph);
    }
  }
  

  