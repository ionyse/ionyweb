admin.page_blog = {

    edit_categories: function(relation_id){
		admin.GET({
		    url : '/wa/action/' + relation_id + '/category_list/',
		});
    },

    edit_entries: function(relation_id){
		admin.GET({
		    url : '/wa/action/' + relation_id + '/entry_list/',
		});
    },


};
