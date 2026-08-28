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
    """UMoney 经济插件提供者（首选）"""

    PLUGIN_NAME = 'umoney'

    def __init__(self, server):
        self.server = server
        self._plugin = None

    def _get_plugin(self):
        """获取 UMoney 插件实例"""
        if self._plugin is None:
            manager = self.server.plugin_manager
            plugin = manager.get_plugin(self.PLUGIN_NAME)
            if plugin is not None and manager.is_plugin_enabled(plugin):
                self._plugin = plugin
        return self._plugin

    def is_available(self) -> bool:
        """检查 UMoney 是否可用（运行时被卸载/禁用后自动失效）"""
        plugin = self._get_plugin()
        if plugin is None:
            return False
        if not self.server.plugin_manager.is_plugin_enabled(plugin):
            self._plugin = None
            return False
        return True

    def get_balance(self, player_name: str) -> Optional[float]:
        """获取玩家余额"""
        plugin = self._get_plugin()
        if plugin is None:
            return None

        try:
            return float(plugin.api_get_player_money(player_name))
        except Exception:
            return None


class GenericEconomyProvider(EconomyProvider):
    """通用经济提供者（备选）。

    按接口特征自动探测已启用的经济插件（duck-typing），
    不依赖、也不记录任何具体插件的名称或实现细节。
    """

    # 标准经济接口特征：余额查询 + 常见资金操作，
    # 同时满足才视为经济插件，避免误匹配无关插件
    _API_METHODS = ('my_money', 'add_money', 'reduce_money', 'transfer_money')

    def __init__(self, server):
        self.server = server
        self._plugin = None

    def _matches(self, plugin) -> bool:
        return all(callable(getattr(plugin, name, None)) for name in self._API_METHODS)

    def _scan(self):
        manager = self.server.plugin_manager
        for plugin in manager.plugins:
            try:
                if manager.is_plugin_enabled(plugin) and self._matches(plugin):
                    return plugin
            except Exception:
                continue
        return None

    def _get_plugin(self):
        if self._plugin is None:
            self._plugin = self._scan()
        return self._plugin

    def is_available(self) -> bool:
        plugin = self._get_plugin()
        if plugin is None:
            return False
        try:
            enabled = self.server.plugin_manager.is_plugin_enabled(plugin)
        except Exception:
            enabled = False
        if not enabled:
            self._plugin = None
            return False
        return True

    def get_balance(self, player_name: str) -> Optional[float]:
        """获取玩家余额"""
        plugin = self._get_plugin()
        if plugin is None:
            return None
        try:
            return float(plugin.my_money(player_name))
        except Exception:
            return None


class EconomyManager:
    """经济管理器 - 支持多个经济插件"""

    def __init__(self, server):
        self.server = server
        self._providers = []
        self._active_provider: Optional[EconomyProvider] = None

        # 注册支持的经济插件提供者（按优先级排序，前者不可用时自动切换到后者）
        self._register_providers()

    def _register_providers(self):
        """注册所有支持的经济插件提供者"""
        self._providers.append(UMoneyProvider(self.server))
        self._providers.append(GenericEconomyProvider(self.server))

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
