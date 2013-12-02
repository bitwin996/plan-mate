'use strict'

angular.module('planMateApp', [
  'ngCookies'
  'ngResource'
  'ngSanitize'
  'ngRoute'
  'route-segment'
  'view-segment'
])

  .config([
    '$routeSegmentProvider', '$routeProvider',
    ($routeSegmentProvider, $routeProvider) ->

      $routeSegmentProvider.options.autoLoadTemplates = true

      $routeSegmentProvider
        .when('/', 'main')

        .when('/plans/:id',            'detail.info')
        .when('/plans/:id/dates',      'detail.dates')
        .when('/plans/:id/comments',   'detail.comments')
        .when('/plans/:id/attendants', 'detail.attendants')

        .segment 'main',
          templateUrl: 'views/main.html'
          controller: 'MainCtrl'

        .segment 'detail',
          templateUrl: 'views/plans/detail.html'
          controller: 'PlansDetailCtrl'

        .within()
          .segment 'info',
            templateUrl: 'views/plans/detail/info.html'
            dependencies: ['id']
          .segment 'dates',
            templateUrl: 'views/plans/detail/dates.html'
            dependencies: ['id']
          .segment 'comments',
            templateUrl: 'views/plans/detail/comments.html'
            dependencies: ['id']
          .segment 'attendants',
            templateUrl: 'views/plans/detail/attendants.html'
            dependencies: ['id']

      $routeProvider.otherwise redirectTo: '/'

    ])

###
  .config(['$routeProvider', ($routeProvider) ->
    $routeProvider
      #.when '/plan-detail',
      #  templateUrl: 'views/plan-detail.html'
      #  controller: 'PlanDetailCtrl'
      .when '/',
        templateUrl: 'views/main.html'
        controller: 'MainCtrl'
      .otherwise
        redirectTo: '/'
  ])
###

