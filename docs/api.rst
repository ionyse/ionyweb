=========
Admin API
=========

Describe informations about the admin API.

Status Code Response
====================

1. **GET** Method :

 * *200 - OK* :
   The resource has been found and the response contains datas.

 * *400 - Bad Request* :
   Indicates a bad request (e.g. wrong parameter).

 * *404 - Not Found* :
   The asked resource does not exist.

2. **PUT** Method :
 * *200 - OK* :
   The new resource has been created and the response contains datas.

 * *400 - Bad Request* :
   Indicates a bad request (e.g. wrong parameter).

3. **POST** Method :
 * *200 - OK* :
   The existing resource has been updated the response contains datas.

 * *202 - ACCEPTED* :
   The existing resource has been updated the page must be reloaded.
   The json contains the location of the redirection.

 * *400 - Bad Request* :
   Indicates a bad request (e.g. wrong parameter).

 * *404 - Not Found* :
   The asked resource for updating does not exist.

4. **DELETE** Method :
 * *200 - OK* :
   The existing resource has been deleted.

 * *400 - Bad Request* :
   Indicates a bad request (e.g. wrong parameter).

 * *404 - Not Found* :
   The asked resource does not exist.

 * *409 - Conflict* :
   A BDD conflict has been occured during deletion (e.g. resource is used by another resource).


Default Data Response
---------------------

* **Message** - ``msg`` :

By default, all responses contains the ``msg`` parameter which
will be displayed in the interface.

The *200* and *400* status displays the message with standard message design
(``admin.messages.alert()`` method).
For *404*, *409* and *500* status, the interface displays the message using
standard error message design (``admin.messages.error()`` method).

* **Content** - ``html`` :

By default, only *200* and *400* response contains the ``html`` parameter.

This parameters contains the new HTML content which will use by the admin to refresh the center panel.


Custom actions
--------------

If you want custom the admin actions for a particular status code, just define a new function for this status
in your request method.

**Be careful about data object in the response :**

    If the request is successful (*200* and *400* status codes), the status code functions take a ``json``
    parameter which contains the data returned from the server;
    if it results in an error (*404*, *409* and *500* status codes) they take ``jqXHRan`` paramater which
    have to be transformed with ``admin.xhr2json()`` method before to be used.
    
    See the `jQuery doc <http://api.jquery.com/jQuery.ajax/>`_ for more precisions.


For example, sending a POST request and override the *400* and *500* status codes actions::

    admin.POST({
        url: '/my/custom/url/',
	data: {'first_data': "Value #1", },
	statusCode: {
	    400: function(json) {
		// Put your actions here...
		admin.messages.alert('My custom action !!');
	    },
	    500: function(json) {
	        // Convert jqXHRan object
	        json = admin.xhr2json(json);
		// Put your actions here...
		admin.messages.alert(json.myData);
	}
    });

