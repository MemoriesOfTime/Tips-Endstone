"""Tips 命令处理"""

from endstone import Player
from endstone.command import Command, CommandSender


def handle_tips_command(plugin, sender: CommandSender, command: Command, args: list[str]) -> bool:
    """处理 /tips 命令"""
    
    if len(args) == 0:
        # 无参数时显示帮助
        send_help(sender)
        return True
    
    sub_command = args[0].lower()
    
    if sub_command == "reload":
        return handle_reload(plugin, sender)
    elif sub_command == "send":
        return handle_send(plugin, sender, args[1:])
    elif sub_command == "theme":
        return handle_theme(plugin, sender, args[1:])
    elif sub_command == "help":
        send_help(sender)
        return True
    else:
        sender.send_message("§c未知子命令，使用 /tips help 查看帮助")
        return False


def send_help(sender: CommandSender):
    """发送帮助信息"""
    sender.send_message("§a==================== Tips ====================")
    if sender.is_op:
        sender.send_message("§e/tips reload §7- 重新加载配置")
        sender.send_message("§e/tips send <玩家> <类型> <信息> §7- 发送消息给玩家")
        sender.send_message("§7  类型: tip, popup, action, title, msg")
    sender.send_message("§e/tips theme [主题名] §7- 查看/切换主题")
    sender.send_message("§e/tips help §7- 显示此帮助")
    sender.send_message("§a================================================")


def handle_reload(plugin, sender: CommandSender) -> bool:
    """处理 reload 子命令"""
    if not sender.is_op:
        sender.send_message("§c你没有权限执行此命令")
        return False
    
    try:
        from endstone_tips.config import PluginConfig
        plugin.plugin_config = PluginConfig(f"{plugin.data_folder}/config.toml")
        sender.send_message("§a配置重新加载成功!")
        plugin.logger.info("配置已重新加载")
        return True
    except Exception as e:
        sender.send_message(f"§c配置加载失败: {e}")
        plugin.logger.error(f"配置加载失败: {e}")
        return False


def handle_send(plugin, sender: CommandSender, args: list[str]) -> bool:
    """处理 send 子命令"""
    if not sender.is_op:
        sender.send_message("§c你没有权限执行此命令")
        return False
    
    if len(args) < 3:
        sender.send_message("§c用法: /tips send <玩家> <类型> <信息>")
        sender.send_message("§7类型: tip, popup, action, title, msg")
        return False
    
    player_name = args[0]
    msg_type = args[1].lower()
    message = " ".join(args[2:])
    
    # 查找玩家
    target_player = None
    for player in plugin.server.online_players:
        if player.name.lower() == player_name.lower():
            target_player = player
            break
    
    if target_player is None:
        sender.send_message(f"§c找不到玩家: {player_name}")
        return False
    
    # 发送消息
    if msg_type == "tip":
        target_player.send_tip(message)
    elif msg_type == "popup":
        target_player.send_popup(message)
    elif msg_type == "action":
        target_player.send_action_bar(message)
    elif msg_type == "title":
        # 解析标题和副标题
        parts = message.split("|", 1)
        title = parts[0]
        subtitle = parts[1] if len(parts) > 1 else ""
        target_player.send_title(title, subtitle)
    elif msg_type == "msg":
        target_player.send_message(message)
    else:
        sender.send_message(f"§c未知消息类型: {msg_type}")
        sender.send_message("§7可用类型: tip, popup, action, title, msg")
        return False
    
    sender.send_message(f"§a已向 {player_name} 发送 {msg_type} 消息")
    return True


def handle_theme(plugin, sender: CommandSender, args: list[str]) -> bool:
    """处理 theme 子命令"""
    from pathlib import Path
    
    theme_dir = Path(plugin.data_folder) / "theme"
    
    if len(args) == 0:
        # 列出可用主题
        themes = []
        if theme_dir.exists():
            for f in theme_dir.glob("*.toml"):
                themes.append(f.stem)
        
        if themes:
            sender.send_message("§a可用主题:")
            for theme in themes:
                sender.send_message(f"§7  - {theme}")
        else:
            sender.send_message("§c没有找到可用主题")
        return True
    
    # 切换主题 (仅 OP)
    if not sender.is_op:
        sender.send_message("§c你没有权限切换主题")
        return False
    
    theme_name = args[0]
    theme_file = theme_dir / f"{theme_name}.toml"
    
    if not theme_file.exists():
        sender.send_message(f"§c主题 '{theme_name}' 不存在")
        return False
    
    try:
        from endstone_tips.config import ThemeConfig
        plugin.plugin_config.theme = ThemeConfig(str(theme_file))
        sender.send_message(f"§a已切换到主题: {theme_name}")
        return True
    except Exception as e:
        sender.send_message(f"§c加载主题失败: {e}")
        return False
