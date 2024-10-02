from endstone.scoreboard import Criteria, DisplaySlot

from endstone_tips.tasks.base_task import BaseTask
from endstone_tips.utils.api import str_replace

OBJECTIVE_NAME = "__TIPS_SIDEBAR_OBJECTIVE__"

class ScoreBoardTask(BaseTask):

    def on_update(self):
        from endstone_tips.tips import tips_instance
        for player in tips_instance.server.online_players:
            config = tips_instance.plugin_config.theme.get_scoreboard_set(player.level.name)
            if not config["是否开启"]:
                continue

            if player.scoreboard is None:
                player.scoreboard = tips_instance.server.create_scoreboard()

            objective = player.scoreboard.get_objective(OBJECTIVE_NAME)
            if objective is not None:
                objective.unregister()
            objective = player.scoreboard.add_objective(OBJECTIVE_NAME, Criteria.DUMMY, str_replace(config["Title"], player))

            count = 0
            for line in config["Line"]:
                objective.get_score(str_replace(line, player)).value = count
                count += 1

            if count > 0:
                objective.set_display(DisplaySlot.SIDE_BAR)

        pass

