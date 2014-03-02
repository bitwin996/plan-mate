'use strict'

describe 'Service: planScheduleAttendant', () ->

  # load the service's module
  beforeEach module 'planMateApp'

  # instantiate service
  planScheduleAttendant = {}
  beforeEach inject (_planScheduleAttendant_) ->
    planScheduleAttendant = _planScheduleAttendant_

  it 'should do something', () ->
    expect(!!planScheduleAttendant).toBe true
