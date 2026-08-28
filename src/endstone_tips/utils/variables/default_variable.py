import math
import random
from datetime import datetime

from endstone_tips.utils.variables.base_variable import BaseVariable


# 指南针显示（引用自 PetteriM1 的 ViewCompass）
COMPASS = [
    "§7|  |  |  |  |  §l§1南§r§7  |  |  |  |  |",
    "§7|  |  |  |  §l§1南§r§7  |  |  |  |  |  |",
    "§7|  |  |  §l§1南§r§7  |  |  |  |  §l§f西南§r§7  |  |",
    "§7|  |  |  |  |  |  §l§f西南§r§7  |  |  |  |",
    "§7|  |  |  |  |  §l§f西南§r§7  |  |  |  |  |",
    "§7|  |  |  |  §l§f西南§r§7  |  |  |  |  |  |",
    "§7|  |  §l§f西南§r§7  |  |  |  |  §l§a西§r§7  |  |  |",
    "§7|  |  |  |  |  |  §l§a西§r§7  |  |  |  |",
    "§7|  |  |  |  |  §l§a西§r§7  |  |  |  |  |",
    "§7|  |  |  |  |  §l§a西§r§7  |  |  |  |  |",
    "§7|  |  |  |  §l§a西§r§7  |  |  |  |  |  |",
    "§7|  |  |  §l§a西§r§7  |  |  |  |  §l§f西北§r§7  |  |",
    "§7|  |  |  |  |  |  §l§f西北§r§7  |  |  |  |",
    "§7|  |  |  |  |  §l§f西北§r§7  |  |  |  |  |",
    "§7|  |  |  |  §l§f西北§r§7  |  |  |  |  |  |",
    "§7|  |  §l§f西北§r§7  |  |  |  |  §l§c北§r§7  |  |  |",
    "§7|  |  |  |  |  |  §l§c北§r§7  |  |  |  |",
    "§7|  |  |  |  |  §l§c北§r§7  |  |  |  |  |",
    "§7|  |  |  |  |  §l§c北§r§7  |  |  |  |  |",
    "§7|  |  |  |  §l§c北§r§7  |  |  |  |  |  |",
    "§7|  |  |  §l§c北§r§7  |  |  |  |  §l§f东北§r§7  |  |",
    "§7|  |  |  |  |  |  §l§f东北§r§7  |  |  |  |",
    "§7|  |  |  |  |  §l§f东北§r§7  |  |  |  |  |",
    "§7|  |  |  |  §l§f东北§r§7  |  |  |  |  |  |",
    "§7|  |  §l§f东北§r§7  |  |  |  |  §l§e东§r§7  |  |  |",
    "§7|  |  |  |  |  |  |  §l§e东§r§7  |  |  |",
    "§7|  |  |  |  |  |  §l§e东§r§7  |  |  |  |",
    "§7|  |  |  |  |  §l§e东§r§7  |  |  |  |  |",
    "§7|  |  |  |  §l§e东§r§7  |  |  |  |  |  |",
    "§7|  |  |  §l§e东§r§7  |  |  |  |  §l§f东南§r§7  |  |",
    "§7|  |  |  |  |  |  §l§f东南§r§7  |  |  |  |",
    "§7|  |  |  |  |  §l§f东南§r§7  |  |  |  |  |",
    "§7|  |  |  |  §l§f东南§r§7  |  |  |  |  |  |",
    "§7|  |  §l§f东南§r§7  |  |  |  |  §l§1南§r§7  |  |  |",
    "§7|  |  |  |  |  |  |  §l§1南§r§7  |  |  |",
    "§7|  |  |  |  |  |  §l§1南§r§7  |  |  |  |",
]


class DefaultVariable(BaseVariable):

    def __init__(self):
        super().__init__()
        self.color_code = ["§c", "§6", "§e", "§a", "§b", "§9", "§d", "§7", "§5"]

    def on_update(self):
        self.update_time()
        self.update_player_info()
        self.update_server_info()
        self.update_other()

    def update_time(self):
        now = datetime.now()
        self.add_variable("{年}", now.strftime("%Y"))
        self.add_variable("{月}", now.strftime("%m"))
        self.add_variable("{日}", str(now.day))
        self.add_variable("{时}", str(now.hour))
        self.add_variable("{分}", str(now.minute))
        self.add_variable("{秒}", str(now.second))
        self.add_variable("{星期}", self._get_weekday_cn(now.weekday()))

    def _get_weekday_cn(self, weekday: int) -> str:
        """获取中文星期"""
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        return weekdays[weekday] if 0 <= weekday < 7 else str(weekday)

    def _get_compass(self, yaw: float) -> str:
        """获取指南针显示"""
        direction = yaw + math.ceil(-yaw / 360) * 360
        index = round(direction * 2 / 10 / 2)
        return COMPASS[index % len(COMPASS)]

    def update_player_info(self):
        if self.player is None:
            return

        # 基础信息
        self.add_variable("{player}", self.player.name)
        self.add_variable("{name}", self.player.name)
        self.add_variable("{ms}", f"{self.player.ping}ms")
        self.add_variable("{h}", f"{self.player.health:.1f}")
        self.add_variable("{mh}", str(int(self.player.max_health)))
        self.add_variable("{levelName}", self.player.level.name)
        
        # 坐标
        self.add_variable("{x}", f"{self.player.location.x:.0f}")
        self.add_variable("{y}", f"{self.player.location.y:.0f}")
        self.add_variable("{z}", f"{self.player.location.z:.0f}")

        # 设备信息
        self.add_variable("{deviceOS}", self.player.device_os)
        self.add_variable("{playerVersion}", self.player.game_version)

        # 指南针
        self.add_variable("{view}", self._get_compass(self.player.location.yaw))

        # 手持物品 (Endstone 0.10+: PlayerInventory.item_in_main_hand，空手为 None)
        try:
            item = self.player.inventory.item_in_main_hand
            if item:
                item_id = item.type.id
                if item_id.startswith("minecraft:"):
                    item_id = item_id[len("minecraft:"):]
                self.add_variable("{id}", item_id)
                self.add_variable("{damage}", str(item.data))
            else:
                self.add_variable("{id}", "air")
                self.add_variable("{damage}", "0")
        except Exception:
            self.add_variable("{id}", "air")
            self.add_variable("{damage}", "0")

        # 饥饿值 (需要检查 API 是否支持)
        try:
            if hasattr(self.player, 'hunger'):
                self.add_variable("{food}", str(self.player.hunger))
                self.add_variable("{mfood}", "20")
            else:
                self.add_variable("{food}", "20")
                self.add_variable("{mfood}", "20")
        except Exception:
            self.add_variable("{food}", "20")
            self.add_variable("{mfood}", "20")

        # 经验值
        try:
            self.add_variable("{player_exp}", str(self.player.total_exp))
            self.add_variable("{player_exp_level}", str(self.player.exp_level))
        except Exception:
            self.add_variable("{player_exp}", "0")
            self.add_variable("{player_exp_level}", "0")

        # 从配置获取变量显示
        from endstone_tips.tips import tips_instance
        var_config = tips_instance.plugin_config.get_variable()
        
        # OP 显示
        op_config = var_config.get("玩家权限", {"op": "§c[§e管理员§c]§f", "player": "§c[§b玩家§c]§f"})
        if self.player.is_op:
            self.add_variable("{op}", op_config.get("op", "§c[§e管理员§c]§f"))
        else:
            self.add_variable("{op}", op_config.get("player", "§c[§b玩家§c]§f"))

        # 游戏模式
        gm_config = var_config.get("游戏模式", {"0": "生存", "1": "创造", "2": "冒险", "3": "旁观"})
        gm_value = str(self.player.game_mode.value)
        self.add_variable("{gm}", gm_config.get(gm_value, "未知"))

        # 飞行状态
        fly_config = var_config.get("飞行", {"0": "飞行开启", "1": "飞行关闭"})
        if self.player.allow_flight:
            self.add_variable("{fly}", fly_config.get("0", "飞行开启"))
        else:
            self.add_variable("{fly}", fly_config.get("1", "飞行关闭"))

        # 金币 (通过经济插件获取)
        money = tips_instance.economy_manager.get_balance_formatted(self.player.name)
        self.add_variable("{money}", money)

    def update_server_info(self):
        from endstone_tips.tips import tips_instance

        self.add_variable("{tps}", f"{tips_instance.server.current_tps:.1f}")
        self.add_variable("{online}", str(len(tips_instance.server.online_players)))
        self.add_variable("{maxplayer}", str(tips_instance.server.max_players))
        self.add_variable("{version}", tips_instance.server.minecraft_version)

    def update_other(self):
        self.add_variable("{换行}", "\n")
        self.add_variable("{color}", random.choice(self.color_code))
