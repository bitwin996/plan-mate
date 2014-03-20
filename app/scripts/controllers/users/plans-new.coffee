'use strict'

angular.module('planMateApp')
  .controller 'UsersPlansNewCtrl', [
    '$scope', '$location', 'Plan', 'FlashAlertService',
    ($scope, $location, Plan, FlashAlertService) ->

      $scope.submit = ->
        params = angular.extend $scope.newPlan
        plan = new Plan params

        request = plan.$save()
        request.then(
            (response) ->
              console.log 'SUCCESS', response
              FlashAlertService.success "Register a new plan."
              $scope.newPlan = {}
              $location.path '/plans/' + response.plan.id
          ,
            (response) ->
              FlashAlertService.error "Fail to register a new plan."
        )

  ]
