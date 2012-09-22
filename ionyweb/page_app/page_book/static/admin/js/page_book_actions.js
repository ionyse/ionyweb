admin.page_book = {

    edit_categories: function(relation_id){
	admin.GET({
	    url : '/wa/action/' + relation_id + '/category_list/',
	});
    },

    edit_clients: function(relation_id){
	admin.GET({
	    url : '/wa/action/' + relation_id + '/client_list/',
	});
    },

    edit_references: function(relation_id){
	admin.GET({
	    url : '/wa/action/' + relation_id + '/reference_list/',
	});
    }

};
