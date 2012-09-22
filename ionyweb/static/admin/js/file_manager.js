// This is use to display popup message (Growl style) to the user.

admin.file_manager = {
	current_directory: 0,
	selector_activate: false,
	tinymce_activate: false,
	input_id: null,
	toggle: function(){
		if($('#wa_file_manager').is(":visible")){
			admin.panels.close('full');
			$("#wa_toolbar_menu li").removeClass("selected");
			$("#wa_toolbar_menu li.preview").addClass('selected');
			admin.urls.hash('');
		}else{
			admin.GET({
				url : '/wa/file_manager/',
				statusCode : {
					200 : function(json) {
						admin.urls.hash('/file_manager');
						admin.panels.display('full', json.html);
						admin.file_manager.refresh_draggable_sortable_file();
					},
				}
			});
		}
	},
	selector: {
		// Use to select a file in a Django FileField
		open: function(name){
			admin.file_manager.input_id = name;
			admin.GET({
				url : '/wa/file_manager/',
				data: {'selector': true},
				statusCode : {
					200 : function(json) {
						$("#wa_panel_file_manager_selector .content").html(json.html);
						$("#wa_panel_file_manager_selector").show('fade');
						admin.file_manager.selector_activate = true;
					},
				}
			});
		},
		close: function(){
			$("#wa_panel_file_manager_selector").hide('fade', function(){
				$("#wa_panel_file_manager_selector .content").html('');
			});
			admin.file_manager.selector_activate = false;
			admin.file_manager.tinymce_activate = false;
		},
		send: function(path){
			if(admin.file_manager.tinymce_activate){
				tinyMCE.activeEditor.execCommand('mceInsertContent', false, "<img src='"+path+"' alt='' />");
			}else{
				$("#"+admin.file_manager.input_id).val(path);
			}
			admin.file_manager.selector.close();
		},
	},
	tinymce: {
		// Use to select a file in a Django FileField
		open: function(name){
			admin.file_manager.tinymce_activate = true;
			admin.file_manager.selector.open(name);
		},
	},
	upload: {
		get: function(){
			admin.GET({
				url : '/wa/file_manager/upload/',
				statusCode : {
					200 : function(json) {
						admin.file_manager.toggle_right_colomn(json.html);
						
					},
				}
			});
			
			
		}
	},
	directory: {
		get: function(id){
			if(id === undefined){
				if(admin.file_manager.current_directory){
					id = admin.file_manager.current_directory;
				}else{
					id = 0;
				}
			}
			admin.GET({
				url : '/wa/file_manager/dir/'+id+'/',
				statusCode : {
					200 : function(json) {
						admin.file_manager.refresh_file_list(json.html);
						admin.file_manager.current_directory = id;
						admin.file_manager.directory.refresh_selected();
					},
				}
			});
		},
		put: function(id){
			if(id === undefined){
				if(admin.file_manager.current_directory){
					id = admin.file_manager.current_directory;
				}else{
					id = 0;
				}
			}
			admin.PUT({
				url : '/wa/file_manager/dir/'+id+'/',
				statusCode : {
					200 : function(json) {
						admin.file_manager.refresh_file_list(json.files_list);
						admin.file_manager.refresh_directory_list(json.directory_list);
						admin.file_manager.directory.rename(json.id);
						admin.file_manager.directory.refresh_selected();
					},
				}
			});
		},
		remove: function(id){
			admin.DELETE({
				url : '/wa/file_manager/dir/'+id+'/',
				statusCode : {
					200 : function(json) {
						admin.file_manager.refresh_directory_list(json.directory_list);
						admin.file_manager.directory.refresh_selected();
						$('#wa_file_manager .quota').html(json.quota);
						$("#dir-"+id).hide(function(){
							$(this).remove();
						});
					},
				}
			});
		},
		rename: function(id){
			tmp_onClick_over = $("#dir-"+id+" a:first-child").attr('onClick');
			$("#dir-"+id+" a:first-child").removeAttr('onClick');
			
			var label =  $("#dir-"+id+" .name .label_js");
			var tmp = label.html();
			label.html("<form><input type='text' name='dir-label' /></form>");
			var input = $("#dir-"+id+" .name .label_js form input");
			input.val(tmp);
			var form = $("#dir-"+id+" .name .label_js form");
			$("#dir-"+id+" .name .label_js form").submit(function(){
				label.unbind('focusout');
				
				admin.POST({
					url : '/wa/file_manager/dir/'+id+'/',
					data: {'name': input.val()},
					statusCode : {
						200 : function(json) {
							label.html(input.val());
				 			$("#dir-"+id+" a:first-child").attr('onClick', tmp_onClick_over);
							admin.file_manager.refresh_file_list(json.files_list);
							admin.file_manager.refresh_directory_list(json.directory_list);
						},
					}
				});
				return false;
			});
			input.focusout(function(){
				label.html(tmp);
				 $("#dir-"+id+" a:first-child").attr('onClick', tmp_onClick_over);
			});
			input.focus();
		},
		refresh_selected: function(){
			$("#wa_file_manager_list .directory_list .selected").removeClass('selected');
			$("#wa_file_manager_list .directory_list #directory-"+admin.file_manager.current_directory).addClass('selected');
		}
	},
	file: {
		get: function(id){
			if($("#"+id).hasClass('selected')){
				$("#"+id).removeClass('selected')
				admin.file_manager.toggle_right_colomn();
			}else{
				$("#"+id).parent().children('.selected').removeClass('selected');
				$("#"+id).addClass('selected');
				admin.GET({
					url : '/wa/file_manager/file/'+id+'/',
					data: {'selector': admin.file_manager.selector_activate},
					statusCode : {
						200 : function(json) {
							admin.file_manager.toggle_right_colomn(json.html);
							admin.lightbox.init();
						},
					}
				});
			}
		},
		remove: function(id){
			admin.DELETE({
				url : '/wa/file_manager/file/'+id+'/',
				statusCode : {
					200 : function(json) {
						admin.file_manager.toggle_right_colomn();
						$('#wa_file_manager .quota').html(json.quota);
						$("#"+id).hide(function(){
							$(this).remove();
						});
					},
				}
			});
		},
		get_thumbnail: function(path, size){
			admin.GET({
					url : '/wa/file_manager/thumbnail/',
					data: { 'path': path,
							'size': size},
					statusCode : {
						200 : function(json) {
							admin.file_manager.selector.send(json.thumbnail);
						},
					}
				});
		},
		rename: function(id){
			tmp_onClick_over = $("#"+id+" a:first-child").attr('onClick');
			$("#"+id+" a:first-child").removeAttr('onClick');
			var label =  $("#"+id+" .name .label_js");
			var tmp = label.html();
			label.html("<form><input type='text' name='label' /></form>");
			var input = $("#"+id+" .name .label_js form input");
			input.val(tmp);
			var form = $("#"+id+" .name .label_js form");
			
			$("#"+id+" .name .label_js form").submit(function(){
				label.unbind('focusout');
				
				admin.POST({
					url : '/wa/file_manager/file/'+id+'/',
					data: {'name': input.val()},
					statusCode : {
						200 : function(json) {
							label.html(input.val());
							$("#"+id+" a:first-child").attr('onClick', tmp_onClick_over);
							admin.file_manager.refresh_file_list(json.files_list);
						},
					}
				});
				return false;
			});
			input.focusout(function(){
				label.html(tmp);
				$("#"+id+" a:first-child").attr('onClick', tmp_onClick_over);
			});
			input.focus();
		},
	},
	toggle_quota: function(){
		if($('#wa_file_manager .quota').height() < 50){
			$('#wa_file_manager .quota').animate({
				height: '300px',
			});
			$('#wa_file_manager .list_directory').animate({
				bottom: '300px',
			});
		}else{
			$('#wa_file_manager .quota').animate({
				height: '30px',
			});
			
			$('#wa_file_manager .list_directory').animate({
				bottom: '30px',
			});
		}
	},
	refresh_file_list: function(html){
		$("#wa_file_manager_content .file_list").html(html);
		admin.file_manager.refresh_draggable_sortable_file();
	},
	refresh_directory_list: function(html){
		$("#wa_file_manager_list .directory_list").html(html);
		admin.file_manager.refresh_draggable_sortable_file();
	},
	refresh_draggable_sortable_file: function(){
		var tmp_onClick = ""
		$(".draggable").draggable({
			revert: 'invalid',
			zIndex: 2700,
			opacity: 0.6,
			distance: 10,
			start: function(event, ui){
				tmp_onClick = ui.helper.children("a").attr('onClick');
				ui.helper.children("a").removeAttr('onClick');
			},
			drag: function(event, ui){
				tmp_onClick = ui.helper.children("a").attr('onClick');
				ui.helper.children("a").removeAttr('onClick');
			},
			stop: function(event, ui){
				ui.helper.children("a").attr('onClick', tmp_onClick);
			}
		});
		
		$( ".droppable" ).droppable({
			accept: ".draggable",
			over: function( event, ui ) {
				tmp_onClick_over = $(this).children("a").attr('onClick');
				$(this).children("a").removeAttr('onClick');
			},
			out: function( event, ui) {
				$(this).children("a").attr('onClick', tmp_onClick_over);
			},
			drop: function( event, ui ) {
				$(this).children("a").attr('onClick', tmp_onClick_over);
				admin.POST({
					url : '/wa/file_manager/',
					data: {
						'drop': ui.draggable.attr('id'), 
						'in': $(this).attr('id'),
						'current': admin.file_manager.current_directory,
					},
					statusCode : {
						200 : function(json) {
							ui.draggable.remove();
							$("#wa_file_manager_list .directory_list").html(json.directory_list);
						},
					}
				});
			}
		});
	},
	toggle_right_colomn: function(html){
		if(html == undefined){
			if($("#wa_file_manager_right").is(":visible")){
				$('#wa_file_manager_right').animate({
					width: '0px',
				}, function(){ $('#wa_file_manager_right').hide().html(""); });
				$('#wa_file_manager_content').animate({
					right: '0px',
				});
			}
		}else{
			if($("#wa_file_manager_right").is(":visible"))
			{
				$('#wa_file_manager_right').html(html);	
			}else{
				$('#wa_file_manager_right').html(html).show();

				$('#wa_file_manager_right').animate({
					width: '300px',
				});
				$('#wa_file_manager_content').animate({
					right: '300px',
				});
			}
		}
	},
	display_mode: function(mode){
		admin.POST({
			url : '/wa/file_manager/display/',
			data: {'mode': mode},
			statusCode : {
				200 : function(json) {
					admin.file_manager.directory.get();
				},
				404 : function(json) {
					
				}
			}
		});
	}
};
