from endstone.event import event_handler, EventPriority, PlayerChatEvent, ServerListPingEvent

from endstone_tips.utils.api import str_replace


class OnListener:

    @event_handler(ignore_cancelled=True, priority=EventPriority.HIGH)
    def on_player_chat(self, event: PlayerChatEvent):
        from endstone_tips.tips import tips_instance
        theme = tips_instance.plugin_config.theme.get_message_set(event.player.level.name)
        if not theme["是否开启"]:
            return
        message = str_replace(theme["显示"], event.player).replace("{msg}", event.message)
        event.message = ""
        event.cancelled = True
        if theme["是否仅在世界内有效"]:
            for p in tips_instance.server.online_players:
                if p.name == event.player.name or p.level.name != event.player.level.name:
                    continue
                p.send_message(event.message)
        else:
            tips_instance.server.broadcast_message(message)
        pass

    @event_handler
    def on_server_list_ping(self, event: ServerListPingEvent):
        from endstone_tips.tips import tips_instance
        enable = tips_instance.plugin_config.get_motd_set()["是否启用"]
        if tips_instance.plugin_config.get_motd_set()["是否启用"]:
            motd = tips_instance.plugin_config.get_motd_set()["内容"]
            event.motd = str_replace(motd, None)
        pass