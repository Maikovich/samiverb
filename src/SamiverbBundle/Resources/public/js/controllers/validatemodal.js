(function() {
  angular.module('Samiverb').controller("ValidateModalController", ['$http', '$q', '$scope', 'VerbObjFactory', 'VerbTaskFactory', function($http, $q, $scope, VerbObjFactory, VerbTaskFactory) {

    $scope.validateForm = {};
    $scope.token = "";

    $scope.generateCrsf = function(mode) {
      return $http.get(VerbTaskFactory.getApiRoot() + '/crsf/' + mode) 
        .then(function(response) {
          $scope.token = response.data;
        });
    };

    $scope.$watch(VerbObjFactory.isVerbAvailable, function(){
      $scope.verb = VerbObjFactory.getVerbObj();
    });

    $scope.$watch(VerbObjFactory.isSuggestionsAvailable, function() {
      $scope.suggestions = VerbObjFactory.getSuggestionsObj();
    });

    $scope.requestNewVerb = function(verb) {
      return VerbTaskFactory.newVerbRequest(verb);
    };

    $scope.validateForm.submit = function(mode) {
      $scope.validateForm.verb = $scope.verb['name'];
      $scope.validateForm.mode = mode;

      return VerbTaskFactory.validateFormSubmit($scope.validateForm, mode, $scope.token);
    };

    $scope.validateForm.isSubmitted = function() {
      return VerbTaskFactory.isSubmitted();
    };

    $scope.validateForm.isError = function() {
      return VerbTaskFactory.isError();
    };


  }]);
})();