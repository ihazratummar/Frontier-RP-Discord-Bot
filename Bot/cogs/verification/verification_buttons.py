import discord
from Bot.core.constants import Color, Channel, Role
from Bot.core.buttons import GenericButtonView
from Bot.cogs.verification import nickname_checker
from Bot.core.helper_function import send_log
import asyncio


class NickNameVerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Проверять", style=discord.ButtonStyle.primary, custom_id="verify_button")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        await send_log(
            title=f"{interaction.user.name} logs",
            description=f"{interaction.user.name} has requested to verify their nickname.",
            color= discord.Color.from_str(Color.brand_color),
            guild= interaction.guild
        )
        await interaction.response.defer()
        thread = await interaction.channel.create_thread(name=f"Application {interaction.user.name}", type= discord.ChannelType.private_thread)
        await thread.add_user(interaction.user)

        rules_embed = discord.Embed(
            title="Обязательно прочитайте правила сервера",
            description="Пройдите ниже по ссылке , после прочтение подтвердите что вы согласны с правилами.",
            color= discord.Color.from_str(Color.brand_color)
        )
        rules_embed.add_field(
            name="Правила",
            value="[Прочитать правила](https://docs.google.com/document/d/14Z4TwIAko0WGgaxHwMIcRpHK_I37iKA6cYp-9Uj-0FE/edit?tab=t.0)"
        )

        buttons = [
            {"label": "Подтверждать", "emoji": "✅", "style": discord.ButtonStyle.primary, "callback": self.confirm_rules_click, "custom_id": "confirm_rules_click"},
            {"label": "Отклонить", "emoji": "❌", "style": discord.ButtonStyle.danger, "callback": self.decline_rules_click, "custom_id": "decline_rules_click"}
        ]
        view = GenericButtonView(buttons=buttons)
        await thread.send("Привет , давайте начнем с вами процесс верификации .", embed=rules_embed, view= view)
    
    async def confirm_rules_click(self, interaction: discord.Interaction):

        await send_log(
            title=f"{interaction.user.name} logs",
            description=f"{interaction.user.name} has agree to that rules",
            color= discord.Color.from_str(Color.brand_color),
            guild= interaction.guild
        )

        age_embed = discord.Embed(
            title="Возрастное ограничение в проекте +18",
            description="Подтверждаете что вам +18",
            color= discord.Color.from_str(Color.brand_color)
        )
        buttons = [
            {"label": "Да, подтверждаю", "emoji": "✅", "style": discord.ButtonStyle.success, "callback": self.on_yes_click, "custom_id": "yes_button"},
            {"label": "Нет", "emoji": "❌", "style": discord.ButtonStyle.danger, "callback": self.on_no_click, "custom_id": "no_button"}
        ]
        view = GenericButtonView(buttons=buttons)
        await interaction.response.send_message(embed=age_embed, view= view)


    async def decline_rules_click(self, interaction: discord.Interaction):

        await send_log(
            title=f"{interaction.user.name} logs",
            description=f"{interaction.user.name} has disagree to that rules",
            color= discord.Color.from_str(Color.brand_color),
            guild= interaction.guild
        )

        await interaction.response.send_message("Вы отклоняете правила! Канал будет удален через 5 секунд", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()



    async def on_yes_click(self, interaction: discord.Interaction):
        await interaction.response.send_modal(EnterNickNameModal())
        await send_log(
            title=f"{interaction.user.name} logs",
            description=f"{interaction.user.name} has agreed to be 18+",
            color= discord.Color.from_str(Color.brand_color),
            guild= interaction.guild
        )
        await interaction.followup.send("Вы подтвердили что вам есть +18 .")
        

    async def on_no_click(self, interaction: discord.Interaction, ):
        await interaction.response.send_message("Вы нажали «Нет»!", ephemeral=True)
        await send_log(
            title=f"{interaction.user.name} logs",
            description=f"❌ {interaction.user.name} has disagreed to be 18+",
            color= discord.Color.from_str(Color.brand_color),
            guild= interaction.guild
        )
        await asyncio.sleep(5)
        await interaction.channel.delete()


class EnterNickNameModal(discord.ui.Modal, title="Введите ваше игровое имя и фамилию"):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Define the TextInput inside __init__ to prevent duplicate IDs
        self.nickname_field = discord.ui.TextInput(
            label="Имя Фамилия вашего персонажа",  
            placeholder="Введите ваше игровое имя и фамилию.", 
            min_length=3, 
            max_length=20, 
            required=True,
            custom_id="nickname_input"  # Ensure a unique custom_id
        )

        self.add_item(self.nickname_field)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)

        await send_log(
            title=f"{interaction.user.name} logs",
            description= f"{interaction.user.name} has submitted the nickname {self.nickname_field.value}",
            color= discord.Color.from_str(Color.brand_color),
            guild= interaction.guild
        )
        

        if nickname_checker.is_nick_name_valid(self.nickname_field.value):    
            await member.edit(nick=self.nickname_field.value)

            role = guild.get_role(Role.verified)

            if role and role not in member.roles:
                await interaction.followup.send(f"Поздравляю 🎉, вы успешно прошли самый сложный этап нашего сервера . Имя и фамилия вашего персонажа {self.nickname_field.value} {role.name} . Спасибо и приятной игры на нашем сервере Frontier Role Play.")
                await asyncio.sleep(5)
                await member.add_roles(role)
            
            else:
                await interaction.followup.send(f"Поздравляю 🎉, вы успешно прошли самый сложный этап нашего сервера . Имя и фамилия вашего персонажа {self.nickname_field.value} {role.name} . Спасибо и приятной игры на нашем сервере Frontier Role Play.")

            await send_log(
                title=f"{interaction.user.name} logs",
                description= f"✅ Nickname set to `{self.nickname_field.value}` and role **{role.name}** assigned!",
                color= discord.Color.from_str(Color.brand_color),
                guild= interaction.guild
            )

            await asyncio.sleep(2)
            await interaction.channel.delete()
        else:
            nickname =  nickname_checker.suggest_valid_nickname(self.nickname_field.value)

            await send_log(
                title=f"{interaction.user.name} logs",
                description= f"❌ Nickname Inavlid and suggested {nickname}",
                color= discord.Color.from_str(Color.brand_color),
                guild= interaction.guild
            )

            embed = discord.Embed(
                title="Ваше имя и фамилия не соответствуют установленным правилам.",
                description=f"",
                color= discord.Color.from_str(Color.brand_color)
            )
            embed.add_field(
                name="** **", value= "1. Имя и фамилия должны быть написаны исключительно латиницей.", inline=False
            )
            embed.add_field(
                name="** **", 
                value="2. В имени и фамилии должна быть одна заглавная буква, полностью писать капсом запрещено (например: John Smith, но не JOHN SMITH).",inline=False
            )
            embed.add_field(
                name= "3. NonRP имена и фамилии запрещены, включая:",
                value="""
>>> Имена и фамилии реальных людей (знаменитостей, персонажей из фильмов, игр или мультфильмов).
Имена с оскорбительными словами или ненормативной лексикой.
Уменьшительно-ласкательные или сокращённые формы (например, Jonny вместо John).
""", inline=False
            )
            embed.add_field(name="** **", value="4. Имена персонажей из России, СНГ или постсоветских стран запрещены.", inline=False)
            embed.add_field(name="** **", value="5. Имя и фамилия должны соответствовать историческим реалиям Дикого Запада XIX века.", inline=False)
            embed.add_field(name="Предлагаю следующее", value= nickname)


            buttons = [
                {"label": "Написать заново", "emoji": "🔃", "style": discord.ButtonStyle.primary, "callback": self.resubmit_nickname, "custom_id": "submit_button"}

            ]
            view = GenericButtonView(
                buttons= buttons
            )

            await interaction.followup.send(embed=embed, view= view)

    async def resubmit_nickname(self, interaction: discord.Interaction):
        guild = interaction.guild
        await interaction.response.send_modal(EnterNickNameModal())
        