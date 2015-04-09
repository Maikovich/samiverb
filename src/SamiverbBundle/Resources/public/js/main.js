(function() {

  angular.module('Samiverb', [])
    .config(function($interpolateProvider){
      $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
    });

})();