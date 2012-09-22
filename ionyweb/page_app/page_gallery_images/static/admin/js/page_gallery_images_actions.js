admin.page_gallery_images = {

    edit_albums: function(relation_id){
	admin.GET({
	    url : '/wa/action/' + relation_id + '/album_list/',
	});
    },
    edit_album: function(relation_id, album_pk){
	admin.GET({
	    url : 'wa/action/' + relation_id + '/album/' + album_pk + '/',
	});
    },
    edit_images: function(relation_id, album_pk){
	admin.GET({
	    url : '/wa/action/' + relation_id + '/album/'+ album_pk +'/image_list/',
	});
    },
    edit_image: function(relation_id, album_pk, image_pk){
	admin.GET({
	    url : 'wa/action/' + relation_id + '/album/' + album_pk + '/image/' + image_pk + '/',
	});
    },

}
