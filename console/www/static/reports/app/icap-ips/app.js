// the main module of the application
var reportApp = angular.module("reportApp", [
    'ngRoute',
    'ngMaterial',
    'md.data.table',
    'reportControllers'
]);

// enable angular views
reportApp.config(['$routeProvider', function($routeProvider) {
    $routeProvider.
    when('/list', {
       templateUrl: 'list.html',
       controller: 'ListCtrl'
    }).
    when('/list/:item', {
       templateUrl: 'detail.html',
       controller: 'DetailCtrl'
    }).
    when('/list/:item/:domain', {
      templateUrl: 'domain.html',
      controller: 'DomainCtrl'
    }).
    when('/log', {
       templateUrl: 'log.html',
       controller: 'LogCtrl'
    }).
    otherwise({
       redirectTo: '/list'
   });
}]);


// add some filters
reportApp.filter('bytes', function() {
    return function(bytes) {
        if (isNaN(parseFloat(bytes)) || !isFinite(bytes) || bytes == 0) return '0';
        var units = {1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'},
        measure, floor, precision;
        if (bytes > 1099511627775) {
            measure = 4;
        } else if (bytes > 1048575999 && bytes <= 1099511627775) {
            measure = 3;
        } else if (bytes > 1024000 && bytes <= 1048575999) {
            measure = 2;
        } else if (bytes <= 1024000) {
            measure = 1;
        }
        floor = Math.floor(bytes / Math.pow(1024, measure)).toString().length;
        if (floor > 3) {
            precision = 0
        } else {
            precision = 3 - floor;
        }
        return (bytes / Math.pow(1024, measure)).toFixed(precision) + units[measure];
    }
});

reportApp.filter('duration', function() {
    return function(duration) {

        var seconds = Math.floor(duration / 1000);
        if (seconds == 0){
            return duration + " ms"
        }
        
        var minutes = Math.floor(duration / 60000);
        if (minutes == 0){
            return seconds + " s"
        }

        var hours = Math.floor(minutes / 60);
        if (hours == 0){
            return minutes + " min"
        }
        return hours + " h"
    }
});
