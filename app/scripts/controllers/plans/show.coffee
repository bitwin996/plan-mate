'use strict'

angular.module('planMateApp')
  .controller 'PlansShowCtrl', [
    '$scope', '$routeSegment', 'apiResponse', 'Plan', 'PlanAttendant', 'AuthenticationService', 'FlashAlertService',
    ($scope, $routeSegment, apiResponse, Plan, PlanAttendant, AuthenticationService, FlashAlertService) ->
      $scope.plan = apiResponse.plan

      $scope.planAttendants = null
      $scope.planComments = null
      $scope.planSchedules = null
      $scope.users ?= {}

      $scope.isOwner = $scope.plan.user_id is AuthenticationService.getUserId()
      $scope.isFixed = not not $scope.plan.date

      $scope.routeSegment = $routeSegment
      #console.log $routeSegment.chain.slice(-1)[0].name

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

      $scope.setPlanSchedules = (response) ->
        $scope.planSchedules = response.plan_schedules
        #$scope.plan.schedules_count = $scope.planSchedules.length

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

      $scope.fix = (date) ->
        plan = new Plan $scope.plan
        plan.date = date
        console.log 'PLAN', plan
        plan.$fix(
            (response) ->
              console.log 'SUCCESS', response
              FlashAlertService.success "Success to fix plan schedule."
          ,
            (response) ->
              FlashAlertService.error response.data.message
        )

  ]
