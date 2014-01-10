'use strict'

angular.module('planMateApp')
  .service 'FlashAlertService', [
    '$rootScope',
    ($rootScope) ->
      @storage = {}

      @setStorage = (storage) ->
        unless storage instanceof Object
          throw 'Passed storage should be an object.'
        @oldStorage = angular.copy @storage
        @storage = storage

      @init = ->
        @storage.message = null
        @storage.type = null
        @storage.show = false

      @reset = ->
        @storage.message = null
        @storage.type = null
        @storage.show = false

      # type: success / info / warning / danger
      @update = (message, type = 'warning') ->
        @storage.message = message
        @storage.type = type
        @storage.show = true

      #$rootScope.$on 'routeSegmentChange', =>
      $rootScope.$on '$routeChangeStart', =>
        @reset()

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
