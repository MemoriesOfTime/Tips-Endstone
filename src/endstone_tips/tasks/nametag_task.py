from endstone_tips.tasks.base_task import BaseTask
from endstone_tips.utils.api import str_replace


class NameTagTask(BaseTask):
    """头顶显示任务"""

    def on_update(self):
        from endstone_tips.tips import tips_instance
        
        for player in tips_instance.server.online_players:
            # 检查玩家是否启用此显示
            if not tips_instance.player_config.is_display_enabled(player.name, "nametag"):
                continue
            
            # 获取玩家的主题配置
            theme = tips_instance.get_player_theme(player.name)
            if theme is None:
                continue
                
            config = theme.get_nametag_set(player.level.name)
            if not config.get("是否开启", False):
                continue
            
            # 替换变量并设置头顶名称
            nametag = str_replace(config.get("显示", ""), player)
            player.name_tag = nametag
