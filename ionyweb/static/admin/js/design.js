admin.design= {
	styles: function(id){
		if(id === undefined){
			ajax_url = '/wa/design/';
		}else{
			ajax_url = '/wa/design/'+id+'/';
		}
		
		admin.GET({
			url : ajax_url,
			statusCode : {
				200 : function(json) {						
					admin.urls.hash('/themes/styles/!/'+json.current);							
					admin.panels.display('bottom_large', json.html);
				},
			}
		});
	},
	list: function(){
		admin.GET({
			url : '/wa/designs/',
			statusCode : {
				200 : function(json) {								
					admin.urls.hash('/themes');
					admin.panels.display('bottom_large', json.html);
				},
			}
		});
	},
	preview: function(id){
		
	},
	change: function(slug, csrf_token){
		admin.POST({
			url : '/wa/design/list/',
			data : {
				'theme_slug' : slug,
				'csrfmiddlewaretoken' : csrf_token,
			},
			statusCode : {
				200 : function(json) {
					window.location.reload();
				},
			},
		});
	},
	custom: function(){
		
	}
};
