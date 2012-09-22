admin.menu = {
    
    see: function(){
   	    admin.urls.hash("");
    	admin.pages.active = false;
		admin.edit.deactive();
		admin.menu.close_sub_menu();
		admin.panels.close_all();
    },
    
    close_sub_menu: function(){
    	$("#wa_toolbar_menu .sub_menu .content").hide('fade');
    	$("#wa_toolbar_menu .sub_menu").removeClass('open');
    },
    
};

/*
 * Mise à jours
 */

/* This function activate selected effet in admin_tool_bar */
$(document).ready(function(){
	
	
	$("#wa_toolbar_menu li a").click(function(){
		
		var button = $(this);
		
		/* If user click on an LI in a submenu */
		if ( $(this).parents('.sub_menu').length == 1) {
			button = $(this).parents('.sub_menu'); /* get sub_menu dom object*/
			
			admin.edit.deactive();
			
			/* Check submenu if need to open or close it */
			if(button.hasClass('open')){
				button.removeClass('open');
				button.children('.content').hide('fade', {duration: 200});
			}else{
				$(".sub_menu").removeClass('open');
				$(".sub_menu").children('.content').hide('fade', {duration: 200});
				button.children('.content').show('fade', {duration: 200});
				button.addClass('open');
			}
			
			if($(this).parents('.content').length == 1){
				$("#wa_toolbar_menu li").removeClass("selected");
				button.addClass('selected');
				button.children(".content").hide('fade');
			}else{
				if(!button.hasClass('selected')){
					$("#wa_toolbar_menu li").removeClass("selected");
					button.addClass('selected');
				}else{
					$("#wa_toolbar_menu li").removeClass("selected");
					$("#wa_toolbar_menu li.preview").addClass('selected');
				}
			}
		}else{
			button = button.parent();
			
			if(button.hasClass('sub_menu') && button.hasClass('selected')){
				
			}else{
				if(button.hasClass('selected')){
					$("#wa_toolbar_menu li").removeClass("selected");
					$("#wa_toolbar_menu li.preview").addClass('selected');
				}else{
					$("#wa_toolbar_menu li").removeClass("selected");
					button.addClass('selected');
				}
			}
			
		
		}
	});
});
