'use strict'

angular.module('planMateApp')
  .controller 'PlansShowCtrl', [
    '$scope', 'plan',
    ($scope, plan) ->
      $scope.plan = plan
  ]
