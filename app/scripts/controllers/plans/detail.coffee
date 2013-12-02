'use strict'

angular.module('planMateApp')
  .controller 'PlansDetailCtrl', [
    '$scope', '$routeSegment',
    ($scope, $routeSegment) ->

      $scope.$routeSegment = $routeSegment

      $scope.plan =
        id: 7
        date: new Date()
        planner:
          id: 17
          name: 'Test organizer'
        location:
          id: 27
          name: 'Test Building'
        dates: []
        comments: []
        attendants: []

      $scope.watch = ->
        console.log "watch"

      $scope.apply = ->
        console.log "apply"

  ]