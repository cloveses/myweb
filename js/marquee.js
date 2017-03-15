$(function () { 
    $("#div2").html($("#div1").html()); //将div2的html设置成div1的html
    var mar = function () { 
    if ($("#container").scrollLeft() > $("#div1").width()) { //当滚动条隐藏的长度大于div1的宽度
        $("#container").scrollLeft(0);
    }
    else {
    $("#container").scrollLeft($("#container").scrollLeft() + 1); //每次滚动条往右移动1px；
}
}; 
var vid = setInterval(mar, 20);
$("#container").mouseenter(function () {
    clearInterval(vid);
}).mouseleave(function () {
    vid = setInterval(mar,20);
}); 
}); 