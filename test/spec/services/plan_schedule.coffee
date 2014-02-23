'use strict'

describe 'Service: planSchedule', () ->

  # load the service's module
  beforeEach module 'planMateApp'

  # instantiate service
  planSchedule = {}
  beforeEach inject (_planSchedule_) ->
    planSchedule = _planSchedule_

  it 'should do something', () ->
    expect(!!planSchedule).toBe true
