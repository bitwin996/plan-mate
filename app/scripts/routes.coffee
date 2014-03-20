'use strict'

app = angular.module('planMateApp')

app.config [
  '$routeSegmentProvider', '$routeProvider',
  ($routeSegmentProvider, $routeProvider) ->

    $routeSegmentProvider.options.autoLoadTemplates = true

    apiResolveFailed = [
      'FlashAlertService', (FlashAlertService) ->
        FlashAlertService.prepareRedirect()
        FlashAlertService.error 'Failed to get data from server.'
    ]

    $routeSegmentProvider
      .when('/', 'main')

      .when('/auth/login', 'login')
      .when('/auth/login-complete', 'login-complete')

      .when('/users/:userId/plans',      'users-plans')
      .when('/mypage/plans',             'mypage-plans')
      .when('/mypage/plans/new',         'mypage-plans-new')

      .when('/plans/:planId',            'plans-show.info')
      .when('/plans/:planId/attendants', 'plans-show.attendants')
      .when('/plans/:planId/comments',   'plans-show.comments')
      .when('/plans/:planId/schedules',  'plans-show.schedules')
      .when('/plans/:planId/schedules/:planScheduleId',  'plans-show.schedules.show')


      .segment 'main',
        templateUrl: 'views/main.html'
        controller: 'MainCtrl'

      .segment 'login',
        templateUrl: 'views/auth/login.html'
        controller: 'AuthCtrl'

      .segment 'login-complete',
        controller: 'AuthLoginCompleteCtrl'
        resolve:
          auth: [
            '$location', 'AuthenticationService',
            ($location, AuthenticationService) ->
              AuthenticationService.update()
              $location.path '/'
          ]

      .segment 'mypage-plans',
        templateUrl: 'views/users/plans.html'
        controller: 'UsersPlansCtrl'
        resolve:
          apiResponse: [
            'Plan',
            (Plan) ->
              console.log 'BEFORE'
              request = Plan.query()
              request.$promise
          ]
        resolveFailed:
          apiResponse: apiResolveFailed

      .segment 'users-plans',
        templateUrl: 'views/users/plans.html'
        controller: 'UsersPlansCtrl'
        dependencies: ['userId']

      .segment 'mypage-plans-new',
        templateUrl: 'views/plans/new.html'
        controller: 'UsersPlansNewCtrl'

      #TODO .segment 'plans.show',
      .segment 'plans-show',
        templateUrl: 'views/plans/show.html'
        controller: 'PlansShowCtrl'
        resolve:
          apiResponse: [
            'Plan', '$routeParams',
            (Plan, $routeParams) ->
              request = Plan.get planId:$routeParams.planId
              request.$promise
          ]
        resolveFailed:
          apiResponse: apiResolveFailed

      .within()
        .segment 'info',
          templateUrl: 'views/plans/show/info.html'
          dependencies: ['planId']

        .segment 'attendants',
          templateUrl: 'views/plans/show/attendants.html'
          controller: 'PlansShowAttendantsCtrl'
          dependencies: ['planId']
          resolve:
            apiResponse: [
              'PlanAttendant', '$routeParams',
              (PlanAttendant, $routeParams) ->
                request = PlanAttendant.query planId:$routeParams.planId
                request.$promise
            ]
          resolveFailed:
            apiResponse: apiResolveFailed

        .segment 'comments',
          templateUrl: 'views/plans/show/comments.html'
          controller: 'PlansShowCommentsCtrl'
          dependencies: ['planId']
          resolve:
            apiResponse: [
              'PlanComment', '$routeParams',
              (PlanComment, $routeParams) ->
                request = PlanComment.query planId:$routeParams.planId
                request.$promise
            ]
          resolveFailed:
            apiResponse: apiResolveFailed

        .segment 'schedules',
          templateUrl: 'views/plans/show/schedules.html'
          controller: 'PlansShowSchedulesCtrl'
          dependencies: ['planId']
          resolve:
            apiResponse: [
              'PlanSchedule', '$routeParams',
              (PlanSchedule, $routeParams) ->
                request = PlanSchedule.query planId:$routeParams.planId
                request.$promise
            ]
          resolveFailed:
            apiResponse: apiResolveFailed

        #.segment 'schedules-show',
        .within()
          .segment 'show',
            templateUrl: 'views/plans/show/schedules/show.html'
            controller: 'PlansShowSchedulesShowCtrl'
            dependencies: ['planId', 'planScheduleId']
            resolve:
              apiResponse: [
                'PlanSchedule', '$routeParams',
                (PlanSchedule, $routeParams) ->
                  request = PlanSchedule.get
                    planId: $routeParams.planId
                    planScheduleId: $routeParams.planScheduleId
                  request.$promise
              ]
              #apiPlanScheduleAttendants: [
              #  'PlanScheduleAttendant', '$routeParams',
              #  (PlanScheduleAttendant, $routeParams) ->
              #    request = PlanScheduleAttendant.query
              #      planId: $routeParams.planId
              #      planScheduleId: $routeParams.planScheduleId
              #    request.$promise
              #]
            resolveFailed:
              apiResponse: apiResolveFailed
              #apiPlan: apiResolveFailed
              #apiPlanSchedule: apiResolveFailed


    $routeProvider.otherwise redirectTo: '/'
]
