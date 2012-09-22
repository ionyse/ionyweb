admin.urls = {
	hash: function(hash){
		if(hash === undefined){
			return window.location.hash;
		}else{
			window.location.hash = hash;
			$.cookie('ionyweb_admin', hash);
		}
	},
	load: function(hash){
		argv =  hash.split('/!/')[1];
		hash = hash.split('/!/')[0];
		
		// admin.messages.alert(hash + "  /!/  " + argv);
		
		switch(hash){
			case 	"": 					admin.menu.see(); break;
			case 	"/analytics": 			admin.settings.analytics.get(); break;
			case 	"/content": 			
				admin.edit.active(); 
				$("#wa_toolbar_menu li").removeClass("selected");
				$("#wa_toolbar_menu li.content").addClass('selected'); 
				break;
			case 	"/domains": 			admin.settings.domains.list(); break;
			case 	"/domains/add": 		admin.settings.domains.add(); break;
			case 	"/file_manager": 		admin.file_manager.toggle(); break;
			case 	"/page_manager": 		admin.pages.list(); break;
			case 	"/pages/edit": 			admin.pages.edit_form(argv); break;
			case 	"/plugins/add": 		admin.plugins.list(argv); break;
			case 	"/plugins/edit":		admin.plugins.edit(argv); break;
			case 	"/seo":					admin.settings.referencement.get(); break;
			case 	"/user":				admin.settings.currentUser.get(); break;
			case 	"/themes": 				admin.design.list(); break;
			case 	"/themes/styles": 		admin.design.styles(argv); break;
			case 	"/versions":			admin.settings.more(); break;
			default: admin.menu.see();
		}
	},
}

$(document).ready(function(){
	val = $.cookie('ionyweb_admin');
	if(val){
		$.cookie('ionyweb_admin', null);
		admin.urls.hash(val);
		admin.urls.load(val);
	}
});
