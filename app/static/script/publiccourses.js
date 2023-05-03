function importCourses() {
  // get all checked checkboxes
  const checkboxes = document.querySelectorAll(".course_checkbox:checked");

  // create an array to store the titles of the checked assignments
  const selectedCourses = [];

  // iterate over each checked checkbox and add its corresponding assignment title to the array
  checkboxes.forEach((checkbox) => {
    const course_id = checkbox.getAttribute("value");
    selectedCourses.push(course_id);
  });

  if (selectedCourses.length === 0) {
    alert("Please mark off courses to import");
  }

  // log the selected assignments
  console.log("Selected Courses:", selectedCourses);

  const hiddenInput = document.getElementById("selected_courses");
  hiddenInput.value = selectedCourses;

  console.log("Hidden Input Value:", hiddenInput.value);
}
