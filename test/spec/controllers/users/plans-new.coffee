'use strict'

describe 'Controller: UsersPlansNewCtrl', () ->

  # load the controller's module
  beforeEach module 'planMateApp'

  UsersPlansNewCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    UsersPlansNewCtrl = $controller 'UsersPlansNewCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', () ->
    expect(scope.awesomeThings.length).toBe 3
