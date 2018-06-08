//
//
//
var reportControllers = angular.module('reportControllers', []);

//
//
//
reportControllers.controller('ListCtrl', ['$scope', '$http', function ($scope, $http) {

	$http.get('data/days.json').success(function(data) {
		$scope.days = data;
	});

	$http.get('data/meta.json').success(function(data) {
		$scope.meta = data;
	});
}]);

//
//
//
reportControllers.controller('DetailCtrl', ['$scope', '$routeParams', '$http', function($scope, $routeParams, $http) {
    $scope.item = $routeParams.item;

    $http.get('data/' + $routeParams.item + '/detailed.json').success(function(data) {
		$scope.detailed = data;
	});

	$http.get('data/' + $routeParams.item + '/hours.json').success(function(data) {
		$scope.hours = data;
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