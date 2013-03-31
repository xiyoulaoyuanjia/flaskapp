
// 同步选择标志 默认为0 ---不同步
var SynchronousFlag =0;

var editor=0;
var preview=0;

function onresize() {
    var view_h = $(this).height(); 
    var view_w = $(this).width(); 
    $('#container').height(view_h - $('#bar').height() - 1);
    $('#container').children('.pane')
        .height(view_h - $('#bar').height - 5);
    $('#input').width(parseInt(view_w/2)+10)
    $('#preview_pane').width(parseInt(view_w/2)-20);
}


function InitAce(){
   editor = ace.edit("input");
   editor.setTheme("ace/theme/chrome");
   //   editor.setTheme("ace/theme/makedown");
  
}


function SynchronousClick(){
  InitAce();
  if(SynchronousFlag){
    if(editor){
	       preview.html(markdown.toHTML(editor.getValue()));
	    //document.getElementById('iframe').src="data:text/html;charset=utf-8,"+markdown.toHTML(editor.getValue());	      
	    }
     editor.getSession().on('change', function(e) {
	    if(editor){
	       preview.html(markdown.toHTML(editor.getValue()));
	    //document.getElementById('iframe').src="data:text/html;charset=utf-8,"+markdown.toHTML(editor.getValue());	      
	    }
	   
	});
     SynchronousFlag--;
  }else{
    editor=0;
    preview.html("");
    SynchronousFlag++;
  }  
}

$(document).ready(function () {

    $(window).resize(function (event) {
        onresize();
    });
    onresize();
   
    InitAce();
    preview = $("#preview"); 

    SynchronousFlag=1;
   
    $('#Synchronous_button').click(function () {
	
	SynchronousClick();
        return false;
    });
   
});	

 



