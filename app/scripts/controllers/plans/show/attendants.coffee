'use strict'

angular.module('planMateApp')
  .controller 'PlansShowAttendantsCtrl', [
    '$scope', 'attendants',
    ($scope, attendants) ->
      $scope.attendants = $scope.$parent.attendants = attendants

      $scope.attend = ->
        $scope.attendants.post().then((response) ->
          console.log 'SUCCESS', response
          FlashAlertService.update 'Success to attending application.', 'info'
          $scope.attendants.push response
        )
  ]
