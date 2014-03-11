'use strict'

angular.module('planMateApp')
  .controller 'MainCtrl', [
    '$scope', 'AuthenticationService',
    ($scope, AuthenticationService) ->
      $scope.updateAuth = ->
        AuthenticationService.update()
  ]
