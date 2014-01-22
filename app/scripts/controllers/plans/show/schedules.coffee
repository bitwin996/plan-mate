'use strict'

angular.module('planMateApp')
  .controller 'PlansShowSchedulesCtrl', [
    '$scope', '$timeout', 'schedules',
    ($scope, $timeout, schedules) ->

      floorTime = (momentObj) ->
        momentObj.hours(0).minutes(0).seconds(0)

      isEqualDate = (date1, date2) ->
        t1 = moment date1
        t2 = moment date2
        t1.year() is t2.year() and t1.dayOfYear() is t2.dayOfYear()


      $scope.schedules = schedules

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

      $scope.disabled = (schedule, mode) ->
        for schedule in $scope.schedules
          return true if isEqualDate date, schedule.date
        false

      $scope.addSchedule = (schedule) ->
        _schedule = angular.copy schedule
        #_schedule.canBeAvailable = $scope.canBeAvailable dp
        #_schedule.canBeUnavailable = $scope.canBeUnavailable dp
        $scope.schedules.push _schedule
  ]
