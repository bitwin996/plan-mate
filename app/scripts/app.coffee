'use strict'

angular.module('planMateApp', [
  'ngCookies'
  'ngResource'
  'ngSanitize'
  'ngRoute'
  'route-segment'
  'view-segment'
  'ui.bootstrap'
  'angularMoment'
])

  .constant('baseUrl', "$BASE_URL$")
  .constant('endpoint', "$BASE_URL$")

  .run([
    '$rootScope',
    ($rootScope) ->
      $rootScope.$on 'routeSegmentChange', ->
        $rootScope.resetFlash()

  ])

  .config([
    '$routeSegmentProvider', '$routeProvider',
    ($routeSegmentProvider, $routeProvider) ->

      $routeSegmentProvider.options.autoLoadTemplates = true

      $routeSegmentProvider
        .when('/', 'main')

        .when('/auth/login', 'login')

        .when('/plans/:planId',            'detail.info')
        .when('/plans/:planId/scheduling', 'detail.scheduling')
        .when('/plans/:planId/comments',   'detail.comments')
        .when('/plans/:planId/attendants', 'detail.attendants')

        .segment 'main',
          templateUrl: 'views/main.html'
          controller: 'MainCtrl'

        .segment 'login',
          templateUrl: 'views/auth/login.html'
          controller: 'AuthCtrl'

        .segment 'detail',
          templateUrl: 'views/plans/detail.html'
          controller: 'PlansDetailCtrl'

        .within()
          .segment 'info',
            templateUrl: 'views/plans/detail/info.html'
            dependencies: ['planId']
          .segment 'scheduling',
            templateUrl: 'views/plans/detail/scheduling.html'
            dependencies: ['planId']
          .segment 'comments',
            templateUrl: 'views/plans/detail/comments.html'
            dependencies: ['planId']
          .segment 'attendants',
            templateUrl: 'views/plans/detail/attendants.html'
            dependencies: ['planId']

      $routeProvider.otherwise redirectTo: '/'

    ])
