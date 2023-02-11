import discord
import button_helper as bh

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        discord.ui.View.timeout = None
        self.value = None          
        
    @discord.ui.button(label="LEFT", emoji="⬅️", style=discord.ButtonStyle.gray, row=0)
    async def left_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed, file = bh.press_button(interaction.guild.id, interaction.user.name, cmd="left")
        await interaction.response.edit_message(embed=embed, attachments=[file])
        
    @discord.ui.button(label="UP", emoji="⬆️", style=discord.ButtonStyle.gray, row=0)
    async def up_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed, file = bh.press_button(interaction.guild.id, interaction.user.name, cmd="up")
        await interaction.response.edit_message(embed=embed, attachments=[file])

    @discord.ui.button(label="DOWN", emoji="⬇️", style=discord.ButtonStyle.gray, row=0)
    async def down_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed, file = bh.press_button(interaction.guild.id, interaction.user.name, cmd="down")
        await interaction.response.edit_message(embed=embed, attachments=[file])
        
    @discord.ui.button(label="RIGHT", emoji="➡️", style=discord.ButtonStyle.gray, row=0)
    async def right_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed, file = bh.press_button(interaction.guild.id, interaction.user.name, cmd="right")
        await interaction.response.edit_message(embed=embed, attachments=[file])
        
    @discord.ui.button(label="A", emoji="🇦", style=discord.ButtonStyle.gray, row=1)
    async def a_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed, file = bh.press_button(interaction.guild.id, interaction.user.name, cmd="a")
        await interaction.response.edit_message(embed=embed, attachments=[file])
    
    @discord.ui.button(label="B", emoji="🇧", style=discord.ButtonStyle.gray, row=1)
    async def b_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed, file = bh.press_button(interaction.guild.id, interaction.user.name, cmd="b")
        await interaction.response.edit_message(embed=embed, attachments=[file])
    
    @discord.ui.button(label="START", emoji="🇸", style=discord.ButtonStyle.gray, row=1)
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed, file = bh.press_button(interaction.guild.id, interaction.user.name, cmd="start")
        await interaction.response.edit_message(embed=embed, attachments=[file])
    
    @discord.ui.button(label="SELECT", emoji="🇸", style=discord.ButtonStyle.gray, row=1)
    async def select_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed, file = bh.press_button(interaction.guild.id, interaction.user.name, cmd="select")
        await interaction.response.edit_message(embed=embed, attachments=[file])