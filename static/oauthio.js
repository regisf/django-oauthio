/**
 * Created by  on 30/01/2015.
 */

var OAuthIOStart = (function() {
    "use strict";

    function _register_on_server(response) {
        if (response.status && response.status === 'success') {
	    var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
            request.addEventlistener('load', function() {

            }, false);

            request.onload = function(evt) {

            };
            request.open('POST', url);
            request.send(JSON.stringify(response.data));
	    
	}


    }

    function _do_err(cb, err) {
        if (cb && typeof cb == 'function') {
            cb(false, result);
        } else {
            console.log(err);
        }
    }

    function OAuthIOStart(options) {
        OAuth.initialize(options.public_key);
        var oauths = document.querySelectorAll('[data-oauthio-provider]'), provider;
        for (var i in oauths) {
            (function (el) {
                if (typeof el !== 'object') {
                } else {
                    el.addEventListener('click', function (event) {
                        event.preventDefault();
                        var provider = el.getAttribute("data-oauthio-provider");
                        OAuth.popup(provider)
                            .done(function (result) {
                                if (options[provider] && typeof options[provider] == 'function') {
                                    options[provider](false, provider, result);
                                } else {
                                    result.me()
                                        .done(_register_on_server)
                                        .fail(function(err) {
                                            _do_err(config[provider], error);
                                        });
                                }
                            })
                            .fail(function (err) {
                                _do_err(options[provider], err);
                            });
                    });
                }
            })(oauths[i]);
        }
    }
    return OAuthIOStart;
})();

