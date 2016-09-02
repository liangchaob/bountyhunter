angular.module('weuiapp', ['ngRoute'])
    .config(function($routeProvider) {
        //路由配置
        $routeProvider
            .when('/', {
                controller: 'homeCtrl',
                templateUrl: 'home.html'
            })
            .when('/button', {
                controller: 'buttonCtrl',
                templateUrl: 'button.html'
            })
            .when('/cell', {
                controller: 'cellCtrl',
                templateUrl: 'cell.html'
            })
            .when('/toast', {
                controller: 'toastCtrl',
                templateUrl: 'toast.html'
            })
            .when('/dialog', {
                controller: 'dialogCtrl',
                templateUrl: 'dialog.html'
            })
            .when('/progress', {
                controller: 'progressCtrl',
                templateUrl: 'progress.html'
            })
            .when('/msg', {
                controller: 'msgCtrl',
                templateUrl: 'msg.html'
            })
            .when('/article', {
                controller: 'articleCtrl',
                templateUrl: 'article.html'
            })
            .when('/actionsheet', {
                controller: 'actionsheetCtrl',
                templateUrl: 'actionsheet.html'
            })
            .when('/icons', {
                controller: 'iconsCtrl',
                templateUrl: 'icons.html'
            })
            .when('/panel', {
                controller: 'panelCtrl',
                templateUrl: 'panel.html'
            })
            .when('/tab', {
                controller: 'tabCtrl',
                templateUrl: 'tab.html'
            })
            .when('/navbar', {
                controller: 'navbarCtrl',
                templateUrl: 'navbar.html'
            })
            .when('/tabbar', {
                controller: 'tabbarCtrl',
                templateUrl: 'tabbar.html'
            })
            .when('/searchbar', {
                controller: 'searchbarCtrl',
                templateUrl: 'searchbar.html'
            })
            .otherwise({
                redirectTo: '/'
            });


    })
    .controller('homeCtrl', function($scope) {
        //初始化ngView的样式为不可见
        $scope.viewStyle = {
            left: '200%',
            height: 0,
            width: 0
        };

        $scope.showBlock = function() {
            //设置ngView的样式可见
            $scope.viewStyle = {
                left: 0,
                height: '100%',
                width: '100%'
            };
        }
    })
    // //增加toast控件控制器
    // .controller('toastCtrl', ['$scope', '$interval', toastCtrl])
    // //增加dialog控件控制器
    // .controller('dialogCtrl', ['$scope', dialogCtrl])
    // //增加progress控件控制器
    // .controller('progressCtrl', ['$scope', progressCtrl])
    // //增加actionsheet控件控制器
    // .controller('actionsheetCtrl', ['$scope', actionsheetCtrl])
    // //增加searchbar控件控制器
    // .controller('searchbarCtrl', ['$scope', searchbarCtrl]);
