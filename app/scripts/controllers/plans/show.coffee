'use strict'

angular.module('planMateApp')
  .controller 'PlansShowCtrl', [
    '$scope', 'plan', 'FlashAlertService',
    ($scope, plan, FlashAlertService) ->
      $scope.plan = plan

      $scope.attend = ->
        console.log 'PLAN', $scope.plan
        $scope.plan.all('attendants').post().then(
            (response) ->
              console.log 'SUCCESS', response, angular.copy(response)
              #TODO fix to success()
              FlashAlertService.update 'Success to attending application.', 'info'
              $scope.plan = response
          ,
            (response) ->
              console.log 'ERROR', response
              FlashAlertService.error response.data.message
          )
  ]
