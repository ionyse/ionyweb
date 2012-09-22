/*
 *  Modulo Lightbox
 */

ionyweb.lightbox = {

    defaults: {
	// Modulo Lightbox Config
	'selector': '.lightbox',
	// FancyBox Config
	'openEffect': 'fade',
	'closeEffect': 'fade',
	'nextEffect': 'fade',
	'prevEffect': 'fade',

    },
    init: function(opts){
	
	if(opts){
	    for(opt in opts){
		ionyweb.lightbox.defaults[opt] = opts[opt];
	    }
	}
	$(ionyweb.lightbox.defaults.selector).fancybox(ionyweb.lightbox.defaults);

    },

};