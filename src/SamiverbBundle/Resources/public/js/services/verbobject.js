(function() {
  angular.module('Samiverb').factory("VerbObjFactory", ['$http', '$q', function($http, $q){
    var verbObj = {};
    var suggestionsObj = {};
    var pronomList = ['mun', 'don', 'son', 'moai', 'doai', 'soai', 'mii', 'dii', 'sii'];
    var vAvailable = false;
    var sAvailable = false;

    var resetVAvail = function() {
      vAvailable = false;
    }
    var resetSAvail = function() {
      sAvailable = false;
    }
    var setVerbObj = function(newObj) {
      angular.copy(newObj, verbObj);
      vAvailable = true;
    }
    var setSuggestionsObj = function(newObj) {
      angular.copy(newObj, suggestionsObj);
      sAvailable = true;
    }

    return {
      requestVerbObj: function(path) {          
        return $http.get(path)
          .then(function(response) {
            setVerbObj(response.data);
            return response;
          }
          , function(response) {
            resetVAvail();
            return $q.reject(response);
          });
      },

      requestSuggestionsObj: function(path) {
        return $http.get(path)
          .then(function(response) {
            setSuggestionsObj(response.data);
            return response;
          }
          , function(response) {
            resetSAvail();
            return $q.reject(response);
          });
      },

      getVerbObj: function() {
        return verbObj;
      },

      getSuggestionsObj: function() {
        return suggestionsObj;
      },
      
      getTense: function(start, len) {
        if (vAvailable == true && start < verbObj['tenses'].length) {
          
          if (start + len >= verbObj['tenses'].length) {
            len = verbObj['tenses'].length - start;
          }

          var rowList = [];

          for (var i = start; i < start + len; i++) {
            rowList.push(verbObj['tenses'][i]['value']);
          };

          return rowList;
        }
      },

      getParadigm: function(col, start, len) {
        if (vAvailable == true && 
          col < pronomList.length && 
          start < verbObj['tenses'].length) 
        {

          if (start + len >= verbObj['tenses'].length) {
            len = verbObj['tenses'].length - start;
          }

          var rowList = [];
        
          for (var i = start; i < start + len; i++) {
            rowList.push(verbObj['tenses'][i]['paradigms'][col]);
          };

          return rowList;
        }
      },

      getPronom: function(idx) {
        return pronomList[idx];
      },
      
      isVerbAvailable: function() {
        return vAvailable;
      },

      isSuggestionsAvailable: function() {
        return sAvailable;
      },

      isChecked: function() {
        if (vAvailable == false) {
          return false;
        }
        return verbObj['check'];
      },

      isValid: function () {
        if (vAvailable == false) {
          return false;
        }
        return (verbObj['check'] && verbObj['valid']);
      },

      isInvalid: function() {
        if (vAvailable == false) {
          return false;
        }
        return (verbObj['check'] && !verbObj['valid']); 
      }
    };

  }]);
})();