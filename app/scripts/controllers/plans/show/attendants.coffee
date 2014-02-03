'use strict'

angular.module('planMateApp')
  .controller 'PlansShowAttendantsCtrl', [
    '$scope', 'attendants',
    ($scope, attendants) ->
      $scope.attendants = $scope.$parent.attendants = attendants
  ]
