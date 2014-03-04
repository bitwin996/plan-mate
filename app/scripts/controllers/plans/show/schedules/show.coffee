'use strict'

angular.module('planMateApp')
  .controller 'PlansShowSchedulesShowCtrl', [
    '$scope', '$routeParams', '$location', '$routeSegment', 'apiResponse', 'PlanSchedule', 'PlanScheduleAttendant', 'AuthenticationService', 'FlashAlertService',
    ($scope, $routeParams, $location, $routeSegment, apiResponse, PlanSchedule, PlanScheduleAttendant, AuthenticationService, FlashAlertService) ->

      $scope.planSchedule = apiResponse.plan_schedule

      $scope.planScheduleAttendants = apiResponse.plan_schedule_attendants

      for user in apiResponse.users
        $scope.$parent.users[user.id] = user

      @currentUserId = AuthenticationService.getUserId()

      $scope.isAvailed = false
      for attendant in $scope.planScheduleAttendants
        if attendant.user_id is @currentUserId
          $scope.isAvailed = true

      $scope.avail = ->
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
