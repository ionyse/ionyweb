admin.test = {
	g200 : function() {
		admin.GET({
			url : '/wa/test/200/'
		});
	},
	g400 : function() {
		admin.GET({
			url : '/wa/test/400/'
		});
	},
	g404 : function() {
		admin.GET({
			url : '/wa/test/404/'
		});
	},
	g409 : function() {
		admin.GET({
			url : '/wa/test/409/'
		});
	},
	g500 : function() {
		admin.GET({
			url : '/wa/test/500/'
		});
	}
};
