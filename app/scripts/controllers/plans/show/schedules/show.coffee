'use strict'

angular.module('planMateApp')
  .controller 'PlansShowSchedulesShowCtrl', [
    '$scope', '$routeParams', '$location', 'apiPlanSchedule', 'apiResponse', 'PlanScheduleAttendant', 'AuthenticationService', 'FlashAlertService',
    ($scope, $routeParams, $location, apiPlanSchedule, apiResponse, PlanScheduleAttendant, AuthenticationService, FlashAlertService) ->
      # PlanSchedul
      #for planSchedule in $scope.$parent.planSchedules
      #  if planSchedule.id is parseInt($routeParams.planScheduleId)
      #    $scope.planSchedule = planSchedule

      $scope.plan = $scope.$parent.plan
      $scope.planSchedule = apiPlanSchedule.plan_schedule

      # PlanScheduleAttendants
      $scope.planScheduleAttendants = apiResponse.plan_schedule_attendants

      for user in apiResponse.users
        $scope.$parent.users[user.id] = user

      @currentUserId = AuthenticationService.getUserId()

      $scope.isOwner = $scope.plan.user_id is @currentUserId
      $scope.isAvailed = false
      for attendant in $scope.planScheduleAttendants
        console.log attendant.id, @currentUserId
        if attendant.id is @currentUserId
          $scope.isAvailed = true

      console.log 'IS_OWNER', $scope.isOwner, $scope.isAvailed

      $scope.avail = ->
        console.log 'AVAIL', $routeParams
        newAttendant = new PlanScheduleAttendant
          plan_id: $routeParams.planId
          plan_schedule_id: $routeParams.planScheduleId

        request = newAttendant.$save()
        request.then(
            (response) ->
              FlashAlertService.success 'Success to join this plan.'
              #$scope.setPlanAttendants response

              FlashAlertService.prepareRedirect()
              $location.path "/plans/"+$routeParams.planId+"/schedules/"
              #$location.replace()
          ,
            (response) ->
              FlashAlertService.error response.data.message
        )
  ]
