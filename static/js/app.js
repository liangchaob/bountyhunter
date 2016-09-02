angular.module('newMissionApp', ['ngAnimate', 'ngRoute'])
    .config(function($routeProvider) {
        $routeProvider
            .when('/', {
                controller: 'home',
                templateUrl: ''
            })
            .when('/mission_name',{
                controller: 'missionNameController',
                templateUrl: 'newmission_name.html'
            })
            .when('/computers',{template:'这是电脑分类页面'})
            .otherwise({
                redirectTo: '/'
            })

    })
    .controller('home', function($scope) {
        $scope.homeShow = true;
        $scope.viewShow = false;

        $scope.showBlock = function() {
            $scope.homeShow = false;
            $scope.viewShow = true;
        }
    })
    // .controller('toast', ['$scope', '$interval', toast])
    // .animation('.aweui-show', ['$animateCss', toastAnimate])
    // .animation('.home', ['$animateCss', function($animateCss) {
    //     return {
    //         enter: function(element, doneFn) {
    //             return $animateCss(element, {
    //                 from: { left: '100%', top: 0, opacity: 0 },
    //                 to: { left: 0, top: 0, opacity: 1 },
    //                 duration: .3
    //             });
    //         },
    //         leave: function(element, doneFn) {
    //             return $animateCss(element, {
    //                 from: { left: 0, top: 0, opacity: 1 },
    //                 to: { left: '-100%', top: 0, opacity: 0 },
    //                 duration: .3
    //             });
    //         }
    //     }
    // }])
    // .animation('.view', ['$animateCss', function($animateCss) {
    //     return {
    //         enter: function(element, doneFn) {
    //             return $animateCss(element, {
    //                 from: { left: '100%', top: 0, opacity: 0 },
    //                 to: { left: 0, top: 0, opacity: 1 },
    //                 duration: .3
    //             });
    //         },
    //         leave: function(element, doneFn) {
    //             return $animateCss(element, {
    //                 from: { left: 0, top: 0, opacity: 1 },
    //                 to: { left: '-100%', top: 0, opacity: 0 },
    //                 duration: .3
    //             });
    //         }
    //     }
    // }])