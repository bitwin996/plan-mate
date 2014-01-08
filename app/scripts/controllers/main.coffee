'use strict'

angular.module('planMateApp')
  .controller 'MainCtrl', [
    '$scope', 'AuthorizationService',
    ($scope, AuthorizationService) ->
      $scope.awesomeThings = [
        'HTML5 Boilerplate'
        'AngularJS'
        'Karma'
      ]

      AuthorizationService.update()
  ]
