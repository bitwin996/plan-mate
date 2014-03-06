'use strict'

angular.module('planMateApp')
  .controller 'PlansShowCtrl', [
    '$scope', '$routeSegment', '$location', 'apiResponse', 'Plan', 'PlanAttendant', 'AuthenticationService', 'FlashAlertService',
    ($scope, $routeSegment, $location, apiResponse, Plan, PlanAttendant, AuthenticationService, FlashAlertService) ->

      $scope.routeSegment = $routeSegment
      #console.log $routeSegment.chain.slice(-1)[0].name

      $scope.planAttendants = null
      $scope.planComments = null
      $scope.planSchedules = null
      $scope.users ?= {}

      $scope.setPlanResponse = (response) ->
        plan = response.plan
        $scope.plan = plan

        $scope.planAttendants = response.plan_attendants
        #$scope.plan.attendants_count = response.plan_attendants.length
        for user in response.users
          $scope.users[user.id] = user

        userId = AuthenticationService.getUserId()

        $scope.isOwner = plan.user_id is userId

        $scope.isFixed = not not plan.date

        $scope.isAttended = false
        for attendant in response.plan_attendants
          if attendant.user_id is userId
            $scope.isAttended = true
            $scope.myPlanAttendantId = attendant.id

      $scope.setPlanResponse apiResponse


      #TODO remove
      $scope.setPlan = (plan) ->
        $scope.plan = plan
        $scope.isOwner = plan.user_id is AuthenticationService.getUserId()
        $scope.isFixed = not not plan.date
      $scope.setPlan apiResponse.plan

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
              #$scope.setPlanAttendants response
              $scope.setPlanResponse response
          ,
            (response) ->
              FlashAlertService.error response.data.message
        )

      $scope.unattend = ->
        return false unless $scope.myPlanAttendantId

        userId = AuthenticationService.getUserId()
        planAttendant = new PlanAttendant plan_id:$scope.plan.id, id:$scope.myPlanAttendantId

        console.log 'PLAN_ATTENDANT', planAttendant

        request = planAttendant.$delete()
        request.then(
            (response) ->
              FlashAlertService.success 'Success to cancel to attend.'
              $scope.setPlanResponse response
          ,
            (response) ->
              FlashAlertService.error response.data.message
        )

      $scope.fix = (date) ->
        plan = new Plan $scope.plan
        plan.date = date
        plan.$fix(
            (response) ->
              console.log 'SUCCESS', response

              #$scope.plan = response.plan
              $scope.setPlan response.plan

              FlashAlertService.prepareRedirect()
              FlashAlertService.success "Success to fix plan schedule."
              $location.path '/plans/'+$scope.plan.id
          ,
            (response) ->
              FlashAlertService.error response.data.message
        )

      $scope.cancelFixing = ->
        plan = new Plan $scope.plan
        plan.$cancelFixing(
            (response) ->
              console.log 'SUCCESS', response

              #$scope.plan = response.plan
              $scope.setPlan response.plan

              FlashAlertService.prepareRedirect()
              FlashAlertService.success "Success to cancel plan schedule."
              $location.path '/plans/'+$scope.plan.id
          ,
            (response) ->
              FlashAlertService.error response.data.message
        )

  ]
