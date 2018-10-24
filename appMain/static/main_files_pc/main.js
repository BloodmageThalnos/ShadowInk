function slide(){
    turn+=102.5;
    Css = {'transform':("translate(-"+turn+"%,0)"), 'transition': 'all 0.8s ease-out'};
    for(i=1;i<=pic_number*2;i++)
        $('#img'+i).css(Css);

    if(turn>307.42)setTimeout(function(){
    turn=0;
    Css = {'transform':("translate(0,0)"), 'transition': 'all 0.0s ease-out'};
    for(i=1;i<=pic_number*2;i++)
        $('#img'+i).css(Css);
    },800)
}
function doit(i,j){
  newinput = document.createElement("div")
  newinput.id='good'+i
  newinput.innerHTML='<input type="file" name="file'+i+'" onchange="doit('+(i+1)+')"/>'
  document.getElementById('good'+(i-1)).appendChild(newinput)
  j.setAttribute("onchange","")
}
function doita(i){
  $.ajax('/w/postWeibo',{
        type: 'POST',
        data: new FormData(i),
        async: true,
        cache: false,
        processData: false,
        contentType: false,
        success: function(msg) {
            msg = JSON.parse(msg)
            alert(msg.message)
            if(msg.success === 'True')
                location.reload(true);
        }
    })
  return false;
}
function doitat(i,j,k){
  formData = new FormData();
  formData.append("id", i)
  formData.append("action", k)
  $.ajax('/w/thumbWeibo', {
        type: 'POST',
        data: formData,
        async: true,
        cache: false,
        processData: false,
        contentType: false,
        success: function(msg) {
            msg = JSON.parse(msg)
            alert(msg.message)
            if(msg.success === 'True')
                location.reload(true)
        }
    })
}
function doitato(i){
  $.ajax('/w/commentWeibo',{
        type: 'POST',
        data: new FormData(i),
        async: true,
        cache: false,
        processData: false,
        contentType: false,
        success: function(msg) {
            msg = JSON.parse(msg)
            alert(msg.message)
            if(msg.success === 'True')
                location.reload(true);
        }
    })
  return false;
}
function dologin(){
  formData = new FormData();
  formData.append("name",$('#inputUsername').val())
  formData.append("password",$('#inputPassword').val())
  $.ajax('/login/ajaxLogin',{
        type: 'POST',
        data: formData,
        async: true,
        cache: false,
        processData: false,
        contentType: false,
        success: function(msg) {
            msg = JSON.parse(msg)
            alert(msg.message)
            if(msg.success === 'True')
                location.reload(true);
        }
    })
  return false;
}
function dologini(){
  formData = new FormData();
  formData.append("logout", "sure")
  $.ajax('/login/ajaxLogout',{
        type: 'POST',
        data: formData,
        async: true,
        cache: false,
        processData: false,
        contentType: false,
        success: function(msg) {
            msg = JSON.parse(msg)
            alert(msg.message)
            if(msg.success === 'True')
                location.reload(true);
        }
    })
}
function doregister(){
  formData = new FormData();
  formData.append("name",$('#inputUsername').val())
  formData.append("password",$('#inputPassword').val())
  $.ajax('/login/ajaxRegister',{
        type: 'POST',
        data: formData,
        async: true,
        cache: false,
        processData: false,
        contentType: false,
        success: function(msg) {
            msg = JSON.parse(msg)
            alert(msg.message)
            if(msg.success === 'True')
                location.reload(true);
        }
    })
  return false;
}
$(document).ready(function () {
    turn=0;
    pic_number=3;

    setInterval(slide,1500);

	$(".bar").click(function (e) {
        id = e.target.id.substr(4);
        console.log(id);
        $("#comment"+id).slideToggle();
		console.log('111');
    });

});


