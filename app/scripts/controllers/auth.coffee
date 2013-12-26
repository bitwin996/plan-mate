'use strict'

angular.module('planMateApp')
  .controller 'AuthCtrl', [
    '$scope', 'baseUrl',
    ($scope, baseUrl) ->
      $scope.baseUrl = baseUrl
      $scope.awesomeThings = [
        'HTML5 Boilerplate'
        'AngularJS'
        'Karma'
      ]
  ]
