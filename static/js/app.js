angular.module('newMissionApp', ['ngAnimate', 'ngRoute'])
    .config(function($routeProvider) {
        $routeProvider
            .when('/', {
                controller: 'newMissionController',
                templateUrl: ''
            })
            .when('/mission_name',{
                controller: 'missionNameController',
                templateUrl: 'newmission_name.html'
            })
            .otherwise({
                redirectTo: '/'
            })

    })
    .controller('newMissionController', function($scope) {
        $scope.newMission = true;
        $scope.viewShow = false;

        $scope.showBlock = function() {
            $scope.homeShow = false;
            $scope.viewShow = true;
        }
    })
    .controller('toast', ['$scope', '$interval', toastCtrl])
    .animation('.aweui-show', ['$animateCss', toastAnimate])
    .animation('.home', ['$animateCss', function($animateCss) {
        return {
            enter: function(element, doneFn) {
                return $animateCss(element, {
                    from: { left: '100%', top: 0, opacity: 0 },
                    to: { left: 0, top: 0, opacity: 1 },
                    duration: .3
                });
            },
            leave: function(element, doneFn) {
                return $animateCss(element, {
                    from: { left: 0, top: 0, opacity: 1 },
                    to: { left: '-100%', top: 0, opacity: 0 },
                    duration: .3
                });
            }
        }
    }])
    .animation('.view', ['$animateCss', function($animateCss) {
        return {
            enter: function(element, doneFn) {
                return $animateCss(element, {
                    from: { left: '100%', top: 0, opacity: 0 },
                    to: { left: 0, top: 0, opacity: 1 },
                    duration: .3
                });
            },
            leave: function(element, doneFn) {
                return $animateCss(element, {
                    from: { left: 0, top: 0, opacity: 1 },
                    to: { left: '-100%', top: 0, opacity: 0 },
                    duration: .3
                });
            }
        }
    }])