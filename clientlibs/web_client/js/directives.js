MASTERAPP.directive('profileWidget', function() {
  return {
    restrict: 'E',
    templateUrl:'/clientlibs/web_client/templates/widgets/profile-widget.html'
  }
})


MASTERAPP.directive('personWidget', function() {
  return {
    restrict: 'E',
    templateUrl:'/clientlibs/web_client/templates/widgets/person-widget.html'
  }
})

MASTERAPP.directive('createTweetWidget', function() {
  return {
    restrict: 'E',
    templateUrl:'/clientlibs/web_client/templates/widgets/create-tweet-widget.html'
  }
})



MASTERAPP.directive('myTweetsWidget', function() {
  return {
    restrict: 'E',
    templateUrl:'/clientlibs/web_client/templates/widgets/my-tweets-widget.html'
  }
})



MASTERAPP.directive('myFeedWidget', function() {
  return {
    restrict: 'E',
    templateUrl:'/clientlibs/web_client/templates/widgets/my-feed-widget.html'
  }
})


MASTERAPP.directive('communityFeedWidget', function() {
  return {
    restrict: 'E',
    templateUrl:'/clientlibs/web_client/templates/widgets/community-feed-widget.html'
  }
})
