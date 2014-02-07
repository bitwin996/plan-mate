'use strict'

angular.module('planMateApp')
  .controller 'UsersPlansNewCtrl', [
    '$scope', '$http', '$location', '$rootScope', 'endpoint', 'Restangular', 'FlashAlertService',
    ($scope, $http, $location, $rootScope, endpoint, Restangular, FlashAlertService) ->

      $scope.submit = ->
        Restangular.one('me').all('plans').post($scope.newPlan).then(
          (response) ->
            FlashAlertService.prepareRedirect()
            FlashAlertService.success "Registered a new plan."
            #$rootScope.$storage['plans-' + response.id] = response
            $location.path '/plans/' + response.id
        )

  ]
