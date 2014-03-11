'use strict'

angular.module('planMateApp')
  .controller 'NavbarCtrl', [
    '$scope', '$rootScope', '$location', 'AuthenticationService', 'FlashAlertService',
    ($scope, $rootScope, $location, AuthenticationService, FlashAlertService) ->

      $rootScope.navbar =
        isCollapsed: true

      #$scope.isCollapsed = true

      collapse = ->
        $rootScope.navbar.isCollapsed = true

      $scope.toggle = ->
        $rootScope.navbar.isCollapsed = not $rootScope.navbar.isCollapsed

      # change routing
      $scope.$on '$routeChangeSuccess', ->
        collapse()

      # for view
      $scope.isActive = (path) ->
        if path is '/'
          $location.path() is '/'
        else
          $location.path().substr(0, path.length) is path

      # Auth
      #$rootScope.navbar.isLoggedIn = AuthenticationService.storage.is_logged_in
      #$scope.isLoggedIn = AuthenticationService.isLoggedIn()

      $scope.logout = ->
        AuthenticationService.logout(->
          $rootScope.navbar.isCollapsed = true

          #FlashAlertService.prepareRedirect()
          FlashAlertService.info "Success to log out."

          #AuthenticationService.update()
          #$location.path '#/mypage/plans'
        )
  ]
