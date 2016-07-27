var MASTERAPP = angular.module('masterapp',['ionic', 'ngCookies'])

MASTERAPP.config(['$stateProvider', '$ionicConfigProvider', '$urlRouterProvider', function($stateProvider, $ionicConfigProvider, $urlRouterProvider) {
  $ionicConfigProvider.views.transition('none');
  $ionicConfigProvider.templates.maxPrefetch(0);
  $ionicConfigProvider.views.maxCache(0);
  $ionicConfigProvider.scrolling.jsScrolling(true)


  $urlRouterProvider.otherwise('/home')

  $stateProvider.state('home', {
    url: '/home',
    abstract: false,
    templateUrl: '/clientlibs/web_client/templates/home.html',
    controller:'homeCtrl'
  })


  $stateProvider.state('person', {
    url: '/person/:user_name',
    abstract: false,
    templateUrl: '/clientlibs/web_client/templates/person.html',
    controller:'homeCtrl'
  })

  $stateProvider.state('myfeed', {
    url: '/myfeed',
    abstract: false,
    templateUrl: '/clientlibs/web_client/templates/myfeed.html',
    controller:'homeCtrl'
  })

  $stateProvider.state('mytweets', {
    url: '/mytweets',
    abstract: false,
    templateUrl: '/clientlibs/web_client/templates/mytweets.html',
    controller:'homeCtrl'
  })

  $stateProvider.state('community', {
    url: '/community',
    abstract: false,
    templateUrl: '/clientlibs/web_client/templates/community.html',
    controller:'homeCtrl'
  })

  $stateProvider.state('access_request', {
    url: '/access/request',
    templateUrl: '/clientlibs/web_client/templates/access-request.html',
    controller:'accessRequestCtrl'
  })

  $stateProvider.state('access_verify', {
    url: '/access/verify',
    templateUrl: '/clientlibs/web_client/templates/access-verify.html',
    controller:'accessVerifyCtrl'
  })


}]);