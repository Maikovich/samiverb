(function(){
  angular.module('Samiverb')

  .directive("conjugateForm", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/directives/frontpage/conjugate-form.html'
    };
  }])

  .directive("alertSuggestions", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/directives/alert/suggestions.html'
    };
  }])

  .directive("alertNotvalidated", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/directives/alert/notvalidated.html'
    };
  }])

  .directive("alertInvalid", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/directives/alert/invalid.html'
    };
  }])

  .directive("verbresult", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/directives/result/verbtable.html'
    };
  }])

  .directive("validateModal", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/directives/modal/validate.html'
    };
  }])

  .directive("revalidateModal", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/directives/modal/revalidate.html'
    };
  }]);
})();