(function() {
  angular.module('Samiverb')

  .directive("conjugateForm", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/views/frontpage/conjugate-form.html'
    };
  })

  .directive("alertSuggestions", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/views/alert/suggestions.html'
    };
  })

  .directive("alertNotvalidated", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/views/alert/notvalidated.html'
    };
  })

  .directive("alertInvalid", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/views/alert/invalid.html'
    };
  })

  .directive("verbresult", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/views/result/verbtable.html'
    };
  })

  .directive("validateModal", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/views/modal/validate.html'
    };
  })

  .directive("revalidateModal", function() {
    return {
      restricted: 'AE',
      templateUrl: '/bundles/samiverb/views/modal/revalidate.html'
    };
  });
})();