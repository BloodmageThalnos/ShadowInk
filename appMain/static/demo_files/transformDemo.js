$(function(){
    $('#uploadIt').on("click",function(){
        $('#LeftSelect').click()
    })

    $('#oneKeyTransfer').on("click",function(){
        formData = new FormData($("#aForm")[0]);
        $.ajax({
            url: '/s/dotran',
            type: 'POST',
            data: formData,
            async: true,
            cache: false,
            contentType: false,
            processData: false,
            success: function(msg) {
                word = JSON.parse(msg)
                alert(word.message)
                if(word["src"]){
                    $("#RightPic").attr("src",word["src"])
                    tranSuccess = 1;
                }
            }
        })
    })

    $('#downloadIt').on("click",function(){
        let src = $("#RightPic").attr("src");
        if(!src){
            alert("没有图片可下载！");return;
        }
        downloadIamge(src);
    })

    tranSuccess = 0
    $('#saveToMy').on("click",function(){
        if(tranSuccess===1){
            tranSuccess = 2;
            alert("保存成功！")
        }
        else if(tranSuccess===2){
            alert("已保存，请勿重复保存！")
        }
        else{
            alert("未成功转换图片，无法保存！")
        }
    })
})


function imgPreview(fileDom){
    var reader = new FileReader();
    var file = fileDom.files[0];
    var imageType = /^image\//;
    if (!imageType.test(file.type)) {
        return;
    }
    reader.onload = function(e) {
        var img = document.getElementById("RightPic");
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
}

function downloadIamge(imgsrc) {
    let image = new Image();
    image.setAttribute("crossOrigin", "anonymous");
    image.onload = function() {
      let canvas = document.createElement("canvas");
      canvas.width = image.width;
      canvas.height = image.height;
      let context = canvas.getContext("2d");
      context.drawImage(image, 0, 0, image.width, image.height);
      let url = canvas.toDataURL("image/png");
      let a = document.createElement("a");
      let event = new MouseEvent("click");
      a.download = "水墨";
      a.href = url;
      a.dispatchEvent(event);
    };
    image.src = imgsrc;
  }