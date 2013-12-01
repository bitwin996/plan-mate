'use strict'

angular.module('planMateApp')
  .controller 'PlanDetailCtrl', ['$scope', ($scope) ->

    $scope.plan =
      organizer:
        id: 17
        name: 'Test organizer'
      place:
        id: 27
        name: 'Test Building'

    $scope.watch = ->
      console.log "watch"

    $scope.apply = ->
      console.log "apply"
  ]
