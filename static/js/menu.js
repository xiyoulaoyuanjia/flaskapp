$(function(){

var currentPage = location.pathname;//  获取当前页面的路径
var currentPageName = currentPage.substring(currentPage.lastIndexOf("/"));//获取"/"+当前文件名


var liMenus = $("#menu").children();//获取所有的菜单项

if (liMenus != null && liMenus.length > 0) {
	for (var i = 0; i < liMenus.length; i++) {
		if($(liMenus[i]).children().attr("href").toLowerCase() == currentPageName.toLowerCase()){
			
			$(liMenus[i]).attr("class", "active");
		}
	}

}

function selectCurrentMenu(ulMenuId) {
    var currentPage = location.pathname;//  获取当前页面的路径
    var currentPageName = currentPage.substring(currentPage.lastIndexOf("/") + 1);//获取当前文件名
    var liMenus = $("#" + ulMenuId).children();//获取所有的菜单项
    //  遍历，匹配，选中
    if (liMenus != null && liMenus.length > 0) {
        for (var i = 0; i < liMenus.length; i++) {
            if ($(liMenus[i]).attr("colhref").indexOf(currentPageName) >= 0) {
                $(liMenus[i]).attr("class", "li_current");
                break;
            }
        }
    }
}

});
