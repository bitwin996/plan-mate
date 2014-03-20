'use strict'

angular.module('planMateApp')
  .controller 'UsersPlansNewCtrl', [
    '$scope', 'Plan', '$http', '$location', '$rootScope', 'endpoint', 'Restangular', 'FlashAlertService',
    ($scope, Plan, $http, $location, $rootScope, endpoint, Restangular, FlashAlertService) ->

      $scope.submit = ->
        #Restangular.one('me').all('plans').post($scope.newPlan).then(
        #  (response) ->
        #    FlashAlertService.prepareRedirect()
        #    FlashAlertService.success "Registered a new plan."
        #    #$rootScope.$storage['plans-' + response.id] = response
        #    $location.path '/plans/' + response.id
        #)

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
