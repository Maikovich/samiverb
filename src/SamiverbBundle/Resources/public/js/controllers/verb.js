(function() {
  angular.module('Samiverb').controller("VerbController", ['$scope', '$q', 'VerbObjFactory', 'VerbTaskFactory', function($scope, $q, VerbObjFactory, VerbTaskFactory){

    $scope.verb = "";

    $scope.requestVerbInfo = function() {
      VerbTaskFactory.requestVerb($scope.verb)
      
      $scope.verb = "";
    };

  }]);
})();