/**
 * Django-OAuthio - Use OAuth.io authentication service with Django
 * (c) Régis FLORET 2015 and later
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

var OAuthIOStart = (function() {
    "use strict";

    function getCookie_(key) {
        if (document.cookie) {
            var cookies = document.cookie.split(';'), keyVal;
            for (var i in cookies) {
                keyVal = cookies[i].split('=');
                if (keyVal[0] == 'csrftoken') {
                    return keyVal[1];
                }
            }
        }
        return "";
    }

    // Setup default behaviour
    var options_ = {
        // Where to send the data
        url: null,

        // Connected with the provider
        done: function(result) {
            if (this.url) {
                var request = new XMLHttpRequest();
                var self=this;

                request.onerror = function (e) {self.error(result['provider'], e.responseText)};

                request.onreadystatechange = function (e) {
                    if (request.readyState === 4) {
                        if (request.status === 200) {
                            self.success(result['provider'], result);
                        } else {
                            self.error(result['provider'], e.responseText);
                        }
                    }
                };

                request.open('POST', this.url);
                request.setRequestHeader('Content-Type', 'application/json');
                request.setRequestHeader('X-CSRFToken',getCookie_('csrftoken'));
                request.send(JSON.stringify(result));
            } else {
                console.error("No url for server registration");
            }
        },

        // An error occured
        fail: function(provider, err) {console.error(this.error(provider, err))},

        // Reload page
        success: function(provider, result) {document.location = document.location},

        // Display error on console
        error: function(provider, err) {console.error("For provider:"+ provider + "Error: " + err)}
    };

    return function (options) {
        if (options.public_key === undefined) {
            var msg = "OAuth.io public key is not set";
            if (options.debug === true) {
                alert(msg);
            } else {
                console.error(msg);
            }
            return;
        }

        // Merge the objects
        for(var o in options) {
            options_[o] = options[o];
        }

        // Start OAuth.io library
        OAuth.initialize(options.public_key);

        // Get all element for connection.
        var elements = document.querySelectorAll('[data-oauthio-provider]'), provider;
        for (var i in elements) {
            (function (el) {
                if (typeof el === 'object') {
                    el.onclick = function (event) {
                        event.preventDefault();
                        var provider = el.getAttribute("data-oauthio-provider");

                        OAuth.popup(provider)
                            .done(function (result) {
                                result.me()
                                    // OK Everythings goes fine. Send all needed information to the server
                                    .done(function(res) {
                                        options_.done({
                                            provider: provider,
                                            access_token: result['access_token'],
                                            email: res['email'],
                                            username: res['name'],
                                            first_name: res['first_name'],
                                            last_name: res['last_name'],
                                            avatar: res['avatar']
                                        });
                                    })
                                    // The me() request failed
                                    .fail(function(err) {options_.fail(provider, err)});
                            })

                            // The popup failed
                            .fail(function(err) {options_.fail(provider, err)});
                    };
                }
            })(elements[i]);
        }
    }
})();

