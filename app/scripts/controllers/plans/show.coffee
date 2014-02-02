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
        $scope.attendants.post().then((response) ->
          #console.log 'SUCCESS', response, angular.copy(response)
          FlashAlertService.update 'Success to attending application.', 'info'
        )

      ###
        $scope.plan.all('attendants').post().then(
              #TODO fix to success()

              console.log 'NEW GET'
              $scope.plan.get().then((response) ->
                console.log 'SUCCESS 2', response
                $scope.$parent.plan = response
              )

              #for k,v in response.originalElement
              #  $scope.plan.k = v
              #$scope.plan = response
            ,
              null
          )
      ###
  ]
