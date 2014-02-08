'use strict'

angular.module('planMateApp')
  .controller 'PlansShowAttendantsCtrl', [
    '$scope', 'apiResponse',
    ($scope, apiResponse) ->
      $scope.$parent.setPlanAttendants apiResponse
  ]
