admin.plugins = {
	placeholder: null,
    list : function(placeholder_id) {
    	admin.urls.hash('/plugins/add/!/'+placeholder_id);
    	admin.plugins.placeholder = placeholder_id
	    admin.GET({
			url : '/wa/plugins/',
			statusCode : {
			    200 : function(json) {
			    	admin.panels.display('full', json.html);
			    },
			}
	    });

    },
    list_by_category: function(slug){
    	admin.GET({
			url : '/wa/plugins/category/'+slug+'/',
			statusCode : {
			    200 : function(json) {
			    	$("#plugins_categorieslist").html(json.html);
			    },
			}
	    });
    	$("#plugins_categories li").removeClass('selected');
    	$("#plugins_categories ."+slug).addClass('selected');
    	$("#plugins_description").html("");
    },
    description: function(plugin_id){
    	admin.GET({
			url : '/wa/plugins/description/'+plugin_id+'/',
			statusCode : {
			    200 : function(json) {
			    	$("#plugins_description").html(json.html);
			    },
			}
	    });
    	$("#plugins_categorieslist li").removeClass('selected');
    	$("#plugins_categorieslist .plugin_"+plugin_id).addClass('selected');
    },
    add : function(id) {
		admin.GET({
			url : '/wa/plugin/',
			data : {
				'placeholder_id' : admin.plugins.placeholder,
				'plugin_type' : id
			}
		});
    },
    create : function() {
		list = admin.serialize('#plugin_form_form');

		admin.PUT({
			url : '/wa/plugin/',
			data : list,
			statusCode : {
				200 : function(json) {
					admin.messages.alert(json.msg);
					admin.panels.close_all();
					$("head").append(json.medias);
					admin.pages.refresh_layout(json.layout_section_slug, json.html);
					admin.edit.refresh();
				}
			}
		});
    },
    remove : function(id) {
		admin.messages.confirm(gettext('Are you sure you want to delete this plugin ?'), function() {
		    admin.DELETE({
			url : '/wa/plugin/' + id + '/',
			data : {
			    'plugin-id' : id
			},
			statusCode : {
			    200 : function(json) {
				admin.messages.alert(json.msg);
				$('#' + id).hide('slow', function() {
				    $('#' + id).remove();
				});
			    }
			}
		    });
		});
    },
    edit : function(id) {
    	admin.urls.hash('/plugins/edit/!/'+id);
		admin.GET({
		    url : '/wa/plugin/' + id + '/'
		});
    },
    save : function() {
		list = admin.serialize('#plugin_form_form');
		id = $('#plugin_form_form input[name=id]').attr('value');

		admin.POST({
			url : '/wa/plugin/' + id + '/',
			data : list,
			statusCode : {
				200 : function(json) {
					admin.messages.alert(json.msg);
					admin.panels.close_all();
					admin.pages.refresh_layout(json.layout_section_slug, json.html);
					admin.edit.refresh();
				}
			}
	    });
    }
};
