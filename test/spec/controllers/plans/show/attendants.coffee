'use strict'

describe 'Controller: PlansShowAttendantsCtrl', () ->

  # load the controller's module
  beforeEach module 'planMateApp'

  PlansShowAttendantsCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    PlansShowAttendantsCtrl = $controller 'PlansShowAttendantsCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', () ->
    expect(scope.awesomeThings.length).toBe 3
