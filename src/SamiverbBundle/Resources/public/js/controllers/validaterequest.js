(function() {
  angular.module('Samiverb').controller("ValidateRequestController", ['$scope', function($scope) {

    $scope.secondTry = function(id, path) {
      
      var deleteBtn = '#deleteRequest'+id.toString()
      
      if ($(deleteBtn).hasClass('btn-warning') == true) {
        
        $(deleteBtn).toggleClass('btn-warning btn-danger');
      
      } 
      else 
      {
        window.location.replace(path);
      }
    }

  }]);
})();