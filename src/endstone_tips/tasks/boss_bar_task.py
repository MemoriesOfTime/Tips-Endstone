import time

# 兼容不同版本的 endstone
try:
    from endstone import BarColor, BarStyle
except ImportError:
    try:
        from endstone.boss import BarColor, BarStyle
    except ImportError:
        from endstone._internal.endstone_python import BarColor, BarStyle

from endstone_tips.tasks.base_task import BaseTask
from endstone_tips.utils.api import str_replace


class BossBarTask(BaseTask):

    def __init__(self):
        super().__init__()
        self.boss_bar = {}
        self.index = {}
        self.update_time = {}

    def on_update(self):
        from endstone_tips.tips import tips_instance
        
        for player in tips_instance.server.online_players:
            # 检查玩家是否启用此显示
            if not tips_instance.player_config.is_display_enabled(player.name, "boss_bar"):
                boss_bar = self.boss_bar.get(player)
                if boss_bar is not None:
                    boss_bar.remove_player(player)
                continue
            
            # 获取玩家的主题配置
            theme = tips_instance.get_player_theme(player.name)
            if theme is None:
                continue
                
            config = theme.get_boss_bar_set(player.level.name)
            boss_bar = self.boss_bar.get(player)

            if not config.get("是否开启", False):
                if boss_bar is not None:
                    boss_bar.remove_player(player)
                continue

            if boss_bar is None:
                color = BarColor.__members__.get(config.get("显示颜色", "PINK"), BarColor.PINK)
                boss_bar = tips_instance.server.create_boss_bar("title", color, BarStyle.SOLID)

            index = self.index.get(player, 0)
            messages = config.get("消息轮播", [])
            if len(messages) == 0:
                continue
            boss_bar.title = str_replace(messages[index], player)

            t = time.time()
            dt = t - self.update_time.get(player, 0)
            interval = config.get("间隔时间", 5)
            
            if config.get("是否根据玩家血量变化", False):
                boss_bar.progress = self.scale_to_range(player.health, 0, player.max_health)
            else:
                boss_bar.progress = 1 - self.scale_to_range(float(dt), float(0), float(interval))

            boss_bar.is_visible = True
            boss_bar.add_player(player)
            self.boss_bar[player] = boss_bar

            if dt >= interval:
                self.update_time[player] = t
                index = (index + 1) % len(messages)
                self.index[player] = index

    def remove_player(self, player):
        boss_bar = self.boss_bar.pop(player, None)
        if boss_bar is not None:
            boss_bar.remove_player(player)
        self.index.pop(player, None)
        self.update_time.pop(player, None)

    def scale_to_range(self, value: float, min_value: float, max_value: float) -> float:
        if min_value == max_value or value > max_value:
            return 1.0
        return (value - min_value) / (max_value - min_value)
