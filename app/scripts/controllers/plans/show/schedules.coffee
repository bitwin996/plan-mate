'use strict'

angular.module('planMateApp')
  .controller 'PlansShowSchedulesCtrl', [
    '$scope', '$timeout', 'apiResponse', 'FlashAlertService', 'PlanSchedule', 'PlanScheduleAttendant',
    ($scope, $timeout, apiResponse, FlashAlertService, PlanSchedule, PlanScheduleAttendant) ->

      $scope.$parent.setPlanSchedules apiResponse

      $scope.planScheduleAttendants ?= []


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
        open: ->
          $timeout ->
            $scope.datePicker.opened = true
        # disable existing dates
        disabled: (date, mode) ->
          for planSchedule in $scope.$parent.planSchedules
            return true if isEqualDate date, planSchedule.date
          false

      $scope.addPlanSchedule = ->
        params = angular.extend plan_id:$scope.plan.id, $scope.newSchedule
        params.date = moment(params.date).format 'YYYY-MM-DD'

        planSchedule = new PlanSchedule params

        request = planSchedule.$save()
        request.then(
            (response) ->
              console.log 'SUCCESS', response
              FlashAlertService.success 'Success to add a new schedule.'
              $scope.$parent.setPlanSchedules response
              $scope.newSchedule = {}
          ,
            (response) ->
              FlashAlertService.error response.data.message
        )
  ]
