/* global $ */

var initialize = function (navigator, user, token, urls) {
	$('#id_login').on('click', function() {
		// console.log(navigator);
		navigator.id.request();
		// navigator.id.doSomethingElse();
	});

	navigator.id.watch({
		loggedInUser: user,
		onlogin: function(assertion) {
			var deferred = $.post(
				urls.login,
				{ assertion: assertion, csrfmiddlewaretoken: token }
			);
			// .done(function() { window.location.reload(); })
			// .fail(function() { navigator.id.logout(); });
			deferred.done(function () { window.location.reload(); }) 
			deferred.fail(function () { navigator.id.logout(); });
		},
		onlogout: function() {},
	});
};

window.Superlists = {
	Accounts: {
		initialize: initialize,
	}
};