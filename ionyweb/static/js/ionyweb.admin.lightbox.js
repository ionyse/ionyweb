/*
 *  Modulo Admin+ Lightbox
 */

admin.lightbox = {

    defaults: {
	// Modulo Lightbox Config
	'selector': '.admin_lightbox',
	// FancyBox Config
	'openEffect': 'fade',
	'closeEffect': 'fade',
	'nextEffect': 'fade',
	'prevEffect': 'fade',
	'index': '9999',
    },
    init: function(opts){
	
	if(opts){
	    for(opt in opts){
		admin.lightbox.defaults[opt] = opts[opt];
	    }
	}
	$(admin.lightbox.defaults.selector).fancybox(admin.lightbox.defaults);

    },

};