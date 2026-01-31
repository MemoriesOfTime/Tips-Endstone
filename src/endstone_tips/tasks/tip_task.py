from endstone import Player

from endstone_tips.tasks.base_task import BaseTask
from endstone_tips.utils.api import str_replace


class TipTask(BaseTask):

    def on_update(self):
        from endstone_tips.tips import tips_instance
        
        for player in tips_instance.server.online_players:
            # 检查玩家是否启用此显示
            if not tips_instance.player_config.is_display_enabled(player.name, "tip"):
                continue
            
            # 获取玩家的主题配置
            theme = tips_instance.get_player_theme(player.name)
            if theme is None:
                continue
                
            config = theme.get_tip_set(player.level.name)
            if not config.get("是否开启", False):
                continue
            
            message = str_replace(config.get("显示", ""), player)
            show_type = config.get("显示类型", 0)
            self.send_message(player, message, show_type)

    def send_message(self, player: Player, message: str, show_type: int = 0):
        if message == "":
            return
        if show_type == 1:
            player.send_popup(message)
        elif show_type == 2:
            player.send_tip(message)  # action_bar if available
        else:
            player.send_tip(message)
