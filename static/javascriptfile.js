$("#logo").css('opacity','0');

$("#select_logo").click(function(e){
e.preventDefault();
$("#logo").trigger('click');
});
submitForms = function(){
    document.forms["form1"].submit();
    document.forms["form2"].submit();
    }


/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function dropDownFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }  