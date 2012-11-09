/*
 *  Slideshow
 *  Requires: jQuery 1.7.1 or later, Modulo Timer
 */

ionyweb.slideshow = {

    defaults: {
	fx: 'fade', // name of transition effect
	timeout: 4000, // milliseconds between slide transitions
	speed: 1000, // speed of the transition
	pause: false,
	pager: null,
	thumb: false,
	// Not used yet ...
	// after: null, // transition callback executing after slide transition
	// before: null, // transition callback executing before slide transition
	// random: null,
    },

    Slideshow: function(idObj, opts){
	var instance_obj = $('#'+idObj);
	var instance_opts = {};
	if(opts != undefined){
	    instance_opts = opts;
	}
	var instance = {
	    obj: instance_obj,
	    container: $(instance_obj.parent().get(0)),
	    opts: instance_opts,
	    items: null,
	    current: 0,
	    intervalID: null,
	    thumbs: [],
	    init_items: function(){this.items = this.obj.children('img');},
	    init_fx_transition: function(){
		var fx_transition = ionyweb.slideshow.transitions[this.get_opt('fx')];
		if(fx_transition == undefined){
		    fx_transition = ionyweb.slideshow.transitions.fade;
		}
		this.opts.fx_transition = fx_transition;
	    },
	    init_transition: function(){this.opts.fx_transition.init(this);},
	    get_id: function(){ return idObj; },
	    get_opt: function(opt){
		if( this.opts[opt] != undefined ){
		    return this.opts[opt];
		}else{
		    return ionyweb.slideshow.defaults[opt];
		}
	    },
	    get_current_item: function(){return $(this.items[this.current]);},
	    get_next: function(){
		this.next();
		return this.get_current_item();
	    },
	    next: function(){
		this.current += 1;
		if(this.current >= this.items.length){
		    this.current = 0;
		}
	    },
	    prev: function(){
		if(this.current == 0){
		    this.current = this.items.length-1;
		}else{
		    this.current -= 1;
		}
	    },
	    start: function(){
		var timer_callback = function(instance){
		    var slideIn = instance.get_current_item();
		    var slideOut = instance.get_next();
		    instance.opts.fx_transition.play(instance, slideIn, slideOut);
		    instance.update_pager_items();
		}
		var timeout = this.get_opt('timeout');
		if(timeout > 0){
		    this.timer = new ionyweb.timer.LoopTimer(timer_callback, timeout, this);
		}
	    },
	    show_item: function(itemIndex){
		this.pause();
		var slideIn = instance.get_current_item();
		this.current = itemIndex;
		var slideOut = instance.get_current_item();
		this.opts.fx_transition.play(this, slideIn, slideOut);
		this.update_pager_items();
		this.start();
	    },
	    get_show_callback: function(i){
		var instance = this;
		return function(){ instance.show_item(i); };
	    },
	    resume: function(){
		this.timer.resume();
	    },
	    pause: function(){
		this.timer.pause();
	    },
	    build: function(){
		if(this.get_opt('pager')){this.build_pager();}
		this.init_transition();
		if(this.get_opt('thumb')){
		    var i;
		    for(i=0; i < this.items.length -1; i++){
			this.thumbs[i] = $(this.items[i]).clone();
		    }
		}
		if(this.get_opt('pause')){
		    var instance = this;
		    $(this.obj).hover(
			function(ev){ instance.pause(); },
			function(ev){ instance.resume(); });
		}
		this.start();
	    },
	    build_pager: function(){
		// Pager container
		var pagerObj = $('<div></div>');
		pagerObj.attr('id', this.get_opt('pager'));
		pagerObj.addClass('plugin-slideshow-pager');
		// Pager items
		var thumbOpt = this.get_opt('thumb');
		var i, thumb, item;
		for(i=0; i<this.items.length; i++){
		    item = $(this.items[i]);
		    itemPagerObj = $('<a></a>');
		    if(thumbOpt){
			thumb = $('<img />');
			thumb.attr('src', item.attr('src'));
			thumb.css('height', 50);
			thumb.css('width', 50);
		     	itemPagerObj.append(thumb);
		    }else{
		    	itemPagerObj.text(i+1);
		    }
		    itemPagerObj.click(this.get_show_callback(i));
		    pagerObj.append(itemPagerObj);
		}
		this.container.after(pagerObj);
		this.update_pager_items();
	    },
	    update_pager_items: function(){
		var pagerId = this.get_opt('pager');
		if(pagerId){
		    var pagerItems = $('#'+pagerId).children();
		    pagerItems.removeClass('active-slide');
		    $(pagerItems.get(this.current)).addClass('active-slide');
		}
	    }
	}
	// Updates items list
	instance.init_items();
	// Transition
	instance.init_fx_transition();
	// Don't register if no slides.
	if(instance.items.length == 0){
	    instance = null;
	}
	return instance;
    },

    instances: {},
    transitions: {},

    init: function(idObj, opts){
	// If object already exists, we kill the timer 
	// and then we re-instanciate the new object.
	if(this.instances[idObj] != undefined){
	    this.instances[idObj].pause();
	}
	var instance = this.Slideshow(idObj, opts);
	if( instance != null){
	    this.instances[idObj] = instance;
	    if(instance.items.length > 1){
		instance.build();
	    }else{
		console.log("Just one image... No transition !");
	    }
	    // instance.pause();
	}else{
	    console.log("No slide, so no slideshow instance !");
	}
    }
};


/******************************************************
 ** TRANSITION EFFECTS
 ******************************************************/

ionyweb.slideshow.transitions.fade = {
    init: function(instance){
	instance.items.each(function(i){
	    if(i > 0){ $(this).css('opacity', 0); }
	    $(this).css('position', 'absolute');
	});
    },
    play: function(instance, slideOut, slideIn){
	var duration = instance.get_opt('speed');
	slideOut.animate({'opacity': 0}, duration);
	slideIn.animate({'opacity': 1}, duration);
    }
};

ionyweb.slideshow.transitions.scrollLeft = {
    init: function(instance){
	// We copy the first item at the end of the list.
	$(instance.obj).append($(instance.items[0]).clone());
	instance.init_items();
	// We had a clear both elements for default positionning.
	$(instance.obj).append('<div style="clear: both;"></div>');
	// We calculate width params
	var objWidth = $(instance.obj).width();
	var totalWidth = instance.items.length*objWidth;
	// We set the width of each item
	// and floating default position.
	instance.items.each(function(i){
	    $(this).width(objWidth);
	    $(this).css('float', 'left');
	});
	$(instance.obj).width(totalWidth);
	$(instance.obj).css('position', 'absolute');
    },
    
    play: function(instance, slideOut, slideIn){
	var leftIn = slideIn.position().left;
	var rightIn = leftIn + slideIn.width();
	var rewind = false;
	// If we will show the last image,
	// we set rewind flag.
	if(instance.obj.width() == rightIn){
	    rewind = true;
	    instance.current = 0;
	}
	$(instance.obj).animate({'left': -leftIn},
				instance.get_opt('speed'),
				function(){
				    if(rewind){
					$(this).css('left', 0);
				    }
				});
    }
};

ionyweb.slideshow.transitions.scrollRight = {
    init: function(instance){
	// We copy the first item at the end of the list.
	$(instance.obj).append($(instance.items[0]).clone());
	instance.init_items();
	// We had a clear both elements for default positionning.
	$(instance.obj).append('<div style="clear: both;"></div>');
	// We calculate width params
	var objWidth = $(instance.obj).width();
	var totalWidth = instance.items.length*objWidth;
	// We set the width of each item
	// and floating default position.
	instance.items.each(function(i){
	    $(this).width(objWidth);
	    $(this).css('float', 'right');
	});
	$(instance.obj).width(totalWidth);
	$(instance.obj).css('position', 'absolute');
	$(instance.obj).css('right', 0);
    },
    
    play: function(instance, slideOut, slideIn){
	var leftIn = slideIn.position().left;
	var rightIn = leftIn + slideIn.width();
	var newRightObj = $(instance.obj).width() - rightIn;
	// If we will show the last image,
	// we set rewind flag.
	var rewind = false;
	if(leftIn == 0){ 
	    instance.current = 0;
	    rewind = true;
	}
	$(instance.obj).animate({'right': -newRightObj},
				instance.get_opt('speed'),
				function(){
				    if(rewind){
					$(this).css('right', 0);
				    }
				});
    }
};