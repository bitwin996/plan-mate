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

      .when('/users/:userId/plans',      'users-plans')
      .when('/mypage/plans',             'mypage-plans')
      .when('/mypage/plans/new',         'mypage-plans-new')

      .when('/plans/:planId',            'plans-show.info')
      .when('/plans/:planId/attendants', 'plans-show.attendants')
      .when('/plans/:planId/comments',   'plans-show.comments')
      .when('/plans/:planId/schedules',  'plans-show.schedules')
      .when('/plans/:planId/schedules/:planScheduleId',  'plans-show.schedules-show')


      .segment 'main',
        templateUrl: 'views/main.html'
        controller: 'MainCtrl'

      .segment 'login',
        templateUrl: 'views/auth/login.html'
        controller: 'AuthCtrl'

      .segment 'mypage-plans',
        templateUrl: 'views/users/plans.html'
        controller: 'UsersPlansCtrl'
        resolve:
          #TODO replace with $resource
          plansResponse: [
            'Restangular',
            (Restangular) ->
              #Restangular.one('me').all('plans').getList()
              Restangular.one('me').getList('plans')
          ]

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

        #.within()
        .segment 'schedules-show',
          templateUrl: 'views/plans/show/schedules/show.html'
          controller: 'PlansShowSchedulesShowCtrl'
          dependencies: ['planId', 'planScheduleId']
          resolve:
            #apiPlan: [
            #  'Plan', '$routeParams',
            #  (Plan, $routeParams) ->
            #    request = Plan.get
            #      planId: $routeParams.planId
            #    console.log 'plan', request
            #    request.$promise
            #]
            #TODO get schedule and attendants once
            apiPlanSchedule: [
              'PlanSchedule', '$routeParams',
              (PlanSchedule, $routeParams) ->
                request = PlanSchedule.get
                  planId: $routeParams.planId
                  planScheduleId: $routeParams.planScheduleId
                request.$promise
            ]
            apiResponse: [
              'PlanScheduleAttendant', '$routeParams',
              (PlanScheduleAttendant, $routeParams) ->
                request = PlanScheduleAttendant.query
                  planId: $routeParams.planId
                  planScheduleId: $routeParams.planScheduleId
                request.$promise
            ]
          resolveFailed:
            #apiPlan: apiResolveFailed
            apiPlanSchedule: apiResolveFailed
            apiResponse: apiResolveFailed


    $routeProvider.otherwise redirectTo: '/'
]
