"""Tips GUI 表单"""

from typing import Optional

from endstone import Player
from endstone.form import ActionForm, ModalForm, Dropdown, Toggle, TextInput

# 显示类型枚举
DISPLAY_TYPES = {
    "Boss血条": "boss_bar",
    "头部显示": "nametag",
    "聊天格式": "chat",
    "底部显示": "tip",
    "聊天栏公告": "broadcast",
    "计分板": "scoreboard",
}


def show_main_menu(player: Player):
    """显示主菜单"""
    form = ActionForm(
        title="§e◎ Tips 设置 ◎",
        content="请选择要执行的操作"
    )
    
    if player.is_op:
        form.add_button(
            text="§a管理玩家显示",
            icon="textures/ui/Friend2",
            on_click=lambda p: show_player_list(p)
        )
        form.add_button(
            text="§b设置默认显示",
            icon="textures/ui/settings_glyph_color_2x",
            on_click=lambda p: show_display_type_menu(p, None)
        )
        form.add_button(
            text="§6重载配置",
            icon="textures/ui/refresh_light",
            on_click=lambda p: _reload_config(p)
        )

    form.add_button(
        text="§d选择主题样式",
        icon="textures/ui/color_picker",
        on_click=lambda p: show_theme_selector(p)
    )

    form.add_button(
        text="§7个人显示设置",
        icon="textures/ui/icon_setting",
        on_click=lambda p: show_personal_settings(p)
    )
    
    form.on_close = lambda p: None
    player.send_form(form)


def show_player_list(player: Player):
    """显示玩家列表 (管理员用)"""
    from endstone_tips.tips import tips_instance
    
    form = ActionForm(
        title="§e玩家列表",
        content="请选择要修改显示的玩家"
    )
    
    for online_player in tips_instance.server.online_players:
        form.add_button(
            text=online_player.name,
            icon="textures/ui/Friend2",
            on_click=lambda p, target=online_player.name: show_display_type_menu(p, target)
        )

    form.add_button(
        text="§c返回",
        icon="textures/ui/refresh_light",
        on_click=lambda p: show_main_menu(p)
    )
    
    form.on_close = lambda p: None
    player.send_form(form)


def show_display_type_menu(player: Player, target_player: Optional[str]):
    """显示类型选择菜单"""
    title = "§e默认显示设置" if target_player is None else f"§e{target_player} 的显示设置"
    
    form = ActionForm(
        title=title,
        content="请选择要修改的显示类型"
    )
    
    for display_name, display_type in DISPLAY_TYPES.items():
        form.add_button(
            text=display_name,
            icon="textures/ui/message",
            on_click=lambda p, dt=display_type, dn=display_name, t=target_player:
                show_settings_form(p, dt, dn, t)
        )

    # 返回按钮
    if target_player is not None:
        form.add_button(
            text="§c返回",
            icon="textures/ui/refresh_light",
            on_click=lambda p: show_player_list(p)
        )
    else:
        form.add_button(
            text="§c返回",
            icon="textures/ui/refresh_light",
            on_click=lambda p: show_main_menu(p)
        )
    
    form.on_close = lambda p: None
    player.send_form(form)


def show_personal_settings(player: Player):
    """显示玩家个人设置"""
    from endstone_tips.tips import tips_instance
    
    # 获取当前玩家配置
    config = tips_instance.player_config.load(player.name)
    displays = config.get("displays", {})
    
    form = ModalForm(title="§7个人显示设置")
    
    # 添加各显示类型的开关
    form.add_control(Toggle(
        label="Boss血条",
        default_value=displays.get("boss_bar", True)
    ))
    form.add_control(Toggle(
        label="计分板",
        default_value=displays.get("scoreboard", True)
    ))
    form.add_control(Toggle(
        label="底部显示",
        default_value=displays.get("tip", True)
    ))
    form.add_control(Toggle(
        label="头部显示",
        default_value=displays.get("nametag", True)
    ))
    form.add_control(Toggle(
        label="聊天栏公告",
        default_value=displays.get("broadcast", True)
    ))
    
    def on_submit(p: Player, data: list):
        # 保存设置
        tips_instance.player_config.set_display_enabled(p.name, "boss_bar", data[0])
        tips_instance.player_config.set_display_enabled(p.name, "scoreboard", data[1])
        tips_instance.player_config.set_display_enabled(p.name, "tip", data[2])
        tips_instance.player_config.set_display_enabled(p.name, "nametag", data[3])
        tips_instance.player_config.set_display_enabled(p.name, "broadcast", data[4])
        p.send_message("§a个人显示设置已保存!")
    
    form.on_submit = on_submit
    form.on_close = lambda p: show_main_menu(p)
    
    player.send_form(form)


def show_settings_form(player: Player, display_type: str, display_name: str, target_player: Optional[str]):
    """显示设置编辑表单"""
    from endstone_tips.tips import tips_instance

    form = ModalForm(title=f"§e{display_name} 设置")

    # 地图选择 - 兼容不同版本的 API
    try:
        # 尝试新版本 API
        level_list = list(tips_instance.server.levels)
    except AttributeError:
        try:
            # 尝试获取方法
            level_list = tips_instance.server.get_levels()
        except AttributeError:
            # 从在线玩家中收集世界名称
            level_list = []

    level_names = set()
    for level in level_list:
        try:
            level_names.add(level.name)
        except AttributeError:
            pass
    # 也从在线玩家中收集
    for p in tips_instance.server.online_players:
        try:
            level_names.add(p.level.name)
        except AttributeError:
            pass
    levels = ["default"] + sorted(level_names)

    # 获取当前主题配置
    if target_player is not None:
        # 获取目标玩家的主题配置
        theme = tips_instance.get_player_theme(target_player)
    else:
        # 获取默认主题配置
        theme = tips_instance.plugin_config.theme

    # 根据显示类型获取当前配置 (使用 default 世界的配置)
    current_config = {}
    if theme is not None:
        if display_type == "boss_bar":
            current_config = theme.get_boss_bar_set("default")
        elif display_type == "nametag":
            current_config = theme.get_nametag_set("default")
        elif display_type == "chat":
            current_config = theme.get_message_set("default")
        elif display_type == "tip":
            current_config = theme.get_tip_set("default")
        elif display_type == "broadcast":
            current_config = theme.get_broadcast_set("default")
        elif display_type == "scoreboard":
            current_config = theme.get_scoreboard_set("default")

    form.add_control(Dropdown(
        label="覆盖的地图 (default 为全地图)",
        options=levels,
        default_index=0
    ))

    # 是否开启
    form.add_control(Toggle(
        label="是否开启显示",
        default_value=current_config.get("是否开启", False)
    ))

    # 根据显示类型添加不同控件
    if display_type == "tip":
        show_type = current_config.get("显示类型", 0)
        form.add_control(Dropdown(
            label="显示类型",
            options=["tip", "popup", "action"],
            default_index=show_type if isinstance(show_type, int) and 0 <= show_type <= 2 else 0
        ))
        form.add_control(TextInput(
            label="显示内容",
            placeholder="变量参考变量文件",
            default_value=current_config.get("显示", "")
        ))

    elif display_type == "boss_bar":
        form.add_control(TextInput(
            label="轮播时间(秒)",
            placeholder="例如 5",
            default_value=str(current_config.get("间隔时间", 5))
        ))
        form.add_control(Toggle(
            label="是否根据玩家血量变化",
            default_value=current_config.get("是否根据玩家血量变化", False)
        ))
        # 将消息列表用 & 连接
        messages = current_config.get("消息轮播", [])
        messages_str = " & ".join(messages) if isinstance(messages, list) else ""
        form.add_control(TextInput(
            label="显示内容 (轮播用 & 隔开)",
            placeholder="变量参考变量文件",
            default_value=messages_str
        ))

    elif display_type == "nametag":
        form.add_control(TextInput(
            label="显示内容",
            placeholder="变量参考变量文件",
            default_value=current_config.get("显示", "")
        ))

    elif display_type == "scoreboard":
        form.add_control(TextInput(
            label="计分板标题",
            placeholder="变量参考变量文件",
            default_value=current_config.get("Title", "")
        ))
        # 将行列表用 & 连接
        lines = current_config.get("Line", [])
        lines_str = " & ".join(lines) if isinstance(lines, list) else ""
        form.add_control(TextInput(
            label="显示内容 (用 & 隔开每行)",
            placeholder="变量参考变量文件",
            default_value=lines_str
        ))

    elif display_type == "chat":
        form.add_control(Toggle(
            label="是否仅在世界内聊天",
            default_value=current_config.get("是否仅在世界内有效", False)
        ))
        form.add_control(TextInput(
            label="聊天格式",
            placeholder="{name}: {msg}",
            default_value=current_config.get("显示", "{name}: {msg}")
        ))

    elif display_type == "broadcast":
        form.add_control(TextInput(
            label="轮播时间(秒)",
            placeholder="例如 30",
            default_value=str(current_config.get("间隔时间", 30))
        ))
        # 将消息列表用 & 连接
        messages = current_config.get("消息轮播", [])
        messages_str = " & ".join(messages) if isinstance(messages, list) else ""
        form.add_control(TextInput(
            label="消息内容 (轮播用 & 隔开)",
            placeholder="变量参考变量文件",
            default_value=messages_str
        ))

    def on_submit(p: Player, data: list):
        # 处理表单提交
        p.send_message(f"§a设置已保存! (注: 当前版本暂不支持保存到配置文件)")
        p.send_message(f"§7收到数据: {data}")
        show_display_type_menu(p, target_player)

    form.on_submit = on_submit
    form.on_close = lambda p: show_display_type_menu(p, target_player)

    player.send_form(form)


def show_theme_selector(player: Player):
    """显示主题选择器"""
    from endstone_tips.tips import tips_instance
    
    form = ActionForm(
        title="§d样式选择",
        content="请选择你喜欢的样式"
    )
    
    # 获取当前玩家主题
    current_theme = tips_instance.player_config.get_theme(player.name)
    themes = tips_instance.theme_manager.list_themes()
    
    for theme in themes:
        # 标记当前使用的主题
        label = f"§a✓ {theme}" if theme == current_theme else theme
        form.add_button(
            text=label,
            icon="textures/ui/color_picker",
            on_click=lambda p, t=theme: _switch_player_theme(p, t)
        )

    form.add_button(
        text="§6重载所有主题",
        icon="textures/ui/refresh_light",
        on_click=lambda p: _reload_all_themes(p)
    )

    form.add_button(
        text="§c返回",
        icon="textures/ui/refresh_light",
        on_click=lambda p: show_main_menu(p)
    )
    
    form.on_close = lambda p: None
    player.send_form(form)


def _reload_config(player: Player):
    """重载配置"""
    from endstone_tips.tips import tips_instance
    from endstone_tips.config import PluginConfig
    
    try:
        tips_instance.plugin_config = PluginConfig(f"{tips_instance.data_folder}/config.toml")
        tips_instance.theme_manager.reload_all()
        tips_instance.player_config.clear_cache()
        player.send_message("§a配置重新加载成功!")
    except Exception as e:
        player.send_message(f"§c配置加载失败: {e}")


def _switch_player_theme(player: Player, theme_name: str):
    """切换玩家主题"""
    from endstone_tips.tips import tips_instance
    
    if not tips_instance.theme_manager.exists(theme_name):
        player.send_message(f"§c主题 '{theme_name}' 不存在")
        return
    
    # 保存玩家的主题选择
    tips_instance.player_config.set_theme(player.name, theme_name)
    player.send_message(f"§a已切换到主题: {theme_name}")
    
    # 重新打开主题选择器
    show_theme_selector(player)


def _reload_all_themes(player: Player):
    """重载所有主题"""
    from endstone_tips.tips import tips_instance
    
    tips_instance.theme_manager.reload_all()
    player.send_message(f"§a已重载 {len(tips_instance.theme_manager.list_themes())} 个主题")
    
    # 重新打开主题选择器
    show_theme_selector(player)
