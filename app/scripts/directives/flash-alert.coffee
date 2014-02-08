'use strict'

angular.module('planMateApp')
  .service 'FlashAlertService', [
    '$rootScope', '$location',
    ($rootScope, $location) ->
      @storage = {}
      REDIRECT_COUNT = 1

      @setStorage = (storage) ->
        unless storage instanceof Object
          throw 'Passed storage should be an object.'
        @oldStorage = angular.copy @storage
        @storage = storage

      @init = ->
        @storage.message = null
        @storage.type = null
        @storage.show = false
        @storage.countFromRedirect = REDIRECT_COUNT

      @reset = ->
        if @storage.countFromRedirect >= REDIRECT_COUNT
          @storage.message = null
          @storage.type = null
          @storage.show = false
        else
          @storage.countFromRedirect++

      # type: success / info / warning / danger
      @update = (message, type = 'warning') ->
        @storage.message = message
        @storage.type = type
        @storage.show = true

      # Use this method only in $rootScope.$on('$routeChangeStart') and so on.
      @prepareRedirect = ->
        @storage.countFromRedirect = 0

      @success = (message) -> @update message, 'success'
      @info = (message) -> @update message, 'info'
      @warning = (message) -> @update message, 'warning'
      @danger = (message) -> @update message, 'danger'

      @error = @danger

      return @
  ]


angular.module('planMateApp')
  .directive 'flashAlert', [
    '$rootScope', 'FlashAlertService',
    ($rootScope, FlashAlertService) ->
      restrict: 'E'
      transclude: true
      scope:
        data: '='

      # <flash-alert data="flashAlert">: Use like this in HTML template
      template:
        '<div ng-class=\'["alert", "alert-" + data.type]\' ng-show="data.show">' +
        '<button type="button" class="close" ng-click="data.show = false" ng-init="data.displayed = true">&times;</button>' +
        "{{data.message}}" +
        '</div>'
  ]
