function getWorkAreaObj()  //获得框架的工作区对象
{
	if(document.all){  //IE
		return top.frames['mainFrame'].document.frames['center'].document.frames['workarea']
	}else{
		return document.parentWindow.parent.getElementById('mainFrame').getElementById('center').getElementById('workarea')
	}
	
}

function navigateTo(url)  //菜单导航
{
	getWorkAreaObj().location=url
}