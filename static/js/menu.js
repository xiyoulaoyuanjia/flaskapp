$(function(){

var currentPage = location.pathname;//  获取当前页面的路径
var currentPageName = currentPage.substring(currentPage.lastIndexOf("/"));//获取"/"+当前文件名


var liMenus = $("#menu").children();//获取所有的菜单项

if (liMenus != null && liMenus.length > 0) {
	for (var i = 0; i < liMenus.length; i++) {
		if($(liMenus[i]).children().attr("href").toLowerCase() == currentPageName.toLowerCase()){
			
			$(liMenus[i]).attr("class", "active");
		}else if($(liMenus[i]).children().attr("href").toLowerCase() == "/" && currentPage.indexOf("/page") == 0){    
		// 加入对分页的支持
			$(liMenus[i]).attr("class", "active");
		}
	}

}



});
