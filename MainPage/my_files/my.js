$('#btnShowLeftBar').bind("click",ShowLeftBar)
function ShowLeftBar(){
    $('#MainPage').attr("style","transform: translate(70%, 0);")
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
    $('#ContentPage').attr("src","./pages/page1.html");
}
function ShowMainPage2(){
    $('#ContentPage').attr("src","./pages/page2.html");
}
function ShowMainPage3(){
    $('#ContentPage').attr("src","./pages/page3.html");
}
function Quit() {
    var result = confirm('是否真的要退出？');
    if(result){
    	window.location.href="login.html";
    }
}

function About(){
	window.confirm('Author : Group 16');
}