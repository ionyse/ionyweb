var admin = {};

admin.callback = "";
//This element is use to save the callback function in confirm messages
admin.hash = "";
admin.layout_slug = "";

admin.xhr2json = function(xhr) {

	if((xhr.responseText[0] == '{' && xhr.responseText[xhr.responseText.length - 1] == '}') || (xhr.responseText[0] == '[' && xhr.responseText[xhr.responseText.length - 1] == ']')) {
		return eval('(' + xhr.responseText + ')');
	} else {
		return {
			'msg' : xhr.responseText
		};
	}
};

// This decorator make sure to close the loading after an ajax call
status_code_decorator = function (callback) {
	return function(json_or_xhr) { 
		callback(json_or_xhr);
		admin.loading.hide();
	};
};

STATUS_CODE = {
	200 : function(json) {
		admin.panels.display('center', json.html);
		if(json.msg != undefined) {
			admin.messages.alert(json.msg);
		}
	},
	202 : function(json) {
	    console.log('redirection asked :', json.location);
	    window.location.href = json.location;
	},
	400 : function(xhr) {
		json = admin.xhr2json(xhr);
		admin.panels.display('center', json.html);
		if(json.msg != undefined) {
			admin.messages.alert(json.msg);
		}
	},
	403 : function(xhr) {
		json = admin.xhr2json(xhr);
		admin.messages.alert(gettext("You don't have the right to modify this settings."));
	},
	404 : function(xhr) {
		json = admin.xhr2json(xhr);
		if(json.msg != undefined) {
			admin.messages.error(json.msg);
		} else {
			admin.messages.error(gettext("Element not found."));		
		}
	},
	409 : function(xhr) {
		json = admin.xhr2json(xhr);
		if(json.msg != undefined) {
			admin.messages.error(json.msg, 800);
		}
	},
	500 : function(xhr) {
		json = admin.xhr2json(xhr);
		if(json.msg != undefined) {
			admin.messages.error(json.msg);
		}
	}
};

admin.urljoin = function (url, suffix) {
	if(url != undefined && suffix != undefined) {
		s_url = url.split('/');
		s_suffix = suffix.split('/');
		var urls = new Array('');for (k in s_url) if(s_url[k]) urls.push(s_url[k]);
		for (k in s_suffix) if(s_suffix[k]) urls.push(s_suffix[k]);
		urls.push('');
		return urls.join('/');
	} else {
		return url;
	}
};

admin.ajax = function(dict) {
	
	if(window.location.pathname != '/') {
		dict['url'] = admin.urljoin(window.location.pathname, dict['url']);
	}

	if(dict['statusCode'] != undefined) {
		for(key in STATUS_CODE) {
			if(dict['statusCode'][key] == undefined) {
				dict['statusCode'][key] = STATUS_CODE[key];
			}
		}
	} else {
		dict['statusCode'] = STATUS_CODE;
	}

	// For each ajax callback, we make sure to close the loading box after.
    for(key in dict['statusCode']) {
		dict['statusCode'][key] = status_code_decorator(dict['statusCode'][key]);
	}

	// Ajout de la gestion des erreurs serveur
	dict['error'] = function(request, errorType, errorThrown){
		if(errorType == 'error' && errorThrown == '') {
			admin.messages.error("Le serveur ne répond pas");			
		}
	}

	admin.loading.show(function() {$.ajax(dict);});

};

admin.GET = function(dict) {
	dict['type'] = 'GET';
	admin.ajax(dict);
};

admin.POST = function(dict) {
	dict['type'] = 'POST';
	admin.ajax(dict);
};

admin.PUT = function(dict) {
	dict['type'] = 'PUT';
	admin.ajax(dict);
};

admin.DELETE = function(dict) {
	dict['type'] = 'DELETE';
	admin.ajax(dict);
};
// Serialize a form and return the data for ajax
admin.serialize = function(id) {
	if( typeof (tinyMCE) != "undefined") {
		tinyMCE.triggerSave();
		tinyMCE = undefined;
	}

	console.log($(id).serialize());

	return $(id).serialize();
};

admin.login = {
	show : function() {
		$("#ionyweb_admin_login").show('drop', {}, 250);
		$(document).keyup(function(e) {
			if (e.keyCode == 27) { admin.login.hide(); }   // esc
		});
	},
	connect : function() {
		list = admin.serialize('#ionyweb_admin_login form');
		admin.POST({
			url : '/wa/login/',
			data : list,
			statusCode : {
				200 : function(json) {
					$("#ionyweb_admin_login").hide('drop', {
						direction : "right"
					}, 250, function() {
						window.location.hash = "";
						window.location.reload();
					});
				},
				400 : function(xhr) {
					json = admin.xhr2json(xhr);
					$('#ionyweb_admin_login_error').html(json.msg);
				}
			}
		});
	},
	hide : function() {
		window.location.hash = "";
		$("#ionyweb_admin_login").hide('drop', {
			direction : "right"
		}, 250);
	}
};

admin.cancel_form = function() {
	admin.panels.close_all();
	admin.urls.hash('');
};

admin.logout = function() {
	admin.GET({
		url : '/wa/logout/',
		statusCode : {
			200 : function(json) {
				admin.edit.deactive();
				$("#ionyweb_admin").hide('slide', function() {
					window.location.hash = "#";
					window.location.reload();
				});
			}
		},
	});
};

admin.loading = {
	show: function(callback){
		if( callback ) callback();
		$("#wa_panel_loading").show('fade');
	},
	hide: function(callback){
		if( callback ) callback();
		$("#wa_panel_loading").stop().hide('fade');
	}
};
