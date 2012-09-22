admin.themes = {
    list: function(){
		$.ajax({
		    type: 'GET',
		    url: window.location.pathname+'wa/themes/',
		    statusCode: {
			200: function(json) {
			    admin.panels.display('bottom',json.html);			    
			},
		    }
		});
    },
    edit: function(slug, csrf_token){
		$("#themes_listform").parent().hide('slow', function(){ 
		    $("#themes_listform").parent().html("");
		});
		if(slug != '0'){
		    $.ajax({
			type: 'POST',
			url: '/wa/themes/',
			data: {'page_path': window.location.pathname,
			       'theme_slug': slug,
			       'csrfmiddlewaretoken': csrf_token},
			statusCode: {
			    200: function(json) {
				admin.messages.alert(json.msg);
				setTimeout(function () {
				    window.location.reload();
				    admin.panels.close_all();
				}, 1000);
			    },						
			},
		    });	
		}
    }
};
