// 返回按钮点击事件
window.onload = function(){
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
    var reader = new FileReader();
    var file = fileDom.files[0];
    var imageType = /^image\//;
    if (!imageType.test(file.type)) {
        return;
    }
    reader.onload = function(e) {
        var img = document.getElementById("preview");
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
}






