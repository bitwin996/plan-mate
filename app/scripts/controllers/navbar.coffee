'use strict'

angular.module('planMateApp')
  .controller 'NavbarCtrl', [
    '$scope', '$location',
    ($scope, $location) ->

      $scope.isCollapsed = true

      $scope.$on '$routeChangeSuccess', ->
        $scope.isCollapsed = true

  ]
