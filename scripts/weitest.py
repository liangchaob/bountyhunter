https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa9312a82e8138370&redirect_uri=http%3A%2F%2Fbountyunions.applinzi.com%2Fwechat%2Fuser_center&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect





    <!-- 如果自己本身是发布者 -->
    {% elif openid == mission_obj.publisher %}
    <a class="weui_btn weui_btn_disabled weui_btn_default" href="javascript:;" id="showTooltips">无法竞标自发布项目</a>
    {% else %}
        <!-- 判断当前任务是否里面有竞标者 -->
        {% if mission_obj.bidder %}
            <!-- 如果已经竞标过了 -->
            {% if openid in mission_obj.bidder%}
            <a class="weui_btn weui_btn_disabled weui_btn_default" href="javascript:;" id="showTooltips">已竞标</a>
            {% else %}
            <a class="weui_btn weui_btn_primary" href="javascript:showDialog();" id="showTooltips">竞标</a>
            {% endif %}
        {% else %}
        <a class="weui_btn weui_btn_primary" href="javascript:showDialog();" id="showTooltips">竞标</a>
        {% endif %}
    {% endif %}