"""玩家配置管理"""

from pathlib import Path
from typing import Optional, Dict, Any

import tomlkit


class PlayerConfig:
    """玩家个性化配置"""
    
    def __init__(self, data_folder: Path):
        self.players_dir = data_folder / "players"
        self.players_dir.mkdir(exist_ok=True)
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def _get_player_file(self, player_name: str) -> Path:
        """获取玩家配置文件路径"""
        # 使用小写文件名避免大小写问题
        return self.players_dir / f"{player_name.lower()}.toml"
    
    def load(self, player_name: str) -> Dict[str, Any]:
        """加载玩家配置"""
        if player_name.lower() in self._cache:
            return self._cache[player_name.lower()]
        
        player_file = self._get_player_file(player_name)
        
        if player_file.exists():
            try:
                with player_file.open("r", encoding="utf-8") as f:
                    config = tomlkit.load(f)
                    self._cache[player_name.lower()] = dict(config)
                    return self._cache[player_name.lower()]
            except Exception:
                pass
        
        # 默认配置
        default_config = {
            "theme": "default",
            "displays": {
                "boss_bar": True,
                "scoreboard": True,
                "tip": True,
                "nametag": True,
                "broadcast": True,
                "chat": True,
            }
        }
        self._cache[player_name.lower()] = default_config
        return default_config
    
    def save(self, player_name: str, config: Optional[Dict[str, Any]] = None):
        """保存玩家配置"""
        if config is None:
            config = self._cache.get(player_name.lower(), {})
        
        player_file = self._get_player_file(player_name)
        
        try:
            with player_file.open("w", encoding="utf-8") as f:
                tomlkit.dump(config, f)
            self._cache[player_name.lower()] = config
        except Exception as e:
            from endstone_tips.tips import tips_instance
            tips_instance.logger.error(f"保存玩家配置失败 {player_name}: {e}")
    
    def get_theme(self, player_name: str) -> str:
        """获取玩家选择的主题"""
        config = self.load(player_name)
        return config.get("theme", "default")
    
    def set_theme(self, player_name: str, theme: str):
        """设置玩家主题"""
        config = self.load(player_name)
        config["theme"] = theme
        self.save(player_name, config)
    
    def is_display_enabled(self, player_name: str, display_type: str) -> bool:
        """检查玩家是否启用了某个显示类型"""
        config = self.load(player_name)
        displays = config.get("displays", {})
        return displays.get(display_type, True)
    
    def set_display_enabled(self, player_name: str, display_type: str, enabled: bool):
        """设置玩家的显示类型开关"""
        config = self.load(player_name)
        if "displays" not in config:
            config["displays"] = {}
        config["displays"][display_type] = enabled
        self.save(player_name, config)
    
    def clear_cache(self, player_name: Optional[str] = None):
        """清除缓存"""
        if player_name:
            self._cache.pop(player_name.lower(), None)
        else:
            self._cache.clear()
