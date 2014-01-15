'use strict'

angular.module('planMateApp')
  .controller 'UsersPlansCtrl', [
    '$scope', 'plans',
    ($scope, plans) ->
      $scope.plans = plans

      ###
      $scope.plans = new Plan
      $scope.plans.$find(user_id:'me').
        success((response) ->
          console.log $scope.plans
        ).
        error (response) ->
          FlashAlertService.error "Couldn't connect the remote server"
      ###
  ]
