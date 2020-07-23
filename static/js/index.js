//index.js

function removeNotification(el){
	el.parentNode.parentNode.removeChild(el.parentNode)
}

var offsetHeight = document.getElementsByClassName('navWrapper')[0].offsetHeight + document.getElementsByClassName('messages')[0].offsetHeight

function miniShop(){
	offsetHeight = document.getElementsByClassName('navWrapper')[0].offsetHeight + document.getElementsByClassName('messages')[0].offsetHeight; //update offset height
	document.getElementById("miniShop").style.top = offsetHeight + 1 + "px";
	//^ here I determine the top offset for the mini shop via javascriwindow.innerHeightpt, because some devices would use different fonts, and plus it's easier on resizing

	document.getElementById("miniShop").style.display = "block";
	document.getElementById("new").classList.add("active");
	document.getElementsByTagName("html")[0].style.overflow = "hidden";
	document.getElementsByTagName("body")[0].style.overflow = "unset";

	document.getElementById("miniShop").style.maxHeight = "calc(100vh - " + offsetHeight + "px)";
	if(document.getElementById("miniShop").offsetHeight > window.innerHeight*0.60){ //if the height is greater than 60% of the window
		document.getElementById("miniShop").style.overflowY = "scroll";
	} else {document.getElementById("miniShop").style.overflowY = "unset";}
	//^here I determine the maxheigh of the minishop (until it starts scrolling), so that it works on mobile
}

function closeMiniShop(){
	document.getElementById("miniShop").style.display = "none";
	document.getElementById("new").classList.remove("active");
	document.getElementsByTagName("html")[0].style.overflow = "unset";
	document.getElementsByTagName("body")[0].style.overflow = "unset";
}

var body = document.getElementsByTagName("body")[0];
body.style.paddingBottom = document.getElementsByTagName("footer")[0].offsetHeight + "px";
//^ this gives space at the bottom for the footer


//accordion stuff
var acc = document.getElementsByClassName("accordion");
var i;
for (i = 0; i < acc.length; i++) {
	acc[i].addEventListener("click", function() {
		this.classList.toggle("active");
		var panel = this.nextElementSibling;
		if (panel.style.maxHeight) {
			panel.style.maxHeight = null;
		} else {
			panel.style.maxHeight = panel.scrollHeight + "px";
		}
	});
}