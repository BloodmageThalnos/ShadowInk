$(document).ready(function () {  
    turn=0
    pic_number=3
    function slide(){
        turn+=102.5
        Css = {'transform':("translate(-"+turn+"%,0)"), 'transition': 'all 0.8s ease-out'};
        for(i=1;i<=pic_number*2;i++)
            $('#img'+i).css(Css);
        
        if(turn==307.5)setTimeout(function(){
        turn=0
        Css = {'transform':("translate(0,0)"), 'transition': 'all 0.0s ease-out'};
        for(i=1;i<=pic_number*2;i++)
            $('#img'+i).css(Css);
        },800)
    }

    setInterval(slide,1500)
	
	
	$(".bar").click(function (e) {
        id = e.target.id.substr(4)
        console.log(id)
        $("#comment"+id).slideToggle();
		console.log('111');
    });
     

});


         