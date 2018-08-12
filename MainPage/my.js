$('#btnShowLeftBar').bind("click",btnShowLeftBar)
function btnShowLeftBar(){
    $('#MainPage').attr("style","transform: translate(70%, 0);") //rotate3d(.25,1,.25,360deg)
    $('#LeftBar').attr("style","transform: translate(100%, 0);")
    $('#btnShowLeftBar').unbind("click")
    $('#btnShowLeftBar').bind("click",btnHideLeftBar)
}
function btnHideLeftBar(){
    $('#MainPage').attr("style","transform: ;")
    $('#LeftBar').attr("style","transform: ;")
    $('#btnShowLeftBar').unbind("click")
    $('#btnShowLeftBar').bind("click",btnShowLeftBar)
}

