// This is use to display popup message (Growl style) to the user.

admin.messages = {
	alert : function(content, duration) {
		if(duration === undefined) {
			duration = '2000';
		}
		$("#admin_message").append("<div class='message'><p>" + content + "</p></div>");
		$("#admin_message .message:last").show('drop').delay(duration).hide('drop', function() {
			$("#admin_message .message:hidden").remove();
		});
	},
	confirm : function(content, callback, callback_no) {

		$.confirm({
			'message' : content,
			'buttons' : {
				'Yes' : {
					'class' : 'blue',
					'action' : function() {
						callback();
					},
					'verbose_name' : gettext('Yes'),
				},
				'No' : {
					'class' : 'gray',
					'action' : function() {
						if(callback_no) {
							callback_no();
						}
					}, // Nothing to do in this case. You can as well omit the action property.
					'verbose_name' : gettext('No'),
				}
			}
		});

	},
	error : function(content, duration) {
		if(duration === undefined) {
			duration = '2000';
		}
		$("#admin_message").append("<div class='error'><p>" + content + "</p></div>");
		$("#admin_message .error:last").show('drop').delay(duration).hide('drop', function() {
			$("#admin_message .error:hidden").remove();
		});
	},
	draft : function(content, duration) {
		if(duration === undefined) {
			duration = '2000';
		}
		$("#admin_message").append("<div class='draft'><p>" + content + "</p></div>");
		$("#admin_message .draft:last").show('drop').delay(duration).hide('drop', function() {
			$("#admin_message .draft:hidden").remove();
		});
	},
	refresh_help_text_bubble : function(){
		$("[rel=tooltip]").tooltip();
	}
};
