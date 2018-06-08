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


function compareByDomainSize(a,b) {
  if (a.domain.size > b.domain.size)
    return -1;
  if (a.domain.size < b.domain.size)
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

function build_user_table(users) {
    var rawHeader = "<thead class=\"md-head\">"+
                    "<tr class=\"md-row\">" +
                    "<th class=\"md-column\"><span class=\"bold\">User Name</span></th>" +
                    "<th class=\"md-column\" class=\"md-numeric\">Hits</th>" +
                    "<th class=\"md-column\" class=\"md-numeric\">Size</th>" +
                    "<th class=\"md-column\" class=\"md-numeric\">Duration</th>" +
                    "</tr></thead>";

    var rawBody = "<tbody class=\"md-body\">";
    angular.forEach(users, function(user, userIndex) {
        var row = "<tr class=\"md-row\">" +
                  "<td class=\"md-cell\"><a href=\"#/users/" + user.id + "\">" + user.value + "</a></td>" +
                  "<td class=\"md-cell\">" + user.hits + "</td>" +
                  "<td class=\"md-cell\">" + function_bytes(user.size) + "</td>" +
                  "<td class=\"md-cell\">" + function_duration(user.duration) + "</td></tr>";
        rawBody = rawBody + row + "\n";
    });
    rawBody = rawBody + "</tbody>";

    var rawHtml= rawHeader + rawBody;
    var userTable = document.getElementById("user_table");
    angular.element(userTable).html(rawHtml);
}


function build_user_domain_table(userDomains, userId) {
    var rawHeader = "<thead class=\"md-head\">"+
                    "<tr class=\"md-row\">" +
                    "<th class=\"md-column\"><span class=\"bold\">Domain</span></th>" +
                    "<th class=\"md-column\" class=\"md-numeric\">Total Requests</th>" +
                    "<th class=\"md-column\" class=\"md-numeric\">Size</th>" +
                    "</tr></thead>";

    var rawBody = "<tbody class=\"md-body\">";
    angular.forEach(userDomains, function(d, unusedIndex){
        var row = "<tr class=\"md-row\">" +
                  "<td class=\"md-cell\"><a href=\"#/users/" + userId + "/" + d.domainLine + "\">" + d.domain.value + "</a></td>" +
                  "<td class=\"md-cell\">" + d.domain.hits + "</td>" +
                  "<td class=\"md-cell\">" + function_bytes(d.domain.size) + "</td></tr>";
        rawBody = rawBody + row + "\n";
    });
    rawBody = rawBody + "</tbody>";

    var rawHtml= rawHeader + rawBody;
    var domainTable = document.getElementById("domain_table");
    angular.element(domainTable).html(rawHtml);
}


function build_domain_event_table(domainInfo, $filter) {
    var rawHeader = "<thead class=\"md-head\">"+
                    "<tr class=\"md-row\">" +
                    "<th class=\"md-column\"><span class=\"bold\">Timestamp</span></th>" +
                    "<th class=\"md-column\" class=\"md-numeric\">Size</th>" +
                    "<th class=\"md-column\" class=\"md-numeric\">Duration</th>" +
                    "</tr>" +
                    "</thead>";

    var rawBody = "<tbody class=\"md-body\">";
    angular.forEach(domainInfo.records, function(e, unusedIndex){
        var row = "<tr class=\"md-row\">" +
                  "<td class=\"md-cell\">" + $filter('date')(e.timestamp * 1000, 'yyyy-MM-dd HH:mm:ss') + "</a></td>" +
                  "<td class=\"md-cell\">" + function_bytes(e.size) + "</td>" +
                  "<td class=\"md-cell\">" + function_duration(e.duration) + "</td></tr>";
        rawBody = rawBody + row + "\n";
    });
    rawBody = rawBody + "</tbody>";

    var rawHtml= rawHeader + rawBody;
    var eventTable = document.getElementById("event_table");
    angular.element(eventTable).html(rawHtml);
}

reportControllers.controller('UsersCtrl', ['$scope', '$http', function ($scope, $http) {
    $http.get('data/meta.json').success(function(data) {
        $scope.meta = data;

        $http.get('data/users/users.json').success(function(data) {
            $scope.users = data;
            $scope.users.sort(compareBySize);
            $scope.users = $scope.users.slice(0, $scope.meta['job']['params']['limit_n_entries']);
            build_user_table($scope.users);
        });
    });
}]);

//
//
//
reportControllers.controller('UserCtrl', ['$scope', '$routeParams', '$http', function($scope, $routeParams, $http) {
    $scope.userId = $routeParams.userId;
    $http.get('data/meta.json').success(function(data) {
        $scope.meta = data;

        $http.get('data/users/' + $routeParams.userId + '/detailed',
           {
               transformResponse: function(data) { return data; }
           }).success(function(data) {

	        var detailedLines = data.split("\n");
                var detailed = [ ];
                for (var i = 0; i < detailedLines.length - 1; ++i) {
                    detailed.push(JSON.parse(detailedLines[i]));
                    detailed[i].domainLine = i;
                }
                detailed.sort(compareByDomainSize);
                detailed = detailed.slice(0, $scope.meta['job']['params']['limit_n_drilldown']);
                build_user_domain_table(detailed, $scope.userId);
	   });


           $http.get('data/users/' + $routeParams.userId + '/user.json').success(function(data) {
   		    $scope.user = data;
                    $scope.days = [];
                    var days_distribution = data['days_distribution'];
                    for(var d in days_distribution) {
                        if(days_distribution.hasOwnProperty(d)) {
                            var totalValue = 0;
                            for(var i = 0; i < days_distribution[d].length; ++i){
                                totalValue = totalValue + days_distribution[d][i];
                            }
                            var currentDate = new Date($scope.meta.start);
                            currentDate.setTime(currentDate.getTime() + d * 86400000);
                            $scope.days.push({ 'day':currentDate, 'size': totalValue});
                        }
                    }
	    });
     });
}]);

//
//
//
reportControllers.controller('DomainCtrl', ['$scope', '$routeParams', '$http', '$filter', function($scope, $routeParams, $http, $filter) {
    $scope.userId = $routeParams.userId;
    $scope.domain = $routeParams.domain;
    $scope.domainLine = $routeParams.domainLine;


	$http.get('data/meta.json').success(function(data) {
		$scope.meta = data;
    })

    $http.get('data/users/' + $routeParams.userId + '/detailed', {
        transformResponse: function(data) { return data; }
    }).success(function(data) {
        var detailedLines = data.split("\n");
        $scope.detailed = JSON.parse(detailedLines[$scope.domainLine]);
        build_domain_event_table($scope.detailed, $filter);
	});

    $http.get('data/users/' + $routeParams.userId + '/user.json').success(function(data) {
	    $scope.user = data;
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
