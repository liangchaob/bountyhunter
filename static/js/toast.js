//toast控制器
function toast($scope, $interval) {
    $scope.toastHide = 0;
    $scope.loadingToastHide = 0;

    $scope.showToast = function() {
        $scope.toastHide = 1;

        $interval(function() {
            $scope.toastHide = 0;
        }, 3000, 1);
    }

    $scope.showLoadingToast = function() {
        $scope.loadingToastHide = 1;

        $interval(function() {
            $scope.loadingToastHide = 0;
        }, 3000, 1);
    }
}

//显示与隐藏时的动画，使用ngAnimate中的$animateCss服务
function toastAnimate($animateCss) {
    return {
        enter: function(element, doneFn) {
            return $animateCss(element, {
                from: { opacity: 0 },
                to: { opacity: 1 },
                duration: .3
            });
        },
        leave: function(element, doneFn) {
            return $animateCss(element, {
                from: { opacity: 1 },
                to: { opacity: 0 },
                duration: .3
            });
        }
    }
}