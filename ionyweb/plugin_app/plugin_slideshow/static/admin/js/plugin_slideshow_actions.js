admin.plugin_slideshow = {

    edit_slides : function(relation_id){
	admin.GET({
	    url : '/wa/action/' + relation_id + '/slide_list/',
	});
    },

}