'use strict'

angular.module('planMateApp')
  .controller 'PlansDetailCtrl', [
    '$scope', '$routeSegment', '$rootScope',
    ($scope, $routeSegment, $rootScope) ->

      #TODO move to Model service
      idIncluded = (arr, obj) ->
        for elem in arr
          return true if obj.id is elem.id
        return false

      deleteFromArray = (arr, obj) ->
        for elem,i in arr
          delete arr[i] if obj.id is elem.id
          return elem


      $rootScope.currentUser = id: 97, name: 'Current User'

      $rootScope.users = []
      for i in [1..60]
        $rootScope.users.push id:i, name:'User '+i

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

      $scope.dateProposals = [
          proposer: id: 47, name: 'User 47'
          date: new Date()
          availableUsers: [
              id: 48, name: 'User 48'
            ,
              id: 49, name: 'User 49'
          ]
          unavailableUsers: [
              id: 50, name: 'User 50'
            ,
              id: 51, name: 'User 51'
          ]
        ,
          proposer:
            id: 52, name: 'User 52'
          date: new Date()
          availableUsers: [
              id: 53, name: 'User 53'
            ,
              id: 54, name: 'User 54'
          ]
          unavailableUsers: [
              id: 55, name: 'User 55'
            ,
              id: 56, name: 'User 56'
          ]
      ]

      # for "Available" button
      $scope.canBeAvailable = (dateProposal) ->
        if idIncluded dateProposal.unavailableUsers, $rootScope.currentUser
          return true
        else if not idIncluded dateProposal.availableUsers, $rootScope.currentUser
          return true
        return false

      # for "Unavailable" button
      $scope.canBeUnavailable = (dateProposal) ->
        if idIncluded dateProposal.availableUsers, $rootScope.currentUser
          return true
        else if not idIncluded dateProposal.unavailableUsers, $rootScope.currentUser
          return true
        return false

      # initialize buttons
      for dateProposal in $scope.dateProposals
        dateProposal.canBeAvailable = $scope.canBeAvailable dateProposal
        dateProposal.canBeUnavailable = $scope.canBeUnavailable dateProposal


      $scope.comments = [
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

      $scope.attendants = [
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
        comment.user = $rootScope.currentUser

        #TODO post to server
        $scope.comments.unshift comment

        $scope.newComment = {}


      $scope.addToAvailable = (dateProposal) ->
        return unless $scope.canBeAvailable dateProposal

        #TODO post to server

        if idIncluded dateProposal.unavailableUsers, $rootScope.currentUser
          deleteFromArray dateProposal.unavailableUsers, $rootScope.currentUser
        dateProposal.availableUsers.push $rootScope.currentUser
        dateProposal.canBeAvailable = false
        dateProposal.canBeUnavailable = true

      $scope.addToUnavailable = (dateProposal) ->
        return unless $scope.canBeUnavailable dateProposal

        #TODO post to server

        if idIncluded dateProposal.availableUsers, $rootScope.currentUser
          deleteFromArray dateProposal.availableUsers, $rootScope.currentUser
        dateProposal.unavailableUsers.push $rootScope.currentUser
        dateProposal.canBeAvailable = true
        dateProposal.canBeUnavailable = false



      $scope.watch = ->
        console.log "watch"

      $scope.apply = ->
        console.log "apply"

  ]
