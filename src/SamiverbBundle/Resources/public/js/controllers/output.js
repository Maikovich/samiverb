(function() {
  angular.module('Samiverb').controller("OutputController", ['$scope', 'VerbObjFactory', 'VerbTaskFactory', function($scope, VerbObjFactory, VerbTaskFactory){

    $scope.$watch(VerbObjFactory.isVerbAvailable, function(){
      $scope.verb = VerbObjFactory.getVerbObj();
    });

    $scope.$watch(VerbObjFactory.isSuggestionsAvailable, function() {
      $scope.suggestions = VerbObjFactory.getSuggestionsObj();
    });

    $scope.isPossibleVerb = function() {
      return VerbObjFactory.isVerbAvailable();
    };

    $scope.isSuggestionsReady = function() {
       return VerbObjFactory.isSuggestionsAvailable();
    };

    $scope.getParadigm = function(col, start, len) {
      return VerbObjFactory.getParadigm(col, start, len);
    };

    $scope.getTense = function(start, len) {
      return VerbObjFactory.getTense(start, len);
    };

    $scope.getPronom = function(idx) {
      return VerbObjFactory.getPronom(idx);
    };

    $scope.range = function(min, max, step) {
      step = step || 1;
      var input = [];
      for (var i = min; i <= max; i += step) input.push(i);
      return input;
    };

    $scope.isValid = function() {
      return VerbObjFactory.isValid();
    };

    $scope.isInvalid = function() {
      return VerbObjFactory.isInvalid();
    };

    $scope.isChecked = function() {
      return VerbObjFactory.isChecked();
    };

    $scope.getRequestedVerb = function(verb) {
      return VerbTaskFactory.getRequestedVerb();
    }

    $scope.requestNewVerb = function(verb) {
      return VerbTaskFactory.newVerbRequest(verb);
    };

    $scope.turnOffProtectedMode = function() {
      return VerbTaskFactory.turnOffProtectedMode();
    };

    $scope.isProtectedMode = function() {
      return VerbTaskFactory.isProtectedMode();
    };

  }]);
})();