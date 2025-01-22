function redirect(){
	document.getElementById('background').classList.add('fade-out');
	setTimeout(function(){
		window.location.href = window.url;
	}, 800);
}

// 若检测到滚动事件，则执行redirect
window.onscroll = function(){
	redirect();
}