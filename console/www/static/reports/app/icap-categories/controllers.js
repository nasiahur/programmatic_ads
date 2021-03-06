//
//
//
var reportControllers = angular.module('reportControllers', []);

//
//
//
reportControllers.controller('ListCtrl', ['$scope', '$http', function ($scope, $http) {

	$http.get('data/categories.json').success(function(data) {
		$scope.categories = data;
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
    $scope.itemvalue = $routeParams.itemvalue;
    $http.get('data/' + $routeParams.item + '/detailed.json').success(function(data) {
		$scope.detailed = data;
	});

	$http.get('data/' + $routeParams.item + '/days.json').success(function(data) {
		$scope.days = data;
	});

	$http.get('data/' + $routeParams.item + '/hours.json').success(function(data) {
		$scope.hours = data;
	});

	$http.get('data/' + $routeParams.item + '/users.json').success(function(data) {
		$scope.users = data;
	});

	$http.get('data/' + $routeParams.item + '/ips.json').success(function(data) {
		$scope.ips = data;
	});

}]);

//
//
//
reportControllers.controller('UserCtrl', ['$scope', '$routeParams', '$http', function($scope, $routeParams, $http) {
    $scope.item = $routeParams.item;
    $scope.user = $routeParams.user;
    $scope.itemvalue = $routeParams.itemvalue;
    $scope.uservalue = $routeParams.uservalue;

    $http.get('data/' + $routeParams.item + '/users/' + $routeParams.user + '/domains.json').success(function(data) {
		$scope.domains = data;
	});

	$http.get('data/' + $routeParams.item + '/users/' + $routeParams.user + '/hours.json').success(function(data) {
		$scope.hours = data;
	});
}]);


//
//
//
reportControllers.controller('DomainCtrl', ['$scope', '$routeParams', '$http', function($scope, $routeParams, $http) {
    $scope.item = $routeParams.item;
    $scope.user = $routeParams.user;
    $scope.domain = $routeParams.domain;
    $scope.itemvalue = $routeParams.itemvalue;
    $scope.uservalue = $routeParams.uservalue;
    $scope.domainvalue = $routeParams.domainvalue;
    $http.get('data/' + $routeParams.item + '/users/' + $routeParams.user + '/domains/' + $routeParams.domain + '/urls.json').success(function(data) {
		$scope.urls = data;
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
