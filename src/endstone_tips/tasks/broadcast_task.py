import time

from endstone_tips.tasks.base_task import BaseTask
from endstone_tips.utils.api import str_replace


class BroadcastTask(BaseTask):
    """聊天栏公告任务"""

    def __init__(self):
        super().__init__()
        self.index = 0
        self.last_update = 0

    def on_update(self):
        from endstone_tips.tips import tips_instance
        
        config = tips_instance.plugin_config.theme.get_broadcast_set("default")
        if not config["是否开启"]:
            return
        
        messages = config.get("消息轮播", [])
        if len(messages) == 0:
            return
        
        # 检查是否到达间隔时间
        current_time = time.time()
        interval = config.get("间隔时间", 30)
        
        if current_time - self.last_update < interval:
            return
        
        self.last_update = current_time
        
        # 获取当前消息
        message = messages[self.index]
        self.index = (self.index + 1) % len(messages)
        
        # 广播给所有玩家
        for player in tips_instance.server.online_players:
            processed_message = str_replace(message, player)
            player.send_message(processed_message)
