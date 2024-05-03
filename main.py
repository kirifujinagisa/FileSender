import os
from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import PersonNormalMessageReceived

@register(name="FileSender", description="A plugin for sending files to requesters", version="1.0", author="Assistant")
class FileSenderPlugin(BasePlugin):

    def __init__(self, host: APIHost):
        self.files_folder = "path/to/your/files/folder"  # 在此处填写你在本机存储想要发送文件的文件夹路径

    async def initialize(self):
        pass

    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message.strip()
        sender_id = ctx.event.sender_id

        # 如果消息以 "发送文件" 开头，则尝试发送指定的文件
        if msg.startswith("发送文件"):
            # 获取文件名（假设文件名即为用户发送的消息）
            file_name = msg.split("发送文件", 1)[-1].strip()
            
            # 遍历文件夹中的文件，查找与文件名相匹配的文件
            file_path = None
            for file in os.listdir(self.files_folder):
                if file_name.lower() in file.lower():  # 不区分大小写
                    file_path = os.path.join(self.files_folder, file)
                    break
            
            # 检查是否找到文件
            if file_path and os.path.exists(file_path):
                try:
                    # 发送文件
                    await ctx.send_file(sender_id, file_path)
                    ctx.add_return("reply", ["文件已发送"])
                except Exception as e:
                    ctx.add_return("reply", ["发送文件时出错：" + str(e)])
            else:
                ctx.add_return("reply", ["未找到匹配的文件"])
                
            ctx.prevent_default()

    def __del__(self):
        pass
