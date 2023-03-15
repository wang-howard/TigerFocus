function assignmentsTabClicked() {
  var tabfirst = document.getElementById("assignments_tab");
  var tabsecond = document.getElementById("preloaded_tab");
  tabfirst.style.zIndex = 2;
  tabsecond.style.zindex = 1;
  print("tab 1");
}

function preloadedTabClicked() {
  var tabfirst = document.getElementById("preloaded_tab");
  var tabsecond = document.getElementById("assignments_tab");
  tabfirst.style.zIndex = 2;
  tabsecond.style.zindex = 1;
  print("tab 2");
}
