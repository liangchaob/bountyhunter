//toast控制器
function toastCtrl($scope, $interval) {
    $scope.toastHide = 0; //是否显示样式一
    $scope.loadingToastHide = 0; //是否显示样式二

    $scope.showToast = function() {
        $scope.toastHide = 1;

        //显示3秒后消失
        $interval(function() {
            $scope.toastHide = 0;
        }, 3000, 1);
    }

    $scope.showLoadingToast = function() {
        $scope.loadingToastHide = 1;

        //显示3秒后消失
        $interval(function() {
            $scope.loadingToastHide = 0;
        }, 3000, 1);
    }
}
