from endstone import Player

from endstone_tips.tasks.base_task import BaseTask
from endstone_tips.utils.api import str_replace


class TipTask(BaseTask):

    def on_update(self):
        from endstone_tips.tips import tips_instance
        for player in tips_instance.server.online_players:
            config = tips_instance.plugin_config.theme.get_tip_set(player.level.name)
            if not config["是否开启"]:
                continue
            self.send_message(player, str_replace(config["显示"], player), config["显示类型"])
            pass
        pass

    def send_message(self, player: Player, message: str, show_type: int = 0):
        if message == "":
            return
        if show_type == 1:
            player.send_popup(message)
        elif show_type == 2:
            # 正常应该是 action_bar
            player.send_tip(message)
        else:
            player.send_tip(message)
        pass