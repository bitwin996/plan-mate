'use strict'

angular.module('planMateApp')
  .controller 'AuthLoginCompleteCtrl', [
    '$rootScope', '$location', 'AuthenticationService',
    ($rootScope, $location, AuthenticationService) ->

      $rootScope.navbar?.isCollapsed = true

      #TODO
      $location.path '#/mypage/plans'
  ]
