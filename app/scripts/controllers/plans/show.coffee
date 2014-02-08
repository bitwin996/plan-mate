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
        #TODO attendants_count
        $scope.plan.attendants_count = $scope.planAttendants.length
        for user in response.users
          $scope.users[user.id] = user

      $scope.setPlanComments = (response) ->
        $scope.planComments = response.plan_comments
        #TODO comments_count
        $scope.plan.comments_count = $scope.planComments.length
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
