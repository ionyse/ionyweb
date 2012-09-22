/**
 * Cookie duplication on external domain 
 *
 * This file is loaded if the external domain doesn't have yet a
 * sessionid cookie. It tries to get id from the authentication
 * serveur.
 *
 * Author: Rémy Hubscher <remy.hubscher@ionyse.com>
 * Modified: 23/03/2011
 *
 */

var cookie_value = "{{ cookie }}";
$.cookie('sessionid', cookie_value, { path: '/'});
window.location.reload();
