var width = $(window).width();
var initInnerHTML = document.getElementById("big").innerHTML;
if($(this).width() < 1200) {
    width = $(this).width();
    document.getElementById("big").innerHTML = document.getElementById("small").innerHTML;
}
$(window).on('resize', function(){
   	if($(this).width() < 1200){
      	width = $(this).width();
      	document.getElementById("big").innerHTML = document.getElementById("small").innerHTML;
   	}
   	if($(this).width() >= 1200){
      	width = $(this).width();
      	document.getElementById("big").innerHTML = initInnerHTML;
   	}
});