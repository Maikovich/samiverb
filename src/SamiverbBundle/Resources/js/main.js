(function() {

  angular.module('Samiverb', [])
    .config(function($interpolateProvider){
      $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
    })
    .config(["$provide", function ($provide) {
        $provide.value("apiRoot", $("#linkApiRoot").attr("href"));
    }]);

})();