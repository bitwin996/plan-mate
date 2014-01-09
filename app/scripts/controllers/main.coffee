'use strict'

angular.module('planMateApp')
  .controller 'MainCtrl', [
    '$scope', 'AuthenticationService',
    ($scope, AuthenticationService) ->
      $scope.awesomeThings = [
        'HTML5 Boilerplate'
        'AngularJS'
        'Karma'
      ]

      AuthenticationService.update()
  ]
