
	function y2k(number) { return (number < 1000) ? number + 1900 : number; }

	function dispdate(){
	     var now = new Date();
	     var dd = now.getDate() , mt = now.getMonth() + 1 , yy = y2k(now.getYear()) , weekVal = now.getDay();

	        if (weekVal==0)
	       msg1="星期日";
	    else if (weekVal==1)
	        msg1="星期一"; 
	    else if (weekVal==2)
	        msg1="星期二"; 
	    else if (weekVal==3)
	            msg1="星期三"; 
	    else if (weekVal==4)
	            msg1="星期四"; 
	    else if (weekVal==5)
	            msg1="星期五"; 
	    else if (weekVal==6)
	            msg1="星期六"; 

	   document.write(yy+"年"+mt+"月"+dd+"日 "+msg1);
	}

	var flasher = false;

	function updateTime() { 
	var now = new Date(); 
	var theHour = now.getHours(); 
	var theMin = now.getMinutes();
	var theSec = now.getSeconds();
	if (theHour<10)
	{
		theHour="0"+theHour
	}
	if(theMin<10)
	{
		theMin="0"+theMin
	}
	if(theSec<10)
	{
		theSec="0"+theSec
	}
	var theTime = theHour + ":"+theMin+":"+theSec;
	flasher = !flasher;
	lblTime.innerHTML = theTime; 
	// recursively call this function every second to keep timer going 
	timerID = setTimeout("updateTime()",1000);
	} 	