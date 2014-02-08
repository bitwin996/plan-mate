'use strict'

angular.module('planMateApp')
  .controller 'PlansShowCommentsCtrl', [
    '$scope', 'apiResponse', 'PlanComment', 'FlashAlertService',
    ($scope, apiResponse, PlanComment, FlashAlertService) ->
      $scope.$parent.setPlanComments apiResponse

      a = {c:1}
      b = {d:2}
      c = angular.extend a, b
      console.log 'CALC', a,b,c

      $scope.postComment = ->
        params = angular.extend plan_id:$scope.plan.id, $scope.newComment
        planComment = new PlanComment params

        request = planComment.$save()
        request.then(
            (response) ->
              FlashAlertService.success 'Success to post a new comment.'
              $scope.setPlanComments response
              $scope.newComment = {}
          ,
            (response) ->
              FlashAlertService.error response.data.message
        )

  ]
