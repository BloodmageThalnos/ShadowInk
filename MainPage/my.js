$('#btnShowLeftBar').bind("click",btnShowLeftBar)
function btnShowLeftBar(){
    $('#MainPage').attr("style","transform: translate(70%, 0);") //rotate3d(.25,1,.25,360deg)
    $('#btnShowLeftBar').unbind("click")
    $('#btnShowLeftBar').bind("click",btnHideLeftBar)
}
function btnHideLeftBar(){
    $('#MainPage').attr("style","transform: ;")
    $('#btnShowLeftBar').unbind("click")
    $('#btnShowLeftBar').bind("click",btnShowLeftBar)
}

