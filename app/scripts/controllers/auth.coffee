'use strict'

angular.module('planMateApp')
  .controller 'AuthCtrl', [
    '$scope', 'baseUrl',
    ($scope, baseUrl) ->
      $scope.baseUrl = baseUrl
  ]
