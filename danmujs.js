$(document).ready(function(){
 $("#msg").html("<h2>jQuery Hello World</h2>");

});



setInterval(function(){
    // console.log("hi")
    $("ul").append("<li class='Barrage-listItem'><span class='Barrage-nickName'>Annoymous</span><span class='Barrage-content'>" +$.now() + "</span></li>");
}, 500);
