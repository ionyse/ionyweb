admin.layouts = {
    list: function(layout_section_slug){
	if(!layout_section_slug) { return false; }
	admin.GET({
	    url: '/wa/layouts/',
	    data: {'layout_section_slug': layout_section_slug},
	    statusCode: {
		200: function(json) {
		    admin.panels.display('bottom',json.html);			    
		},
	    }
	});
    },
    preview: function(layout_template_slug, layout_section_slug, csrf_token){
	if(layout_template_slug && layout_section_slug && csrf_token){
	    // Get infos for default refresh
	    // list of plugin id in current default
	    var plugin_relation_default = new Array();
	    var plugin_relation_default_placeholder = new Array();
	    $('#default-placeholder .placeholder-container').each(function(){
		var current_obj = $(this);
		plugin_relation_default.push(current_obj.attr('id'));
		plugin_relation_default_placeholder.push(current_obj.attr('data-placeholder-slug'));
	    });
	    admin.GET({
		url: '/wa/layout/',
		data: {
		    layout_template_slug : layout_template_slug,
		    layout_section_slug: layout_section_slug,
		    plugin_relation_default: plugin_relation_default,
		    plugin_relation_default_placeholder: plugin_relation_default_placeholder
		},
		statusCode: {
		    200: function(json) {
			// Refresh default and layout
			admin.pages.refresh_layout_and_default_with_html(json.layout_section_slug,
									 json.html,
									 json.default_to_add,
									 json.default_to_delete);
			// Refresh admin
			admin.edit.refresh();
			// Display confirm message
			admin.messages.confirm(gettext('Do you want save this layout ?'), function(){
			    admin.layouts.edit(layout_template_slug, layout_section_slug, csrf_token);
			}, function(){
			    admin.pages.refresh_layout(layout_section_slug);
			    admin.edit.refresh();
			});
		    },
		},
	    });
	}
    },
    edit: function(layout_template_slug, layout_section_slug, csrf_token){
	if(layout_template_slug && layout_section_slug && csrf_token){
	    admin.POST({
		url: '/wa/layout/',
		data: {
		    layout_template_slug : layout_template_slug,
		    layout_section_slug: layout_section_slug,
		},
		statusCode: {
		    200: function(json) {
			admin.messages.alert(json.msg);
			admin.panels.close('bottom');
		    },
		},
	    });	
	}
    }
};
