'use strict'

angular.module('planMateApp')
  .controller 'PlansShowSchedulesCtrl', [
    '$scope', '$timeout', 'apiResponse', 'FlashAlertService', 'PlanSchedule',
    ($scope, $timeout, apiResponse, FlashAlertService, PlanSchedule) ->

      $scope.$parent.setPlanSchedules apiResponse


      floorTime = (momentObj) ->
        momentObj.hours(0).minutes(0).seconds(0)

      isEqualDate = (date1, date2) ->
        t1 = moment date1
        t2 = moment date2
        t1.year() is t2.year() and t1.dayOfYear() is t2.dayOfYear()

      $scope.datePicker =
        min: floorTime(moment()).toDate()
        max: floorTime(moment()).add('years', 1).toDate()
        opened: false
        dateOptions:
          'year-format': "'yy'"
          'starting-day': 1

      $scope.open = ->
        $timeout ->
          $scope.datePicker.opened = true

      # disable existing dates
      $scope.disabled = (schedule, mode) ->
        for planSchedule in $scope.$parent.planSchedules
          return true if isEqualDate date, planSchedule.date
        false

      $scope.addSchedule = ->
        #TODO
        params = angular.extend plan_id:$scope.plan.id, $scope.newSchedule
        #params = angular.copy $scope.newSchedule
        planSchedule = new PlanSchedule params
        console.log 'PLAN_SCHEDULE', planSchedule

        request = planSchedule.$save()
        request.then(
            (response) ->
              console.log 'SUCCESS', response
              FlashAlertService.success 'Success to add a new schedule.'
              $scope.setPlanSchedules response
              $scope.newSchedule = {}
          ,
            (response) ->
              FlashAlertService.error response.data.message
        )

        ###
        _schedule = angular.copy schedule
        #_schedule.canBeAvailable = $scope.canBeAvailable dp
        #_schedule.canBeUnavailable = $scope.canBeUnavailable dp
        $scope.schedules.post($scope.newSchedule).then(
            (response) ->
              console.log response
          ,
            (response) ->
              FlashAlertService.error 'Fail to add a schedule.'
        )
        $scope.schedules.push _schedule
        ###
  ]
