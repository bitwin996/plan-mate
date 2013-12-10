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

      today = (obj = null) -> moment(obj).hours(0).minutes(0).seconds(0)

      floorTime = (momentObj) ->
        momentObj.hours(0).minutes(0).seconds(0)


      isEqualDate = (date1, date2) ->
        a = moment date1
        b = moment date2
        a.year() is b.year() and a.dayOfYear() is b.dayOfYear()

      # constants in each controller
      #$scope.dateFormat = 'dd MMM yyyy'
      #$scope.timeFormat = 'hh:mm:ss a'

      # date picker
      $scope.datePicker =
        config:
          min: floorTime(moment()).toDate()
          max: floorTime(moment()).add('years', 1).toDate()
          opened: false
          dateOptions:
            'year-format': "'yy'"
            'starting-day': 1
        open: ->
          $timeout ->
            $scope.datePicker.config.opened = true

        disabled: (date, mode) ->
          for dateProposal in $scope.dateProposals
            return true if isEqualDate date, dateProposal.date
          false


      $rootScope.currentUser = id: 97, name: 'Current User'

      $rootScope.users = []
      for i in [1..60]
        $rootScope.users.push id:i, name:'User '+i

      $scope.$routeSegment = $routeSegment

      $scope.plan =
        id: 7
        date: floorTime(moment()).toDate()
        planner:
          id: 17
          name: 'Test organizer'
        location:
          id: 27
          name: 'Test Building'

      $scope.dateProposals = [
          proposer: id: 47, name: 'User 47'
          date: floorTime(moment()).add('days', 5).toDate()
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
          date: floorTime(moment()).add('days', 2).toDate()
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
