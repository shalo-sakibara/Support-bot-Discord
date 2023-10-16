from typing import Optional
import disnake
from disnake.ext import commands


PREFIX = "/"
bot = commands.Bot(command_prefix=PREFIX, help_command=None,
                   intents=disnake.Intents.all())

"""Ивент который сообщает в консоль то, что бот запущен"""


@bot.event
async def on_ready():
    print(f"Бот // {bot.user} // готов к работе")

"""Ошибки"""


@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения этой команды!")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=disnake.Embed(
            description=f"Правильное использование команды: '{ctx.prefix}{ctx.command.name}' ({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"))

"""Кнопки для выдачи гендера"""


class Gender(disnake.ui.View):

    def __init__(self):
        super().__init__(timeout=20.0)
        self.value = Optional[bool]

    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="🚹")
    async def gender_man(self, button: disnake.ui.Button, ctx):
        self.value = False
        self.stop()

    @disnake.ui.button(style=disnake.ButtonStyle.red, emoji="🚺")
    async def gender_woman(self, button: disnake.ui.Button, ctx):
        self.value = True
        self.stop()


"""Ссылка на канал, которая отправляеться в ЛС пользователю"""


class Get_channel(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=1234.0)
        self.add_item(disnake.ui.Button(label="Отправь отзыв сюда",
                      url="Ссылка на текстовый канал с логами верефикации"))


"""Команда для выбора кнопок"""


@bot.command(name="verif")
@commands.has_permissions(administrator=True)
async def verif(ctx, member: disnake.Member):
    view = Gender()
    woman_role = disnake.utils.get(
        ctx.message.guild.roles, name="⠀")  # женская
    man_role = disnake.utils.get(ctx.message.guild.roles, name="⠀⠀")  # мужская
    unver_role = disnake.utils.get(ctx.message.guild.roles, name="unverify")
    channel = bot.get_channel('id текстового канала')
    await ctx.send(f"Выберите гендерку пользователю {member.mention}", view=view)
    await view.wait()

    if view.value is None:
        await ctx.send("Пропишите команду заново")
    elif view.value is True:
        await member.remove_roles(unver_role)
        await member.add_roles(woman_role)  # женская
        await channel.send(f"{ctx.author.mention} верефицировал(a) пользователя {member.mention} женским гендером")
        await ctx.channel.purge(limit=4)
    elif view.value is False:
        await member.remove_roles(unver_role)
        await member.add_roles(man_role)  # мужская
        await channel.send(f"{ctx.author.mention} верефицировал(а) пользователя {member.mention} мужским гендером")
        await ctx.channel.purge(limit=4)
    else:
        pass
    user = bot.get_user(member.id)
    await user.send(f"Привет {member.mention}. Ты прошел верификацию на нашем сервере, оставь отзыв(Всё ли понравилось?). И не забудь указать {ctx.author.mention} который провел верификацию", view=Get_channel())

"""Запуск бота с указанием токена"""
bot.run("ТОКЕН БОТА")
