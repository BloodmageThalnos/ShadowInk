$(function(){
    $('#LeftPicContainer').on("click",function(){
        $('#LeftSelect').click()
    })

    $('#Go').on("click",function(){
        formData = new FormData($("#aForm")[0]);
        $.ajax({
            url: '/p/post',
            type: 'POST',
            data: formData,
            async: true,
            cache: false,
            contentType: false,
            processData: false,
            success: function(msg) {
                word = JSON.parse(msg)
                alert(word.message)
                $("#RightPic").attr("src",word["src"])
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
        var img = document.getElementById("LeftPic");
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
}
