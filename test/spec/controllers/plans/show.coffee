'use strict'

describe 'Controller: PlansShowCtrl', () ->

  # load the controller's module
  beforeEach module 'planMateApp'

  PlansShowCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    PlansShowCtrl = $controller 'PlansShowCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', () ->
    expect(scope.awesomeThings.length).toBe 3
