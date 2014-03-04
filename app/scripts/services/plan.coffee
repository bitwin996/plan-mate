'use strict'

angular.module('planMateApp')
  .factory 'Plan', [
    '$resource', '$filter', 'endpoint',
    ($resource, $filter, endpoint) ->
      $resource endpoint + '/plans/:planId', planId:'@id',
        fix:
          method: 'PUT'
          transformRequest: (data, headersGetter) ->
            attrs = ['date']
            params = {}

            for attr in attrs
              params[attr] = data[attr]

            json = $filter('json') params
            return json
  ]

