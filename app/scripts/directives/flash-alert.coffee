'use strict'

angular.module('planMateApp')
  .directive 'flashAlert', [
    '$rootScope',
    ($rootScope) ->
      # $rootScope
      $rootScope.flash = message:null, type:null, show:false

      $rootScope.updateFlash = (message, type = 'warning') ->
        $rootScope.flash =
          message: message
          type: type
          show: true

      $rootScope.resetFlash = ->
        $rootScope.flash =
          message: null
          type: null
          show: false

      $rootScope.$on 'routeSegmentChange', ->
        $rootScope.resetFlash()


      restrict: 'E'
      transclude: true
      scope:
        data: '='

      template:
        '<div ng-class=\'["alert", "alert-" + data.type]\' ng-show="data.show">' +
        '<button type="button" class="close" ng-click="data.show = false" ng-init="data.displayed = true">&times;</button>' +
        "{{data.message}}" +
        '</div>'

  ]
