(function(){
  angular.module('Samiverb')

  .directive("conjugateForm", [ 'apiRoot', function(apiRoot) {
    return {
      restricted: 'AE',
      templateUrl: apiRoot + '/bundles/samiverb/directives/frontpage/conjugate-form.html'
    };
  }])

  .directive("alertSuggestions", [ 'apiRoot', function(apiRoot) {
    return {
      restricted: 'AE',
      templateUrl: apiRoot + '/bundles/samiverb/directives/alert/suggestions.html'
    };
  }])

  .directive("alertNotvalidated", [ 'apiRoot', function(apiRoot) {
    return {
      restricted: 'AE',
      templateUrl: apiRoot + '/bundles/samiverb/directives/alert/notvalidated.html'
    };
  }])

  .directive("alertInvalid", [ 'apiRoot', function(apiRoot) {
    return {
      restricted: 'AE',
      templateUrl: apiRoot + '/bundles/samiverb/directives/alert/invalid.html'
    };
  }])

  .directive("verbresult", [ 'apiRoot', function(apiRoot) {
    return {
      restricted: 'AE',
      templateUrl: apiRoot + '/bundles/samiverb/directives/result/verbtable.html'
    };
  }])

  .directive("validateModal", [ 'apiRoot', function(apiRoot) {
    return {
      restricted: 'AE',
      templateUrl: apiRoot + '/bundles/samiverb/directives/modal/validate.html'
    };
  }])

  .directive("revalidateModal", [ 'apiRoot', function(apiRoot) {
    return {
      restricted: 'AE',
      templateUrl: apiRoot + '/bundles/samiverb/directives/modal/revalidate.html'
    };
  }]);
})();