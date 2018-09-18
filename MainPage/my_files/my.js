// 侧边栏点击滑入滑出效果
$('#btnShowLeftBar').bind("click",ShowLeftBar)
__GLOBAL_leftBarShown=true
function ShowLeftBar(){
    $('#MainPage').attr("style","transform: translate(70%, 0);")
    $('#LeftBar').attr("style","transform: translate(100%, 0);")
    $('#btnShowLeftBar').unbind("click")
    $('#btnShowLeftBar').bind("click",HideLeftBar)
    __GLOBAL_leftBarShown=true
}
function HideLeftBar(){
    $('#MainPage').attr("style","transform: ;")
    $('#LeftBar').attr("style","transform: ;")
    $('#btnShowLeftBar').unbind("click")
    $('#btnShowLeftBar').bind("click",ShowLeftBar)
    __GLOBAL_leftBarShown=false
}

// 撰写文章按钮点击事件
$('#FloatPage').attr("style","margin-top: "+$('body').height()+";")
$('#PostArticleBtn').bind("click",function(){
    HideLeftBar()
    $('#FloatPage').attr("style","margin-top: 0;")
})

$('#MyPage').attr("style","margin-top: "+$('body').height()+";")
$('#exitButton').bind("click",function(){
	console.log('111')
	$('#MyPage').attr("style","margin-top:0;")
	console.log('111')
})


// 底部按钮绑定点击事件
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

// 侧边栏退出按钮和关于按钮点击事件
function Quit(){
    var result = confirm('是否真的要退出？');
    if(result){
    	window.location.href="login.html";
    }
}
function About(){
	window.confirm('Author : Group 16');
}

// TODO：/explore中顶部图片滚动效果
/*
function RollTheImg(){
	$('MainPage-TopBar').attr("style","transform:translate(100%,0);")
	
}
*/