admin.plugin_blog_entries = {

	edit_entries : function(relation_id) {
		admin.GET({
			url : '/wa/action/' + relation_id + '/entrylink_list/',
		});
	},

	edit_entries_order : function(relation_id) {
		admin.GET({
			url : '/wa/action/' + relation_id + '/entires_order/',
			statusCode : {
				200 : function(json) {
					admin.panels.display('center', json.html);
					// Start sortable
					$("#links-ordering-container").sortable();
					$("#links-ordering-container").disableSelection();
				}
			}
		});
	},
	
	save_entries_order : function(relation_id) {
		orders = $('#links-ordering-container li').map(function() {
			return this.id;
		}).get();

		console.log(orders);

		admin.POST({
			url : '/wa/action/' + relation_id + '/entires_order/',
			data : {
				links_id : orders,
			},
			statusCode : {
				200 : function(json) {
					// Display message
					if(json.msg != undefined) {
						admin.messages.alert(json.msg);
					}
					// Remove selection
					admin.plugin_blog_entries.cancel_blog_entries_order();
					if(json.placeholder_type == "header") {
						admin.pages.refresh_header(json.html);
					} else if(json.placeholder_type == "footer") {
						admin.pages.refresh_footer(json.html);
					} else if(json.placeholder_type == "content") {
						admin.pages.refresh_content(json.html);
					} else if(json.placeholder_type == "widget") {
						$("#" + json.html_id).html(json.html);
						admin.edit.refresh();
					}
				},
			}
		});
	},
	
	cancel_blog_entries_order : function() {
		// We close panels
		admin.panels.close_all();
		// We disable sortable for links
		$("#links-ordering-container").sortable("destroy");
	}
}