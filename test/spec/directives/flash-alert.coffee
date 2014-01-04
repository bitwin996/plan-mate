'use strict'

describe 'Directive: flashAlert', () ->

  # load the directive's module
  beforeEach module 'planMateApp'

  scope = {}

  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()

  it 'should make hidden element visible', inject ($compile) ->
    element = angular.element '<flash-alert></flash-alert>'
    element = $compile(element) scope
    expect(element.text()).toBe 'this is the flashAlert directive'
