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
                if(word["src"]) $("#RightPic").attr("src",word["src"])
            }
        })
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
