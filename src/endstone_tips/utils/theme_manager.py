"""主题管理器"""

from pathlib import Path
from typing import Dict, Optional

from endstone_tips.config import ThemeConfig


class ThemeManager:
    """主题管理器 - 支持多主题和热加载"""
    
    def __init__(self, data_folder: Path):
        self.theme_dir = data_folder / "theme"
        self.theme_dir.mkdir(exist_ok=True)
        self._themes: Dict[str, ThemeConfig] = {}
        self._default_theme: str = "default"
        
        # 初始加载所有主题
        self.reload_all()
    
    def reload_all(self):
        """重新加载所有主题"""
        self._themes.clear()
        
        for theme_file in self.theme_dir.glob("*.toml"):
            theme_name = theme_file.stem
            try:
                self._themes[theme_name] = ThemeConfig(str(theme_file))
            except Exception as e:
                from endstone_tips.tips import tips_instance
                tips_instance.logger.error(f"加载主题 {theme_name} 失败: {e}")
    
    def reload(self, theme_name: str) -> bool:
        """重新加载指定主题"""
        theme_file = self.theme_dir / f"{theme_name}.toml"
        
        if not theme_file.exists():
            return False
        
        try:
            self._themes[theme_name] = ThemeConfig(str(theme_file))
            return True
        except Exception as e:
            from endstone_tips.tips import tips_instance
            tips_instance.logger.error(f"重新加载主题 {theme_name} 失败: {e}")
            return False
    
    def get(self, theme_name: str) -> Optional[ThemeConfig]:
        """获取主题配置"""
        return self._themes.get(theme_name)
    
    def get_or_default(self, theme_name: str) -> ThemeConfig:
        """获取主题配置，不存在则返回默认主题"""
        theme = self._themes.get(theme_name)
        if theme is None:
            theme = self._themes.get(self._default_theme)
        if theme is None:
            # 如果连默认主题都没有，尝试加载
            self.reload(self._default_theme)
            theme = self._themes.get(self._default_theme)
        return theme
    
    def list_themes(self) -> list:
        """列出所有可用主题"""
        return list(self._themes.keys())
    
    def exists(self, theme_name: str) -> bool:
        """检查主题是否存在"""
        return theme_name in self._themes
    
    def set_default(self, theme_name: str):
        """设置默认主题"""
        if theme_name in self._themes:
            self._default_theme = theme_name
    
    def get_player_theme(self, player_name: str) -> ThemeConfig:
        """获取玩家的主题配置"""
        from endstone_tips.tips import tips_instance
        
        # 从玩家配置获取主题名
        theme_name = tips_instance.player_config.get_theme(player_name)
        return self.get_or_default(theme_name)
