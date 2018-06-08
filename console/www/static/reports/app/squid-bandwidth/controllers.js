//
//
//
var reportControllers = angular.module('reportControllers', []);

function compareBySize(a,b) {
  if (a.size > b.size)
    return -1;
  if (a.size < b.size)
    return 1;
  return 0;
}

function function_bytes(bytes) {
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

function function_duration(duration) {
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

reportControllers.controller('BandwidthCtrl', ['$scope', '$routeParams', '$http', function($scope, $routeParams, $http) {

    $http.get('data/meta.json').success(function(data) {
		$scope.meta = data;
    });

    $http.get('data/bandwidth/bandwidth.json').success(function(data) {
        $scope.days = {}
        $scope.hours = {}
        for (var i = 0; i < data.length; ++i) {
            if ($scope.days[data[i].day] == null) {
                var currentDate = new Date(data[i].day * 86400000);
                $scope.days[data[i].day] = {
                    'day' : currentDate,
                    'date' : data[i].day,
                    'duration' : 0,
                    'size' : 0,
                    'domains' : 0,
                    'users' : 0,
                };
            }

            if ($scope.hours[data[i].hour] == null) {
                $scope.hours[data[i].hour] = {
                    'hour' : data[i].hour,
                    'duration' : 0,
                    'size' : 0,
                    'domains' : 0,
                    'users' : 0,
                };
            }

            $scope.days[data[i].day].duration += data[i].duration;
            $scope.days[data[i].day].size += data[i].size;
            $scope.days[data[i].day].domains += data[i].domains;
            $scope.days[data[i].day].users += data[i].users;

            $scope.hours[data[i].hour].duration += data[i].duration;
            $scope.hours[data[i].hour].size += data[i].size;
            $scope.hours[data[i].hour].domains += data[i].domains;
            $scope.hours[data[i].hour].users += data[i].users;
        }
	});

	$http.get('data/meta.json').success(function(data) {
		$scope.meta = data;
    });
}]);

reportControllers.controller('BandwidthDateCtrl', ['$scope', '$routeParams', '$http', function($scope, $routeParams, $http) {
    $scope.date = $routeParams.date;

    $http.get('data/bandwidth/bandwidth.json').success(function(data) {
        $scope.hours = []
        for (var i = 0; i < data.length; ++i) {
            if (data[i].day == $scope.date) {
                $scope.hours.push(data[i]);
            }
        }
	});

	$http.get('data/meta.json').success(function(data) {
		$scope.meta = data;
    });
}]);

//
//
//
reportControllers.controller('LogCtrl', ['$scope', '$http', function($scope, $http) {

    $http.get('data/report.log').success(function(data) {
		$scope.log = data;
	});
}]);
