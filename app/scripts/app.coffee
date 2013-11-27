'use strict'

angular.module('planMateApp', [
  'ngCookies'
  'ngResource'
  'ngSanitize'
  'ngRoute'
])
  .config ['$routeProvider', ($routeProvider) ->
    $routeProvider
      .when '/',
        templateUrl: 'views/main.html'
        controller: 'MainCtrl'
      .otherwise
        redirectTo: '/'
  ]
