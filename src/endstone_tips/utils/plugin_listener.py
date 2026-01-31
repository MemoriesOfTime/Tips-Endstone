from endstone.event import event_handler, EventPriority, PlayerChatEvent, ServerListPingEvent, PlayerQuitEvent

from endstone_tips.utils.api import str_replace


class OnListener:

    @event_handler(ignore_cancelled=True, priority=EventPriority.HIGH)
    def on_player_chat(self, event: PlayerChatEvent):
        from endstone_tips.tips import tips_instance
        theme = tips_instance.plugin_config.theme.get_message_set(event.player.level.name)
        if not theme.get("是否开启", False):
            return
        message = str_replace(theme.get("显示", "{name}: {msg}"), event.player).replace("{msg}", event.message)
        event.cancelled = True
        if theme.get("是否仅在世界内有效", False):
            for p in tips_instance.server.online_players:
                if p.level.name == event.player.level.name:
                    p.send_message(message)
        else:
            tips_instance.server.broadcast_message(message)

    @event_handler
    def on_server_list_ping(self, event: ServerListPingEvent):
        from endstone_tips.tips import tips_instance
        motd_config = tips_instance.plugin_config.get_motd_set()
        if motd_config.get("是否启用", False):
            motd = motd_config.get("内容", "")
            if motd:
                event.motd = str_replace(motd, None)

    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent):
        from endstone_tips.tips import tips_instance, BOSS_BAR_TYPE
        # 清理 BossBar
        if BOSS_BAR_TYPE in tips_instance.tasks:
            tips_instance.tasks[BOSS_BAR_TYPE].remove_player(event.player)
