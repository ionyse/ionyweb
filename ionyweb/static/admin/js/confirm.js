/*
 * 
 *  This function replace a confirm box in javascript using jQuery
 * 
 */
(function($){

	$.confirm = function(params){

		var buttonHTML = '';
		$.each(params.buttons,function(name,obj){

			// Generating the markup for the buttons:
		    var verbose_name = name;
		    if(obj['verbose_name'] != undefined){
			verbose_name = obj['verbose_name'];
		    }

		    buttonHTML += '<input type="button" class="button '+obj['class']+'" value="'+verbose_name+'" />';

			if(!obj.action){
				obj.action = function(){};
			}
		});

		var markup = [
			'<div class="confirm">',
			'<p>',params.message,'</p>',
			'<div><form>',
			buttonHTML,
			'</form></div></div>'
		].join('');
		
		$('#admin_message .confirm').remove();

		$(markup).hide().appendTo('#admin_message').show('drop');

		var buttons = $('#admin_message .confirm .button'),
			i = 0;

		$.each(params.buttons,function(name,obj){
			buttons.eq(i++).click(function(){

				// Calling the action attribute when a
				// click occurs, and hiding the confirm.

				obj.action();
				$.confirm.hide();
				return false;
			});
		});
	}

	$.confirm.hide = function(){
		$('#admin_message .confirm').hide('drop', function(){
			$(this).remove();
		});
	}

})(jQuery);
