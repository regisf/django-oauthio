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

    // Setup default behaviour
    var options_ = {
        // Connected with the provider
        done: function(provider, result) {
            if (result.status && result.status === 'success') {
                var request = new XMLHttpRequest();
                var self=this;

                request.onerror = function (e) {self.error(provider, e.responseText)};

                request.onreadystatechange = function (e) {
                    if (request.readyState === 4) {
                        if (request.status === 200) {
                            self.success(provider, result);
                        } else {
                            self.error(provider, e.responseText);
                        }
                    }
                };

                request.open('POST', url);
                request.send(JSON.stringify(result.data));
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
            if (options.debug === true) {
                alert("OAuth.io public key is not set");
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
                                    // OK Everythings goes fine
                                    .done(function(result) {
                                        options_.done(provider, result);
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

