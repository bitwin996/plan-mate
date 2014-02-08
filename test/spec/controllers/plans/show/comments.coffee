'use strict'

describe 'Controller: PlansShowCommentsCtrl', () ->

  # load the controller's module
  beforeEach module 'planMateApp'

  PlansShowCommentsCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    PlansShowCommentsCtrl = $controller 'PlansShowCommentsCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', () ->
    expect(scope.awesomeThings.length).toBe 3
