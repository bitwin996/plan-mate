'use strict'

angular.module('planMateApp')
  .controller 'NavbarCtrl', [
    '$scope', '$location',
    ($scope, $location) ->

      $scope.isCollapsed = true

      $scope.$on '$routeChangeSuccess', ->
        $scope.isCollapsed = true

      $scope.getClass = (path) ->
        ###
        if path is '/'
          if $location.path() is '/'
            return 'active'
          else
            return ''

        if $location.path().substr(0, path.length) is path
          return 'active'
        else
          return ''
        ###

        if path is '/'
          return if $location.path() is '/' then 'active' else ''
        else if $location.path().substr(0, path.length) is path
          return 'active'
        ''

  ]
