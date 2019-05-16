// Add a goal Modal
var modal = document.getElementById("addAGoal");

// Get the button that opens the modal
var btn = document.getElementById("addAGoalBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// Add a goal Modal
var modal1 = document.getElementById("addAnActivity");

// Get the button that opens the modal
var btn1 = document.getElementById("addAnActivityBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn1.onclick = function() {
  modal1.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal1.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal1) {
    modal1.style.display = "none";
  }
}
    /**
     *
     * Modals

addAGoal
Add an activity
Calorie Intake
Food Intake (Which includes calories)
Calorie goals
A modal with a list of all the foods that have been added to the food intake list
     */
