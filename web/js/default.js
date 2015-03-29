$(document).ready(function () {
            $("#about").click(function () {
                 $('html, body').animate({
        scrollTop: $("#lower").offset().top
    }, 1000);
             })
        });
        window.onload = function() {
  document.getElementById("box").focus();
};