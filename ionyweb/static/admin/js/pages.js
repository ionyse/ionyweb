admin.pages = {
	active : false,
	active_sortable : function() {
		$('ol.move_liste_pages').nestedSortable({
			disableNesting : 'no-nest',
			forcePlaceholderSize : true,
			handle : '.move_grip',
			helper : 'clone',
			items : 'li',
			opacity : .6,
			placeholder : 'sortable_placeholder',
			errorClass : 'sortable_placeholder_error',
			revert : 250,
			scroll : true,
			scrollSensitivity : 40,
			scrollSpeed : 40,
			tabSize : 25,
			tolerance : 'pointer',
			toleranceElement : '> div',
			stop : function(event, ui) {
				var id = $(ui.item).attr('id');
				// gets id
				var item = $("#" + id);
				var parent = item.parents('li').attr('id');
				// gets id du père
				var previous = item.prev().attr('id');
				// gets id du left
				var next = item.next().attr('id');
				// gets id du right
				admin.POST({
					url : '/wa/page/' + id + '/',
					data : {
						'move' : 'move',
						'parent' : parent,
						'previous' : previous,
						'next' : next
					},
					statusCode : {
						200 : function(json) {
							if(json.msg) {
								admin.messages.alert(json.msg);
							}
							if(json.navigation_html) {
								admin.pages.refresh_navigation(json.navigation_html);
							}
							if(json.manager_html) {
								admin.panels.change_content('full', json.manager_html);
							}
							admin.pages.active_sortable();
						},
						203 : function(json) {
							admin.messages.error(json.msg);
						}
					}
				});
			},
		});
	},
	list : function() {
		if(this.active == true) {
			admin.panels.close('full');
			this.active = false;
		} else {
			admin.edit.deactive();
			//admin.urls.hash("/page_manager");
			admin.loading.show(function() {
				admin.GET({
					url : '/wa/pages/',
					statusCode : {
						200 : function(json) {
							admin.loading.hide();
							admin.panels.display('full', json.html);
							admin.pages.active = true;
							admin.pages.active_sortable();
							$("#wa_toolbar_menu li").removeClass("selected");
							$("#wa_toolbar_menu li.page_manager").addClass('selected');
						},
					}
				});
			});
		}
	},
	add : function() {
		admin.PUT({
			url : '/wa/page/',
			statusCode : {
				200 : function(json) {
					this.active = false;
					admin.panels.display('center', json.html);
				},
			}
		});
	},
	create_form : function(parent) {
		if(parent == undefined) {
			parent = 0;
		}
		admin.GET({
			url : '/wa/page/',
			data : {
				'parent' : parent
			},
			statusCode : {
				200 : function(json) {
					this.active = false;
					admin.panels.display('center', json.html);
				},
			}
		});
	},
	create : function() {
		list = admin.serialize('#page_form_form');

		admin.PUT({
			url : '/wa/page/',
			data : list
		});
	},
	edit_form : function(id) {
		admin.GET({
			url : '/wa/page/' + id + '/',
			statusCode : {
				200 : function(json) {
					this.active = false;
					//admin.urls.hash('/pages/edit/!/'+id);
					admin.panels.display('center', json.html);
				},
				203 : function(json) {
					admin.messages.error(json.msg);
					admin.panels.change_content('center', json.html);
				}
			}
		});
	},
	edit : function(id) {
		list = admin.serialize('#page_form_form');

		admin.POST({
			url : '/wa/page/' + id + '/',
			data : list,
			statusCode : {
				200 : function(json) {
					if(json.msg) {
						admin.messages.alert(json.msg);
					}
					if(json.navigation_html) {
						admin.pages.refresh_navigation(json.navigation_html);
					}
					if(json.page_html) {
						admin.pages.refresh_content(json.page_html);
					}
					admin.panels.close_all();
					//admin.pages.list();
				},
				203 : function(json) {
					admin.messages.error(json.msg);
					admin.panels.change_content('center', json.html);
				}
			}
		});
	},
	remove : function(id) {
		admin.messages.confirm(gettext('Deleting the page :<br /><br />Be careful : the app and all plugins will be deleted.<br/><br />Are you sure you want to delete this page now?<br /><br />'), function() {
			admin.DELETE({
				url : '/wa/page/' + id + '/',
				statusCode : {
					200 : function(json) {
						if(json.msg) {
							admin.messages.alert(json.msg);
						}
						if(json.navigation_html) {
							admin.pages.refresh_navigation(json.navigation_html);
						}
						// Removing page in manager
						$("#" + json.id).hide('slow', function() {
							$("#" + json.id).remove();
						});
					},
					203 : function(json) {
						admin.messages.error(json.msg);
						admin.pages.list();
					}
				}
			});
		});
	},
	toggle_draft : function(id) {
		admin.POST({
			url : '/wa/page/' + id + '/',
			data : {
				"draft" : ""
			},
			statusCode : {
				200 : function(json) {
					admin.panels.change_content('full', json.html);
					if(json.navigation_html) {
						admin.pages.refresh_navigation(json.navigation_html);
						admin.pages.refresh_content();
					}
				},
				203 : function(json) {
					admin.messages.error(json.msg);
				}
			}
		});
	},
	duplicate : function(id) {
		admin.GET({
			url : '/wa/page/duplicate/' + id + '/',
			statusCode : {
				200 : function(json) {
					admin.panels.change_content('full', json.html);
				},
				203 : function(json) {
					admin.messages.error(json.msg);
				}
			}
		});
	},
	cancel_form : function() {
		this.active = false;
		admin.panels.close_all();
		admin.menu.see();
		$("#wa_toolbar_menu li").removeClass("selected");
		$("#wa_toolbar_menu li.preview").addClass('selected');
	},
	cancel_edit_form : function() {
		this.active = false;
		admin.panels.close_all();
		
		if($(".wa_placeholder_widget").is(':visible')){
			$("#wa_toolbar_menu li").removeClass("selected");
			$("#wa_toolbar_menu li.content").addClass('selected');
		}else{
			$("#wa_toolbar_menu li").removeClass("selected");
			$("#wa_toolbar_menu li.preview").addClass('selected');
		}
		//admin.pages.list();
	},
	refresh_header : function(html) {
		if(html == undefined) {
			// On fait une requete Ajax pour récupérer le contenu
			admin.GET({
				url : '/wa/website/header/',
				statusCode : {
					200 : function(json) {

						// On change le HTML
						$("#header").html(json.html);
						// On regarde si l'admin est activé et la réactualise.
						admin.edit.refresh();
					}
				}
			});
		} else {
			// On change le HTML
			$("#header").html(html);
			// On regarde si l'admin est activé et la réactualise.
			admin.edit.refresh();
		}
	},
	refresh_navigation : function(html) {
		if(html != undefined) {
			$("#nav").html(html);
			admin.edit.refresh();
		}
	},
	refresh_content : function(html) {
		if(html != undefined) {
			// On change le HTML
			$("#main-content").html(html);
			// On regarde si l'admin est activé et la réactualise.
			admin.edit.refresh();
		}

	},
	refresh_footer : function(html) {
		if(html == undefined) {
			// On fait une requete Ajax pour récupérer le contenu
			admin.GET({
				url : '/wa/website/footer/',
				statusCode : {
					200 : function(json) {
						// On change le HTML
						$("#footer").html(json.html);
						// On regarde si l'admin est activé et la réactualise.
						admin.edit.refresh();
					},
				}
			});
		} else {
			// On change le HTML
			$("#footer").html(html);
			// On regarde si l'admin est activé et la réactualise.
			admin.edit.refresh();
		}

	},
	refresh_layout : function(layout_section_slug, html) {
		if(!html) {
			admin.GET({
				url : '/wa/page/layout/',
				data : {
					layout_section_slug : layout_section_slug,
				},
				statusCode : {
					200 : function(json) {
						// On change le HTML
						$("#layout-" + layout_section_slug).html(json.html);
						// Refresh admin
						admin.edit.refresh();
					},
				}
			});
		} else {
			// Update html
			$('#layout-' + layout_section_slug).html(html);
		}
	},
	refresh_placeholder : function(placeholder_slug, html) {
		if(placeholder_slug && html) {
			$('#' + placeholder_slug).html(html);
		}
	},
	refresh_default : function(items_to_add, items_to_delete) {
		var default_container = $("#default-placeholder");
		for(item in items_to_add) {
			default_container.append(items_to_add[item]);
		}
		for(item in items_to_delete) {
			$("#" + items_to_delete[item]).remove();
		}
	},
	refresh_layout_and_default_with_html : function(layout_section_slug, html, default_add, default_delete) {
		admin.pages.refresh_default(default_add, default_delete);
		admin.pages.refresh_layout(layout_section_slug, html);
		admin.edit.refresh();
	},
};
