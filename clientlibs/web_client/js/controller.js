MASTERAPP.controller('homeCtrl', ['$scope', '$state', '$cookies', '$timeout', 'ricsAPI', function ($scope, $state, $cookies, $timeout, ricsAPI) {
	$scope.person = {}
	$scope.user = {}
	$scope.feed = []
	$scope.community_feed = []
	$scope.my_tweets = []
	$scope.tweet = {message:''}
	

  	$scope.userAccess = function(){
	  	ricsAPI.accessPassport(function(resp){
	    	if(resp.status === 200){
	     		$scope.user = resp.data
	    	}
	    });
	}

	$scope.logUserOut = function(){
		$cookies.remove('ricsmasterapp-cookie');
		window.location.reload()
	}

	$scope.myTweets = function(){
		ricsAPI.myTweets(function(resp){
        	if(resp.status == 200){
          		$scope.my_tweets = resp.data;
        	}
      	});
	}

	$scope.Feed = function(){
		ricsAPI.Feed(function(resp){
			if(resp.status === 200){
				$scope.feed = resp.data;
			}
		});
	}

	$scope.communityFeed = function(){
		ricsAPI.communityFeed(function(resp){
			if(resp.status === 200){
				$scope.community_feed = resp.data;
			}
		});
	}

	$scope.createTweet = function(){
		if(!$scope.tweet.message){
			ricsAPI.showAlert('You are missing a tweet! ; )', function(resp){});
		}else{
	      	ricsAPI.createTweet($scope.tweet, function(resp){
	      		$timeout($scope.myTweets, 200);
	      	});
	    }
    }

    $scope.Person = function(){
    	ricsAPI.Person({user_name: $state.params.user_name}, function(resp){
			if(resp.status === 200){
				$scope.person = resp.data
			}
		});
    }

    $scope.FollowPerson = function(){
    	$scope.person.following = ($scope.person.following)?false:true;
    	ricsAPI.FollowPerson({user_name:$scope.person.user_name}, function(resp){});
    }

	function init(){
		if($state.current.name  === 'person' && $state.params.user_name != ""){
			$scope.Person();
		}else{
			$scope.userAccess();
			$scope.myTweets();
			$scope.Feed();
			$scope.communityFeed();
		}
	}

	init();
	
}]);
	

MASTERAPP.controller('accessRequestCtrl', ['$scope', '$http', '$state', 'ricsAPI', function ($scope, $http, $state, ricsAPI) {

	$scope.user_data = {email:'', cellphone:''}

	$scope.sendRequest = function(){
		if(!$scope.user_data.email || !$scope.user_data.cellphone){
			ricsAPI.showAlert('Please feel out the form.', function(resp){});
			return
		}

		ricsAPI.accessRequest($scope.user_data, function(resp){
			if(resp.status === 200){
				$state.go('access_verify')
			}else{
				ricsAPI.showAlert(resp.message, function(resp){});
			}
		});
	}

}]);


MASTERAPP.controller('accessVerifyCtrl', ['$scope', '$http', '$state', '$location', 'ricsAPI', function ($scope, $http, $state, $location, ricsAPI) {

	$scope.user_data = {access_token:''}

	$scope.sendVerification = function(){
		ricsAPI.accessVerify($scope.user_data, function(resp){
			if(resp.status === 200){
				ricsAPI.showAlert('Access granted', function(resp){
					if (resp){
						$state.go('home');
					}
				});
			}else{
				ricsAPI.showAlert(resp.message, function(resp){
					$state.go('access_request');
				});
			}
		});
	}

}]);


MASTERAPP.controller('navCtrl', ['$scope', '$ionicSideMenuDelegate', function ($scope, $ionicSideMenuDelegate) {
	$scope.toggleLeftSideMenu = function() {
    	$ionicSideMenuDelegate.toggleLeft();
  	};
}]);
