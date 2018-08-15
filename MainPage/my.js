$('#btnShowLeftBar').bind("click",ShowLeftBar)
function ShowLeftBar(){
    $('#MainPage').attr("style","transform: translate(70%, 0);") //rotate3d(.25,1,.25,360deg)
    $('#LeftBar').attr("style","transform: translate(100%, 0);")
    $('#btnShowLeftBar').unbind("click")
    $('#btnShowLeftBar').bind("click",HideLeftBar)
}
function HideLeftBar(){
    $('#MainPage').attr("style","transform: ;")
    $('#LeftBar').attr("style","transform: ;")
    $('#btnShowLeftBar').unbind("click")
    $('#btnShowLeftBar').bind("click",ShowLeftBar)
}
$('#BottomBarBtn_1').bind("click",ShowMainPage1)
$('#BottomBarBtn_2').bind("click",ShowMainPage2)
$('#BottomBarBtn_3').bind("click",ShowMainPage3)
function ShowMainPage1(){
    $('#ContentPage').attr("src","./page1.html");
}
function ShowMainPage2(){
    $('#ContentPage').attr("src","./page2.html");
}
function ShowMainPage3(){
    $('#ContentPage').attr("src","./page3.html");
}