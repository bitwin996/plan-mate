'use strict'

describe 'Service: Plan', () ->

  # load the service's module
  beforeEach module 'planMateApp'

  # instantiate service
  Plan = {}
  beforeEach inject (_Plan_) ->
    Plan = _Plan_

  it 'should do something', () ->
    expect(!!Plan).toBe true
