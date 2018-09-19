function slide1(){
	$('#img1').css({'transform':'translate(206%,0)','transition': 'all 0.0s ease-out'})
	$('#img2').css({'transform':'translate(-103%,0)','transition': 'all 0.8s ease-out'})
	$('#img3').css({'transform':'translate(-103%,0)','transition': 'all 0.8s ease-out'})	
}

function slide2(){
	$('#img1').css({'transform':'translate(103%,0)','transition': 'all 0.8s ease-out'})
	$('#img2').css({'transform':'translate(103%,0)','transition': 'all 0.0s ease-out'})
	$('#img3').css({'transform':'translate(-206%,0)','transition': 'all 0.8s ease-out'})	
}

function slide3(){
	$('#img1').css({'transform':'translate(0,0)','transition': 'all 0.8s ease-out'})
	$('#img2').css({'transform':'translate(0,0)','transition': 'all 0.8s ease-out'})
	$('#img3').css({'transform':'translate(0,0)','transition': 'all 0.0s ease-out'})	
}

function rotate(){
	setTimeout(slide1,1000)
	setTimeout(slide2,2800)
	setTimeout(slide3,4600)
}

rotate()
setInterval(rotate,5600)

