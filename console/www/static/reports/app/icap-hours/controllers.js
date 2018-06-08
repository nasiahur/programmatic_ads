//
//
//
var reportControllers = angular.module('reportControllers', []);

//
//
//
reportControllers.controller('ListCtrl', ['$scope', '$http', function ($scope, $http) {

	$http.get('data/hours.json').success(function(data) {
		$scope.hours = data;
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