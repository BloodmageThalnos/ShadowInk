// 返回按钮点击事件
window.onload=function(){
    $('#exitButton').bind("click",function(){
        $('#FloatPage').attr("style","margin-top: "+$('body').height()+";")
        setTimeout(function(){
            parent.window.location.reload()
        }, 500);
    })
    $('#btnSend').bind("click",function(){
        formData = new FormData($("#aForm")[0]);
        $.ajax({  
            url: '/e/pPostArticle',
            type: 'POST',
            data: formData,
            async: false,  
            cache: false,  
            contentType: false,  
            processData: false,  
            success: function(msg) {
            }
        })
        
    })
}

function imgPreview(fileDom){
    //判断是否支持FileReader
    if (window.FileReader) {
        var reader = new FileReader();
    } else {
        alert("您的设备不支持图片预览功能，如需该功能请升级您的设备！");
    }
    //获取文件
    var file = fileDom.files[0];
    var imageType = /^image\//;
    //是否是图片
    if (!imageType.test(file.type)) {
        alert("请选择图片！");
        return;
    }
    //读取完成
    reader.onload = function(e) {
        //获取图片dom
        var img = document.getElementById("preview");
        //图片路径设置为读取的图片
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
}

function imgDelete(){
	window.confirm("确认删除吗？");
	if(result){
		$('#preview').src.reset();
	}
}






