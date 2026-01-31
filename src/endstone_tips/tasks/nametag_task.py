from endstone_tips.tasks.base_task import BaseTask
from endstone_tips.utils.api import str_replace


class NameTagTask(BaseTask):
    """头顶显示任务"""

    def on_update(self):
        from endstone_tips.tips import tips_instance
        for player in tips_instance.server.online_players:
            config = tips_instance.plugin_config.theme.get_nametag_set(player.level.name)
            if not config["是否开启"]:
                continue
            
            # 替换变量并设置头顶名称
            nametag = str_replace(config["显示"], player)
            player.name_tag = nametag
