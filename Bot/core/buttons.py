import discord


class GenericButtonView(discord.ui.View):
    def __init__(self, buttons: list):
        super().__init__(timeout=None)
        for button in buttons:
            self.add_item(GenericButton(
                button_name=button["label"],
                emoji=button["emoji"],
                style=button["style"],
                callback=button["callback"],
                custom_id=button["custom_id"] 
            ))


class GenericButton(discord.ui.Button):
    def __init__(self,  button_name: str, emoji:str, style: discord.ButtonStyle, callback, custom_id:str=None ):
        super().__init__(label= button_name, emoji=emoji, style=style, custom_id=custom_id)
        self.button_action = callback
    async def callback(self, ctx: discord.Interaction):
        
        for item in self.view.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True
                
        await ctx.message.edit(view=self.view)
        await self.button_action(ctx)




