# 兼容不同版本的 endstone
try:
    from endstone.scoreboard import Criteria, DisplaySlot
except ImportError:
    from endstone import Criteria, DisplaySlot

from endstone_tips.tasks.base_task import BaseTask
from endstone_tips.utils.api import str_replace

OBJECTIVE_NAME = "__TIPS_SIDEBAR_OBJECTIVE__"


class ScoreBoardTask(BaseTask):

    def on_update(self):
        from endstone_tips.tips import tips_instance

        for player in tips_instance.server.online_players:
            # 检查玩家是否启用此显示
            if not tips_instance.player_config.is_display_enabled(player.name, "scoreboard"):
                # 如果计分板已存在，移除显示
                objective = player.scoreboard.get_objective(OBJECTIVE_NAME)
                if objective is not None:
                    objective.unregister()
                continue

            # 获取玩家的主题配置
            theme = tips_instance.get_player_theme(player.name)
            if theme is None:
                continue

            config = theme.get_scoreboard_set(player.level.name)
            if not config.get("是否开启", False):
                # 如果计分板已存在，移除显示
                objective = player.scoreboard.get_objective(OBJECTIVE_NAME)
                if objective is not None:
                    objective.unregister()
                continue

            # player.scoreboard 永远不为 None (未设置时返回服务器全局计分板)，
            # 必须用 is 判断玩家是否仍持有全局板，是则分配独立板；
            # 否则所有玩家共用全局板，内容会互相覆盖 (A 看到 B 的计分板)
            if player.scoreboard is tips_instance.server.scoreboard:
                player.scoreboard = tips_instance.server.create_scoreboard()

            objective = player.scoreboard.get_objective(OBJECTIVE_NAME)
            if objective is not None:
                objective.unregister()
            objective = player.scoreboard.add_objective(
                OBJECTIVE_NAME,
                Criteria.DUMMY,
                str_replace(config.get("Title", ""), player)
            )

            count = 0
            for line in config.get("Line", []):
                objective.get_score(str_replace(line, player)).value = count
                count += 1

            if count > 0:
                objective.set_display(DisplaySlot.SIDE_BAR)
