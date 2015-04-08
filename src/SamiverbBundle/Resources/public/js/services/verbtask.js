(function() {
  angular.module('Samiverb').factory("VerbTaskFactory", ['$http', '$q', '$timeout', 'VerbObjFactory', function($http, $q, $timeout, VerbObjFactory){

    var conjugations_section = '#conjugations'
    var conjugateBtn = '#conjugate-btn';
    var validateBtn = '#validate-btn';
    var requestDir = 'request';
    var suggestionsDir = 'suggestions';
    var validateDir = 'validate';
    var protectedMode = true;
    var requestedVerb = false;
    var submitted = false;
    var is_error = false;

    var setError   = function() { is_error = true; }
    var resetError = function() { is_error = false; }

    var errorCallback = function(button) {
      setError();
      $(button).toggleClass('btn-primary btn-danger');

      $timeout(function() {
        $(button).toggleClass('btn-danger btn-primary');
        resetError();
      }, 3000);
    }


    return {
      turnOffProtectedMode: function() {
        scrollToTarget(conjugations_section);
        protectedMode = false;
      },

      isProtectedMode: function() {
        return protectedMode;
      },

      isSubmitted: function() {
        return submitted;
      },

      isError: function() {
        return is_error;
      },

      getRequestedVerb: function() {
        if (requestedVerb != false) {
          return requestedVerb;
        }
      },

      requestVerb: function(verb) {
        var l = Ladda.create( document.querySelector(conjugateBtn));
        var todo = 2;
        requestedVerb = verb;
        submitted = false;

        l.start();
        VerbObjFactory.requestVerbObj(requestDir+'/'+verb).
          then(function(response) {
            requestedVerb = response.data['name'];
          },
          function(error) {
            requestedVerb = error.data;
          }).
          finally(function() {
            if (--todo == 0) {
              l.stop();
              $('#conjug').fadeIn();
              scrollToTarget(conjugations_section);
            }
          });

        VerbObjFactory.requestSuggestionsObj(suggestionsDir+'/'+verb).
          finally(function() {
            if (--todo == 0) {
              l.stop();
              $('#conjug').fadeIn();
              scrollToTarget(conjugations_section);
            }
          });
      },

      newVerbRequest: function(verb) {
        var l = Ladda.create( document.querySelector(conjugateBtn));
        requestedVerb = verb;
        submitted = false;

        l.start();
        VerbObjFactory.requestVerbObj(requestDir+'/'+verb).
          then(function(response) {
            requestedVerb = response.data['name'];
          },
          function(error) {
            requestedVerb = error.data;
          }).
          finally(function() {
            l.stop();
            scrollToTarget(conjugations_section);
          });
      },

      validateFormSubmit: function(formData, mode, csrf_token) {
        var validate_btn = document.querySelector(validateBtn+mode.toString());

        var req = {
          method: 'POST',
          url: validateDir,
          headers: {
            'Content-Type': undefined,
            'X-CSRF-Token': csrf_token
          },
          data: formData,
        }

        var l = Ladda.create( validate_btn );
        
        l.start();
        $http(req).
          success(function(response) {
            submitted = true;
            return response;
          }).
          error(function(error) {
            errorCallback( validate_btn );
            return error;
          }).
          finally(function() {
            l.stop();
          });
      }
    };

  }]);    
})();