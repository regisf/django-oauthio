/**
 * Created by  on 30/01/2015.
 */

var OAuthIOStart = (function() {
    "use strict";

    function _register_on_server(url, response) {
        var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
        request.open('POST', url);
        request.send(response);
    }

    function _do_err(provider, err) {
        if (options[provider] && typeof options[provider] == 'function') {
            options[provider](false, provider, result);
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

