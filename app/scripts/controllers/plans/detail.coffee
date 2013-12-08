'use strict'

angular.module('planMateApp')
  .controller 'PlansDetailCtrl', [
    '$scope', '$routeSegment', '$rootScope',
    ($scope, $routeSegment, $rootScope) ->

      $rootScope.currentUser = id: 97, name: 'Current User'

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

        date_proposals: [
            proposer:
              id: 47
              name: 'User 47'
            date: new Date()
            supporters: []
          ,
            proposer:
              id: 48
              name: 'User 48'
            date: new Date()
            supporters: []
        ]

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

        attendants: [
            id: 37
            name: 'User 37'
          ,
            id: 38
            name: 'User 38'
        ]

      $scope.newComment = {}
      $scope.postComment = (newComment) ->
        comment = angular.copy newComment

        #TODO create account service
        comment.user = id: 37, name: 'User 37'

        #TODO post to server
        $scope.plan.comments.push comment

        $scope.newComment = {}

      $scope.isSupported = (dateProposal, user) ->
        for supporter in dateProposal.supporters
          return true if user.id is supporter.id
        return false

      $scope.enable = (dateProposal) ->
        unless $scope.isSupported dateProposal $rootScope.current_user
          #TODO post to server

          $scope.dateProposals.push $rootScope.current_user



      $scope.watch = ->
        console.log "watch"

      $scope.apply = ->
        console.log "apply"

  ]
