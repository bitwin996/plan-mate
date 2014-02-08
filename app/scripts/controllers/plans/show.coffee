'use strict'

angular.module('planMateApp')
  .controller 'PlansShowCtrl', [
    '$scope', 'planResponse', 'FlashAlertService', 'PlanAttendant',
    ($scope, planResponse, FlashAlertService, PlanAttendant) ->
      $scope.plan = planResponse.plan

      $scope.planAttendants = null
      $scope.planComments = null
      $scope.planSchedules = null
      $scope.users ?= {}

      #$scope.pickupUser = (userId) ->
      #  for user in $scope.users
      #    if user.id is userId
      #      return user

      $scope.attend = ->
        planAttendant = new PlanAttendant plan_id:$scope.plan.id

        request = planAttendant.$save()
        request.then(
            (response) ->
              FlashAlertService.success 'Success to join this plan.'
              $scope.planAttendants = response.plan_attendants

              for user in response.users
                $scope.users[user.id] = user
          ,
            (response) ->
              FlashAlertService.error response.data.message
        )

  ]
