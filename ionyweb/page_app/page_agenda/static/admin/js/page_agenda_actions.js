admin.page_agenda = {
    edit_events: function(relation_id){
	admin.GET({
	    url : '/wa/action/' + relation_id + '/event_list/',
	});
    }
}
