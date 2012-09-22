admin.settings = {
	more: function(){
		admin.GET({
			url : '/wa/website/versions/',
			statusCode : {
				200 : function(json) {			
					admin.urls.hash('/versions');								
					admin.panels.display('right_colomn', json.html);
				},
			}
		});
	},
	analytics: {
		get:  function(){
			admin.GET({
				url : '/wa/website/analytics/',
				statusCode : {
					200 : function(json) {			
						admin.urls.hash('/analytics');					
						admin.panels.display('center', json.html);
					},
				}
			});
		},
		post: function(){
			list = admin.serialize("#page_analytics_form");
			
			admin.POST({
				url : '/wa/website/analytics/',
				data : list,
				statusCode : {
					200 : function(json) {								
						admin.panels.close('center');
					},
					400 : function(json) {
						admin.messages.error(json.msg);
					},
				}
			});
		},
	},
	domains: {
		list:  function(){
			admin.GET({
				url : '/wa/website/domains/',
				statusCode : {
					200 : function(json) {			
						admin.urls.hash('/domains');								
						admin.panels.display('center', json.html);
					},
				}
			});
		},
		add:  function(){
			admin.GET({
				url : '/wa/website/domain/',
				statusCode : {
					200 : function(json) {		
						admin.urls.hash('/domains/add');							
						admin.panels.display('center', json.html);
					},
				}
			});
		},
		edit_form:  function(id){
			admin.GET({
				url : '/wa/website/domain/'+id+'/',
				statusCode : {
					200 : function(json) {								
						admin.panels.display('center', json.html);
					},
				}
			});
		},
		create:  function(){
			list = admin.serialize('#domain_form');
			admin.PUT({
				url : '/wa/website/domain/',
				data : list,
				statusCode : {
					200 : function(json) {		
						admin.messages.alert(json.msg);						
						admin.settings.domains.list();
					},
				}
			});
		},
		edit:  function(id){
			list = admin.serialize('#domain_form');
			admin.POST({
				url : '/wa/website/domain/'+id+'/',
				data : list,
				statusCode : {
					200 : function(json) {		
						admin.messages.alert(json.msg);						
						admin.settings.domains.list();
					},
				}
			});
		},
		set_primary:  function(id){
			admin.POST({
				url : '/wa/website/domain/'+id+'/',
				data : {'primary': ''}
			});
		},
		remove:  function(id){
			admin.messages.confirm(gettext('Deleting the domain :<br /><br />Are you sure that you want to delete this domain name now?'), function() {
				admin.DELETE({
					url : '/wa/website/domain/'+id+'/',
					statusCode : {
						200 : function(json) {
							if(json.msg) {
								admin.messages.alert(json.msg);					
								admin.settings.domains.list();
							}
						},
					}
				});
			});
		},
		cancel_form: function () {
			admin.settings.domains.list();
		}
	},
	referencement: {
		get:  function(){
			admin.GET({
				url : '/wa/website/referencement/',
				statusCode : {
					200 : function(json) {			
						admin.urls.hash('/seo');								
						admin.panels.display('center', json.html);
					},
				}
			});
		},
		post: function(){
			list = admin.serialize("#page_referencement_form");
			
			admin.POST({
				url : '/wa/website/referencement/',
				data : list,
				statusCode : {
					200 : function(json) {								
						admin.panels.close('center');
					},
					400 : function(json) {
						admin.messages.error(json.msg);
					},
				}
			});
		},
	},
	maintenance: {
		get:  function(){
			admin.GET({
				url : '/wa/website/maintenance/',
				statusCode : {
					200 : function(json) {								
						admin.panels.display('center', json.html);
					},
				}
			});
		},
		post: function(){
			list = admin.serialize("#page_maintenance_form");
			
			admin.POST({
				url : '/wa/website/maintenance/',
				data : list
			});
		},
	},
	currentUser: {
		get:  function(){
			admin.GET({
				url : '/wa/users/currentUser/',
				statusCode : {
					200 : function(json) {			
						admin.urls.hash('/user');								
						admin.panels.display('center', json.html);
					},
				}
			});
		},
		post: function(){
			list = admin.serialize("#user_pass_form");
			
			admin.POST({
				url : '/wa/users/currentUser/',
				data : list,
				statusCode : {
					200 : function(json) {
						admin.panels.close('center');
					},
					400 : function(xhr) {
						json = admin.xhr2json(xhr);
						admin.panels.change_content('center', json.html);
					},
				}
			});
		},
	},
	cancel_form: function(){
		$("#wa_toolbar_menu li").removeClass("selected");
		$("#wa_toolbar_menu li.preview").addClass('selected');
		admin.cancel_form();
	}
};
