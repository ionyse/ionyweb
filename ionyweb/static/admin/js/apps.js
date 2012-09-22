
admin.apps = {
    edit: function(id) {
        url = '/wa/page_app/';
        if(id != undefined) {
            url += id+'/'; 
        }
        admin.GET({
            url: url
        });
    },
    save: function(id){
        url = '/wa/page_app/';
        if(id != undefined) {
            url += id+'/'; 
        }
        list = admin.serialize('#app_form_form');
        admin.POST({
            url: url,
            data: list,
            statusCode: {
                200: function(json) {
					admin.messages.alert(json.msg);
					admin.panels.close_all();
					if(json.layout_section_slug && json.html){
						admin.pages.refresh_layout(json.layout_section_slug,
												   json.html);
						admin.edit.refresh();
					}
					if(json.refresh_pages_list){
						//admin.pages.list();
					}
                }
            }
        });
    }
};
