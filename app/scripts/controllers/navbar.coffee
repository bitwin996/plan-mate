'use strict'

angular.module('planMateApp')
  .controller 'NavbarCtrl', [
    '$scope', '$location', 'AuthenticationService',
    ($scope, $location, AuthenticationService) ->

      $scope.isCollapsed = true

      collapse = ->
        $scope.isCollapsed = true

      $scope.toggle = ->
        $scope.isCollapsed = not $scope.isCollapsed

      $scope.$on '$routeChangeSuccess', ->
        collapse()

      $scope.isActive = (path) ->
        if path is '/'
          $location.path() is '/'
        else
          $location.path().substr(0, path.length) is path

      $scope.logout = ->
        AuthenticationService.logout ->
          $location.path '/plans/7'  #TODO
  ]
