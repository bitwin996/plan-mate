'use strict'

angular.module('planMateApp')
  .controller 'PlansShowCtrl', [
    '$scope', 'apiResponse', 'FlashAlertService', 'PlanAttendant',
    ($scope, apiResponse, FlashAlertService, PlanAttendant) ->
      $scope.plan = apiResponse.plan

      $scope.planAttendants = null
      $scope.planComments = null
      $scope.planSchedules = null
      $scope.users ?= {}

      $scope.setPlanAttendants = (response) ->
        $scope.planAttendants = response.plan_attendants
        for user in response.users
          $scope.users[user.id] = user

      $scope.attend = ->
        planAttendant = new PlanAttendant plan_id:$scope.plan.id

        request = planAttendant.$save()
        request.then(
            (response) ->
              FlashAlertService.success 'Success to join this plan.'
              $scope.setPlanAttendants response
          ,
            (response) ->
              FlashAlertService.error response.data.message
        )

  ]
