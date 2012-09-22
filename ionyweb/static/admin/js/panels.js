admin.panels = {
	panel : ['bottom', 'bottom_large', 'center', 'left', 'right', 'full', 'menu', 'right_colomn', 'left_colomn', 'file_manager'],
	animation : {
		'bottom' : 'slide',
		'bottom_large' : 'slide',
		'center' : 'fade',
		'left' : 'fade',
		'right' : 'fade',
		'full' : 'fade',
		'menu' : 'slide',
		'right_colomn' : 'fade',
		'left_colomn' : 'slide',
		'file_manager': 'fade',
	},
	// Open a panel and display the HTML code
	display : function(type, html, callback) {
		admin.panels.close_others(type);
		admin.loading.hide();
		var selected_panel = $("#wa_panel_" + type);

		if(selected_panel.is(":visible")) {
			selected_panel.find(".content").html(html);
		} else {
			// Close submenu in panel
			admin.menu.close_sub_menu();
			// Change content and display the panel
			selected_panel.find(".content").html(html);
			selected_panel.show(admin.panels.animation[type]);
		    $("#wa_bg_panels").show();
		}
		// refresh help_text bubble on hover for button
		admin.messages.refresh_help_text_bubble();
	},
	change_content : function(type, html, callback) {
		$("#wa_panel_" + type).find(".content").html(html);
		// refresh help_text bubble on hover for button
		admin.messages.refresh_help_text_bubble();
	},
	// Close a panel, where type is in panels.panel
	close : function(type, callback) {
		var selected_panel = $("#wa_panel_" + type);
		selected_panel.hide(admin.panels.animation[type], function() {
			selected_panel.find(".content").html("");
			if(callback)
				callback();
		});
	    $("#wa_bg_panels").hide();
	        
	},
	// Close all panels in panels.panel and erase their content
	close_others : function(type) {
		admin.pages.active = false;
		for(var i = 0; i < admin.panels.panel.length; i++) {
			if(admin.panels.panel[i] != type) {
				if($("#wa_panel_" + admin.panels.panel[i]).is(":visible")) {
					admin.panels.close(admin.panels.panel[i]);
				}
			}
		}
	},
	close_all : function() {
		for(var i = 0; i < admin.panels.panel.length; i++) {
			if($("#wa_panel_" + admin.panels.panel[i]).is(":visible")) {
				admin.panels.close(admin.panels.panel[i]);
			}
		}
	},
};
