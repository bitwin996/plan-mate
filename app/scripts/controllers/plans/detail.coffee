'use strict'

angular.module('planMateApp')
  .controller 'PlansDetailCtrl', [
    '$scope', '$routeSegment',
    ($scope, $routeSegment) ->

      $scope.$routeSegment = $routeSegment

      $scope.plan =
        id: 7
        date: new Date()
        planner:
          id: 17
          name: 'Test organizer'
        location:
          id: 27
          name: 'Test Building'
        dates: []
        _comments: []
        comments: [
            user:
              id: 37
              name: 'User 37'
            body: 'Test comment 37 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
          ,
            user:
              id: 38
              name: 'User 38'
            body: 'Test comment 38'
        ]
        attendants: []

      $scope.newComment = {}
      $scope.postComment = (newComment) ->
        comment = angular.copy newComment

        #TODO create account service
        comment.user = id: 37, name: 'User 37'

        #TODO post to server
        $scope.plan.comments.push comment

        $scope.newComment = {}

      $scope.watch = ->
        console.log "watch"

      $scope.apply = ->
        console.log "apply"

  ]
