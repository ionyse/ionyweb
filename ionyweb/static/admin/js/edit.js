admin.edit = {
    
    is_active: false, // Precise if edition mode is activate or not
    header: false, // If user is editing the header
    content: false, // if use is editin the content
    footer: false, // If user is editing the footer
    
    active: function(){
	/*
	 * We start the editing mode. Display the content and change is_active
	 * to keep in memory the current status
	 */
	// If edition menu is disabled, we activate it
   	if(this.is_active){
   			
    	    this.deactive();
    	    
    	}else{
    	    // First step, we close all panels of the administration
    	    admin.urls.hash("/content");
    	    

    	    admin.panels.close_all();
    	    admin.menu.close_sub_menu();
    	    admin.messages.refresh_help_text_bubble();
    	    this.is_active = true; // Change current statue
    	    this.edit_content();
    	    
    	}
    },
    
    deactive: function(){
    	/*
    	 * We disable the edition mode. Need to hide each administration element.
    	 */
    	if(this.is_active){
		    // We close all menu just to be sure.
		    admin.panels.close_all();
		    // Hide structure which is before each layout and allow user to change layout
		    $(".wa_placeholder_structure").hide('fast');
		    
		    if(this.content){
				this.edit_content();
		    }
		    if(this.header){
				this.edit_header();
		    }
		    if(this.footer){
				this.edit_footer();
		    }
    	    this.is_active = false;
    	    admin.urls.hash("");
    	}
    },
    
    edit_content: function(){
    	if (this.is_active){
    	    
    	    if(this.header){
    		this.edit_header();	
    	    }
    	    if(this.footer){
    		this.edit_footer();
    	    }
    	    
    	    if(this.content){
		// We disable drag and drop sortable for content menu
    		// Disabled because created some trouble with drag and drop if contant display then hide then display
    		$(".placeholder").sortable( "disable" );
    		
    		// Enable selection for placeholder
		$(".placeholder").enableSelection();
		// Remove CSS for the placeholder content
		$(".placeholder").removeClass('wa_placeholder');
		// Hide menu in plugins like Move, edit or del
		// $(".wa_plugin_content").hide('fast');
		// Hide structure which is before each layout and allow user to change layout
		// $(".wa_placeholder_structure").hide('fast');
        // We hide the placeholder default
        $("#placeholder-default").hide('fast');
                
		// hide placeholder-default
		$("#default-placeholder").hide('fast');
        // We hide the placeholder clipboard
        $("#clipboard-placeholder").hide('fast');


		this.content = false;
		this.clipboard.deactive();

		// Hide ADMIN WIDGET
		$(".widget .wa_plugin_widget").hide('fast');
		// Hide admin actions object
		$(".wa_actions_object_widget").hide('fast');

	    }else{
		
		// We add wa_placeholder to add CSS style to placeholder (white style)
		$(".placeholder").addClass('wa_placeholder');

		// We show the placeholder default
		$("#default-placeholder").show('fast');
		// We show the placeholder clipboard
		$("#clipboard-placeholder").show('fast');
		// structure is before each layout and allow user to change layout
		$(".wa_placeholder_structure").show('fast');
		// We show placeholder widget, which define each placeholder in a layout
		$(".placeholder .wa_placeholder_widget").show('fast');
		
		this.clipboard.active();

		// SHOW ADMIN WIDGET
		$(".widget .wa_plugin_widget").show('fast');
		// Show actions objects widget
		$(".wa_actions_object_widget").show('fast');

		// wa_plugin_content display menu of each plugin (like move, edit, delete)
		// $(".wa_plugin_content").show('fast');
		// Active sortable on element in placeholder, not in placeholder-header
		// or placeholder-footer
		
		
		$(".placeholder").sortable({
		    items: '.placeholder-container',
		    handle: '.sortable_click',
		    connectWith: '.placeholder',
		    tolerance: 'pointer', 
		    opacity: 0.6,
		    forcePlaceholderSize:true,
		    placeholder: 'ui-state-highlight',
		    start:function(event, ui) {
		    	ui.item.find('[rel=tooltip]').tooltip('hide');
		    },
		    stop: function(event, ui) { 
	
				var cancel = false;
				var msg = gettext("You can't move this item in this placeholder.");
	
				item_id = ui.item.attr('id');
				placeholder_id = ui.item.parent('.placeholder').attr('id');
				
				
				if(placeholder_id == "default-placeholder"){
				    cancel = true;
				    console.log(gettext("Items can not be moved in the default placeholder !"));
				}
				
				// We disable move if the app go into the clipboard
				if(item_id.split('-')[0] == 'app' &&
				   placeholder_id == 'clipboard-placeholder'){
				    cancel=true;
				    msg = gettext("The App Page can not be moved in the clipboard !");
				}
				
				if(!cancel){
				    admin.POST({
					url: '/wa/plugin-page-relation/',
					data: {
					    placeholder_id: placeholder_id,
					    plugins_order: ui.item.parent(".placeholder").sortable('toArray'),
					},
					statusCode: {
					    200: function(json) {
						admin.messages.alert(json.msg, 400);
					    },
					    400: function(json) {
						admin.messages.error(json.msg, 800);
					    }
					}
				    });	
				}else{
				    console.log('Illegal Move !!');
				    $(this).sortable('cancel');
				    // Show message
				    admin.messages.error(msg);
				}
		    }
		});
		
		// If has been destroyed of disable previously, need to be reactivate
		$(".placeholder").sortable( "enable" );
		
		// We disable selection in .placeholder because if an element is selected drag&drop doesn't work.
		$(".placeholder").disableSelection();
		this.content = true;
	    }    		
    	    
	}
    },
    
    edit_header: function(){
    	// Si edition est actif, on ne fait rien.
    	if (this.is_active){
    	    // If we are already editing header, we need to disable this action.
    	    if(this.header){
    		// Disable sortable on plugin (to change order)
		$(".placeholder-header").sortable( "destroy" );
		// Enable selection because no more drag&drop
		$(".placeholder-header").enableSelection();
		// Remose CSS of placeholder
		$(".placeholder-header").removeClass('wa_placeholder');
		// Hide placeholder widget.
		$(".placeholder-header .wa_placeholder_widget").hide('fast');    			
		this.header = false;
    	    }else{
	    	
	    	// If not header and footer, means we are editing content.
	    	if(this.content){
	    	    this.edit_content();
	    	}
	    	// If user is editing footer, we disable it.
	    	if(this.footer){
	    	    this.edit_footer();
	    	}
	    	// We then show widgets in header
		$(".placeholder-header .wa_placeholder_widget").show('fast');
		// Add CSS style
		$(".placeholder-header").addClass('wa_placeholder');
		// Activate sortable effect
		$(".placeholder-header").sortable({
		    items: '.placeholder-container',
		    handle: '.sortable_click',
		    connectWith: '.placeholder-header',
		    tolerance: 'pointer', 
		    opacity: 0.6,
		    forcePlaceholderSize:true,
		    placeholder: 'ui-state-highlight',
		    start:function(event, ui) {
		    	ui.item.find('[rel=tooltip]').tooltip('hide');
		    },
		    stop: function(event, ui) {
				admin.POST({
				    url: '/wa/plugin-page-relation/',
				    data: {
					placeholder: ui.item.parent(".placeholder-header").attr("id"),
					placeholder_order: ui.item.parent(".placeholder-header").sortable('toArray'),
				    },
				    statusCode: {
					200: function(json) {
					    admin.messages.alert(json.msg, 400);
					},
					400: function(json) {
					    admin.messages.error(json.msg, 800);
					}
				    }
				});	
		    }
		});
		// Disable selection in some case of drag&drop
		$(".placeholder-header").disableSelection();
		
	    	this.header = true;
    	    }
    	    
    	}
    },
    
    edit_footer: function(){
    	// Si edition est actif, on ne fait rien.
    	if (this.is_active){
    	    // If we are already editing header, we need to disable this action.
    	    if(this.footer){
    		// Disable sortable on plugin (to change order)
		$(".placeholder-footer").sortable( "destroy" );
		// Enable selection because no more drag&drop
		$(".placeholder-footer").enableSelection();
		// Remose CSS of placeholder
		$(".placeholder-footer").removeClass('wa_placeholder');
		// Hide placeholder widget.
		$(".placeholder-footer .wa_placeholder_widget").hide('fast');    			
		this.footer = false;
    	    }else{
	    	
	    	// If not header and footer, means we are editing content.
	    	if(this.content){
	    	    this.edit_content();
	    	}
	    	// If user is editing footer, we disable it.
	    	if(this.header){
	    	    this.edit_header();
	    	}
	    	
	    	// We then show widgets in header
		$(".placeholder-footer .wa_placeholder_widget").show('fast');
		// Add CSS style
		$(".placeholder-footer").addClass('wa_placeholder');
		// Activate sortable effect
		$(".placeholder-footer").sortable({
		    items: '.placeholder-container',
		    handle: '.sortable_click',
		    connectWith: '.placeholder-footer',
		    tolerance: 'pointer', 
		    opacity: 0.6,
		    forcePlaceholderSize:true,
		    placeholder: 'ui-state-highlight',
		    start:function(event, ui) {
		    	ui.item.find('[rel=tooltip]').tooltip('hide');
		    },
		    stop: function(event, ui) { 
			/*$.ajax({
			  type: 'POST',
			  url: '/wa/plugin-page-relation/',
			  data: {
			  placeholder: ui.item.parent(".placeholder").attr("id"),
			  placeholder_order: ui.item.parent(".placeholder").sortable('toArray'),
			  },
			  statusCode: {
			  200: function(json) {
			  admin.messages.alert(json.msg, 400);
			  },
			  400: function(json) {
			  admin.messages.error(json.msg, 800);
			  }
			  }
			  });	*/
		    }
		});
		// Disable selection in some case of drag&drop
		$(".placeholder-footer").disableSelection();
		
	    	this.footer = true;
    	    }
    	    
    	}
    },
    
    refresh: function(){
		if(this.is_active){
		    
		    this.footer = false;
		    this.header = false;
		    this.content = false;
		    
		    this.edit_content();
		    
		}
    },

    settings: function(){
		admin.messages.error('Modifier les settings de l\'admin');
		admin.menu.edit_hide();
    },
    
    clipboard: {
    	active: function(){
    	    
    	    $("#clipboard-placeholder .wa_placeholder_widget").click(function(){
    		//$(this).css('left','0px');
    		if($("#clipboard-placeholder").css('left') == '0px'){
    		    $("#clipboard-placeholder").animate({left: '-250px'},100);
    		}else{
    		    $("#clipboard-placeholder").animate({left: '0px'},100);
    		}
    		
    	    });
    	    
    	},
    	deactive: function(){
    	    
    	    $("#clipboard-placeholder .wa_placeholder_widget").unbind('click');
    	    
    	}
    }
};