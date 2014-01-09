'use strict'

angular.module('planMateApp')
  .controller 'NavbarCtrl', [
    '$scope', '$location', '$http', 'endpoint', '$rootScope', 'FlashAlert',
    ($scope, $location, $http, endpoint, $rootScope, FlashAlert) ->

      $scope.isCollapsed = true

      $scope.$on '$routeChangeSuccess', ->
        $scope.isCollapsed = true

      $scope.isActive = (path) ->
        if path is '/'
          $location.path() is '/'
        else
          $location.path().substr(0, path.length) is path

      $scope.logout = ->
        request = $http.get endpoint + '/auth/logout'

        request.success (response) ->
          $location.path '/plans/7'  #TODO

        request.error (response) ->
          FlashAlert.update 'Fail to logout', 'danger'
  ]
