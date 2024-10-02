import random
from datetime import datetime

from endstone_tips.utils.variables.base_variable import BaseVariable


class DefaultVariable(BaseVariable):

    def __init__(self):
        super().__init__()
        self.color_code = ["§c", "§6", "§e", "§a", "§b", "§9", "§d", "§7", "§5"]
        pass

    def on_update(self):
        self.update_time()
        self.update_player_info()
        self.update_server_info()
        self.update_other()
        pass

    def update_time(self):
        now = datetime.now()
        self.add_variable("{年}", now.strftime("%Y"))
        self.add_variable("{月}", now.strftime("%m"))
        self.add_variable("{日}", str(now.day))
        self.add_variable("{时}", str(now.hour))
        self.add_variable("{分}", str(now.minute))
        self.add_variable("{秒}", str(now.second))
        self.add_variable("{星期}", str(now.weekday()))
        pass

    def update_player_info(self):
        if self.player is None:
            return

        self.add_variable("{player}", self.player.name)
        self.add_variable("{name}", self.player.name)
        self.add_variable("{ms}", self.player.ping)
        self.add_variable("{levelName}", self.player.level.name)
        self.add_variable("{x}", f"{self.player.location.x:.1f}")
        self.add_variable("{y}", f"{self.player.location.y:.1f}")
        self.add_variable("{z}", f"{self.player.location.z:.1f}")

        self.add_variable("{deviceOS}", self.player.device_os)
        self.add_variable("{playerVersion}", self.player.game_version)

        from endstone_tips.tips import tips_instance
        op = ""
        if self.player.is_op:
            op = tips_instance.plugin_config.get_variable()["玩家权限"]["op"]
        else:
            op = tips_instance.plugin_config.get_variable()["玩家权限"]["player"]
        tips_instance.plugin_config.get_variable()
        self.add_variable("{op}", op)

        self.add_variable("{gm}", tips_instance.plugin_config.get_variable()["游戏模式"][str(self.player.game_mode.value)])

        fly = ""
        if self.player.allow_flight:
            fly = tips_instance.plugin_config.get_variable()["飞行"]["0"]
        else:
            fly = tips_instance.plugin_config.get_variable()["飞行"]["1"]
        self.add_variable("{fly}", fly)

        pass

    def update_server_info(self):
        from endstone_tips.tips import tips_instance

        self.add_variable("{tps}", tips_instance.server.current_tps)
        self.add_variable("{online}", len(tips_instance.server.online_players))
        self.add_variable("{maxplayer}", tips_instance.server.max_players)
        pass

    def update_other(self):
        self.add_variable("{换行}", "\n")
        self.add_variable("{color}", random.choice(self.color_code))
        pass