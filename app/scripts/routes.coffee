'use strict'

app = angular.module('planMateApp')

app.config([
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

      .when('/users/:userId/plans', 'users-plans')
      .when('/me/plans',            'me-plans')
      .when('/me/plans/new',        'me-plans-new')

      .segment 'main',
        templateUrl: 'views/main.html'
        controller: 'MainCtrl'

      .segment 'login',
        templateUrl: 'views/auth/login.html'
        controller: 'AuthCtrl'

      .segment 'me-plans',
        templateUrl: 'views/users/plans.html'
        controller: 'UsersPlansCtrl'

      .segment 'users-plans',
        templateUrl: 'views/users/plans.html'
        controller: 'UsersPlansCtrl'
        dependencies: ['userId']

      .segment 'me-plans-new',
        templateUrl: 'views/plans/new.html'
        controller: 'UsersPlansNewCtrl'

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
