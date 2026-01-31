"""经济插件集成"""

from typing import Optional


class EconomyProvider:
    """经济插件提供者接口"""
    
    def get_balance(self, player_name: str) -> Optional[float]:
        """获取玩家余额"""
        raise NotImplementedError
    
    def is_available(self) -> bool:
        """检查经济插件是否可用"""
        raise NotImplementedError


class UMoneyProvider(EconomyProvider):
    """UMoney 经济插件提供者"""
    
    def __init__(self, server):
        self.server = server
        self._plugin = None
    
    def _get_plugin(self):
        """获取 UMoney 插件实例"""
        if self._plugin is None:
            self._plugin = self.server.plugin_manager.get_plugin('umoney')
        return self._plugin
    
    def is_available(self) -> bool:
        """检查 UMoney 是否可用"""
        return self._get_plugin() is not None
    
    def get_balance(self, player_name: str) -> Optional[float]:
        """获取玩家余额"""
        plugin = self._get_plugin()
        if plugin is None:
            return None
        
        try:
            return float(plugin.api_get_player_money(player_name))
        except Exception:
            return None


class EconomyManager:
    """经济管理器 - 支持多个经济插件"""
    
    def __init__(self, server):
        self.server = server
        self._providers = []
        self._active_provider: Optional[EconomyProvider] = None
        
        # 注册支持的经济插件
        self._register_providers()
    
    def _register_providers(self):
        """注册所有支持的经济插件提供者"""
        # UMoney
        self._providers.append(UMoneyProvider(self.server))
    
    def get_active_provider(self) -> Optional[EconomyProvider]:
        """获取当前激活的经济插件"""
        if self._active_provider is not None and self._active_provider.is_available():
            return self._active_provider
        
        # 查找可用的经济插件
        for provider in self._providers:
            if provider.is_available():
                self._active_provider = provider
                return provider
        
        return None
    
    def is_available(self) -> bool:
        """检查是否有可用的经济插件"""
        return self.get_active_provider() is not None
    
    def get_balance(self, player_name: str) -> Optional[float]:
        """获取玩家余额"""
        provider = self.get_active_provider()
        if provider is None:
            return None
        return provider.get_balance(player_name)
    
    def get_balance_formatted(self, player_name: str) -> str:
        """获取格式化的玩家余额"""
        balance = self.get_balance(player_name)
        if balance is None:
            return "N/A"
        return f"{balance:.2f}"
