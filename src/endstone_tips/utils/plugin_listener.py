from endstone.event import event_handler, EventPriority, PlayerJoinEvent, PlayerChatEvent


from endstone_tips.utils.api import str_replace


class OnListener:

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        event.player.send_message("Welcome to the server!")
        pass

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

    pass