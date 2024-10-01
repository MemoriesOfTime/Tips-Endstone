# **Tips - Endstone**
适用于Endstone的Tips插件，从 [Tips](https://github.com/SmallasWater/Tips) 移植  
目前项目正在开发中，功能仍不完善，请等待后续更新  

#### 使用说明
 1. 将本插件放置到` plugins`文件夹
 2. 自定义样式可参考 **`Tips变量.txt`** 文件
 3. 重启服务器即可正常使用
  
#### 如何注册变量？
创建一个类继承 `BaseVariable`
```python
from endstone_tips.utils.variables.base_variable import BaseVariable

class DemoVariable(BaseVariable):
    def __init__(self):
        super().__init__()
        pass

    def on_update(self):
        #在这里添加变量
        #{demo} 替换为 "演示"
        self.add_variable("{demo}", "演示")
        pass
```
注册创建的变量类
```python
from endstone_tips.utils.variables.default_variable import DefaultVariable

register_variable("demo", DemoVariable)
```