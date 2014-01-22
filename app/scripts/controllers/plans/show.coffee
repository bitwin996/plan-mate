'use strict'

angular.module('planMateApp')
  .controller 'PlansShowCtrl', [
    '$scope', 'plan', 'FlashAlertService',
    ($scope, plan, FlashAlertService) ->
      $scope.plan = plan

      $scope.attend = ->
        $scope.plan.customPOST({}, 'attend').then(
            (response) ->
              #TODO fix to success()
              FlashAlertService.update 'Success to attending application.', 'info'
              $scope.plan = response
          ,
            (response) ->
              FlashAlertService.error response.data.message
          )
  ]
