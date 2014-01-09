'use strict'

angular.module('planMateApp')
  .service 'FlashAlert', [
    '$rootScope',
    ($rootScope) ->
      @init = ->
        $rootScope.flashAlert =
          message: null
          type: null
          show: false

      # type: success / info / warning / danger
      @update = (message, type = 'warning') ->
        $rootScope.flashAlert =
          message: message
          type: type
          show: true

      @reset = ->
        $rootScope.flashAlert =
          message: null
          type: null
          show: false

      return @
  ]


angular.module('planMateApp')
  .directive 'flashAlert', [
    '$rootScope', 'FlashAlert',
    ($rootScope, FlashAlert) ->
      FlashAlert.init()

      $rootScope.$on 'routeSegmentChange', ->
        FlashAlert.reset()

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
