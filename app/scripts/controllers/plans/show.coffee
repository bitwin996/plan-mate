'use strict'

angular.module('planMateApp')
  .controller 'PlansShowCtrl', [
    '$scope', 'plan', 'FlashAlertService', '$rootScope',
    ($scope, plan, FlashAlertService, $rootScope) ->
      $scope.plan = plan

      $scope.attendants = plan.all('attendants')
      $scope.comments = plan.all('comments')
      $scope.schedules = plan.all('schedules')

      $scope.attend = ->
        $scope.attendants.post({}).then((response) ->
          FlashAlertService.success 'Success to join this plan.'
          $scope.attendants = response
        )

  ]
