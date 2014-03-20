'use strict'

angular.module('planMateApp')
  .controller 'UsersPlansCtrl', [
    '$scope', 'apiResponse',
    ($scope, apiResponse) ->
      console.log 'PLANS RESPONSE', apiResponse

      $scope.plans = apiResponse.plans

      $scope.users = {}
      for user in apiResponse.users
        $scope[user.id] = user

  ]
