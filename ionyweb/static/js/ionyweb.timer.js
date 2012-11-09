/*
 *  Modulo Timer
 */

ionyweb.timer = {
    Timer: function(callback, delay, params) {
	var timerId, start = null;
	var remaining = delay;
	var running = false;
	this.pause = function() {
	    if(running){
		running = false;
		window.clearTimeout(timerId);
		remaining -= new Date() - start;
	    }
	};
	this.resume = function() {
	    if(!running){
		running = true;
		start = new Date();
		timerId = window.setTimeout(callback, remaining, params);
	    }
	};
	this.resume();
    },
    LoopTimer: function(callback, delay, params) {
	var timerId, start, remaining = null;
	var intervalRunning, timerRunning = false;
	var intervalCallback = function(params){
	    callback(params);
	    remaining = delay;
	    start = new Date();
	};
	var timeoutCallback = function(params, timerInstance){
	    callback(params);
	    timerRunning = false;
	    timerInstance.start();
	};
	this.pause = function(){
	    if(intervalRunning || timerRunning){
		remaining -= new Date() - start;
		if(intervalRunning){
		    window.clearInterval(timerId);
		    intervalRunning = false;
		}else if(timerRunning){
		    window.clearTimeout(timerId);
		    timerRunning = false;
		}
	    }
	};
	this.start = function() {
	    if(!intervalRunning && !timerRunning){
		intervalRunning = true;
		remaining = delay;
		start = new Date();
		timerId = window.setInterval(intervalCallback, remaining, params);
	    }
	};
	this.resume = function() {
	    if(!intervalRunning && !timerRunning){
		timerRunning = true;
		start = new Date();
		timerId = window.setTimeout(timeoutCallback, remaining, params, this);
	    }
	};
	this.start();
    }
};
