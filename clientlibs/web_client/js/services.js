MASTERAPP.factory('ricsAPI', ['$http', '$state', '$ionicPopup', function($http, $state, $ionicPopup){
	var service = {}

	service.FollowPerson = function(payload, callBack){
		var config = {headers: {'X-Ric-Master-App': 'Come on in!'}}
		var url = '/service/tweet/follow';
		$http.post(url, payload, config).success(function(resp){
			callBack(resp);
		}).error(function(resp){
			$state.go('access_request')
			return
		});
	}

	service.Person = function(payload, callBack){
		var config = {headers: {'X-Ric-Master-App': 'Come on in!'}}
		var url = '/service/tweet/person';
		$http.post(url, payload, config).success(function(resp){
			callBack(resp);
		}).error(function(resp){
			$state.go('access_request')
			return
		});
	}

	service.Feed = function(callBack){
		var config = {headers: {'X-Ric-Master-App': 'Come on in!'}}
		var url = '/service/tweet/feed';
		$http.get(url, config).success(function(resp){
			callBack(resp);
		}).error(function(resp){
			$state.go('access_request')
			return
		});
	}

	service.communityFeed = function(callBack){
		var config = {headers: {'X-Ric-Master-App': 'Come on in!'}}
		var url = '/service/tweet/communityfeed';
		$http.get(url, config).success(function(resp){
			callBack(resp);
		}).error(function(resp){
			$state.go('access_request')
			return
		});
	}

	service.createTweet = function(payload, callBack){
		var config = {headers: {'X-Ric-Master-App': 'Come on in!'}}
		var url = '/service/tweet/create';
		$http.post(url, payload, config).success(function(resp){
			callBack(resp);
		}).error(function(resp){
			$state.go('access_request')
			return
		});
	}

	service.myTweets= function(callBack){
		var config = {headers: {'X-Ric-Master-App': 'Come on in!'}}
		var url = '/service/tweet/my';
		$http.get(url, config).success(function(resp){
			callBack(resp);
		}).error(function(resp){
			$state.go('access_request')
			return
		});
	}
	
	service.accessPassport = function(callBack){
		var config = {headers: {'X-Ric-Master-App': 'Come on in!'}}
		var url = '/access/passport';
		$http.get(url, config).success(function(resp){
			callBack(resp);
		}).error(function(resp){
			$state.go('access_request')
			return
		});
	}

	service.accessRequest = function(data, callBack){
		var config = {headers: {'X-Ric-Master-App': 'Come on in!'}}
		var url = '/access/request';
		var payload = data;

		$http.post(url, payload, config).success(function(resp){
			callBack(resp);
		}).error(function(resp){
			callBack(resp)
		});
	}

	service.accessVerify = function(data, callBack){
		var config = {headers: {'X-Ric-Master-App': 'Come on in!'}}
		var url = '/access/verify';
		var payload = data;

		$http.post(url, payload, config).success(function(resp){
			callBack(resp);
		}).error(function(resp){
			callBack(resp)
		});
	}

	service.showAlert = function(msg, callBack) {
	    var alertPopup = $ionicPopup.alert({
	    	title: 'App Message',
	    	template: msg
	   	});
	   	alertPopup.then(function(res) {
	   		callBack(res);
	   	});
	};

	return service

}]);