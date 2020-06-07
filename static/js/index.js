//index.js

function removeNotification(el){
	el.parentNode.parentNode.removeChild(el.parentNode)
}

function miniShop(){
	document.getElementById("miniShop").style.top = document.getElementsByClassName('navWrapper')[0].offsetHeight + 1 + "px";
	//^ here I determine the top offset for the mini shop via javascript, because some devices would use different fonts, and plus it's easier on resizing
	document.getElementById("miniShop").style.display = "block";
	document.getElementById("new").classList.add("active");
}

function closeMiniShop(){
	document.getElementById("miniShop").style.display = "none";
	document.getElementById("new").classList.remove("active");
}