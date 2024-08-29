import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import io
import os
from PIL import Image
from flask import Flask
import threading

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

# Flask app to keep the bot online
app = Flask(__name__)

@app.route('/')
def home():
    return "The bot is running!"

# Function to run the Flask server in a separate thread
def run_flask():
    app.run(host='0.0.0.0', port=8080)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')

# Dictionaries to map inputs to corresponding images
FLAG_COUNTRY = {
    '日本': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/japanballpbmaker.png?raw=true',
    'ブラジル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/brazilballpbmaker.png?raw=true'
}

FLAG_PREFECTURE = {
    '愛知県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/aichiballpbmaker.png?raw=true'
}

CORE_CITY = {
    '鹿児島市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kagoshimaballpbmaker.png?raw=true'
    # Add more cities as needed
}

ORDINANCE_CITY = {
    '大阪市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/osakaballpbmaker.png?raw=true'
}

EXPRESSION_IMAGES = {
    '普通': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/normaleyes.png?raw=true',
    'ニコニコ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/veryhappyeyes.png?raw=true'
}

POSITION_COMMANDS = {
    '真ん中': '目の位置は真ん中に設定されました。',
    '上': '目の位置は上に設定されました。',
    '下': '目の位置は下に設定されました。',
    '左': '目の位置は左に設定されました。',
    '右': '目の位置は右に設定されました。',
    '右上': '目の位置は右上に設定されました。',
    '右下': '目の位置は右下に設定されました。',
    '左下': '目の位置は左下に設定されました。',
    '左上': '目の位置は左上に設定されました。',
}

CATEGORY_FLAGS = {
    '国': FLAG_COUNTRY,
    '都道府県': FLAG_PREFECTURE,
    '政令市': ORDINANCE_CITY,
    '中核市': CORE_CITY
}

CATEGORY_CHOICES = [
    app_commands.Choice(name='国', value='国'),
    app_commands.Choice(name='都道府県', value='都道府県'),
    app_commands.Choice(name='政令市', value='政令市'),
    app_commands.Choice(name='中核市', value='中核市'),
]

EXPRESSION_CHOICES = [
    app_commands.Choice(name='普通', value='普通'),
    app_commands.Choice(name='ニコニコ', value='ニコニコ'),
]

POSITION_CHOICES = [app_commands.Choice(name=pos, value=pos) for pos in POSITION_COMMANDS.keys()]

# Function to dynamically provide country/prefecture/city options based on category
async def get_country_choices(interaction: discord.Interaction, current: str):
    category = interaction.namespace.category
    flags = CATEGORY_FLAGS.get(category, {})
    return [app_commands.Choice(name=name, value=name) for name in flags.keys() if current.lower() in name.lower()]

# Function to download an image from a URL
async def fetch_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = io.BytesIO(await response.read())
                return Image.open(data)
            else:
                return None

# Function to merge the flag and expression images with more offset for each predefined position
def merge_images(flag_img, expression_img, position):
    # Resize the expression image to 100% of the flag's size
    new_width = int(flag_img.width * 1)
    new_height = int(flag_img.height * 1)
    expression_img = expression_img.resize((new_width, new_height), Image.LANCZOS)

    # Define offset values for more exaggerated positions
    offset_x, offset_y = 120, 120  # Adjust these values for more or less offset

    # Define positions with more offset
    positions = {
        '真ん中': ((flag_img.width - expression_img.width) // 2, (flag_img.height - expression_img.height) // 2),
        '上': ((flag_img.width - expression_img.width) // 2, -offset_y),
        '下': ((flag_img.width - expression_img.width) // 2, flag_img.height - expression_img.height + offset_y),
        '左': (-offset_x, (flag_img.height - expression_img.height) // 2),
        '右': (flag_img.width - expression_img.width + offset_x, (flag_img.height - expression_img.height) // 2),
        '右上': (flag_img.width - expression_img.width + offset_x, -offset_y),
        '右下': (flag_img.width - expression_img.width + offset_x, flag_img.height - expression_img.height + offset_y),
        '左下': (-offset_x, flag_img.height - expression_img.height + offset_y),
        '左上': (-offset_x, -offset_y),
    }

    # Get the coordinates for the given position
    x, y = positions.get(position, ((flag_img.width - expression_img.width) // 2, (flag_img.height - expression_img.height) // 2))

    # Merge the expression onto the flag image
    combined_img = flag_img.copy()
    combined_img.paste(expression_img, (x, y), expression_img)

    return combined_img

# Command to create the Polandball image
@bot.tree.command(name='pb_maker', description='指定されたポーランドボールを作成します')
@app_commands.describe(
    category='柄のカテゴリーを選んでください',
    country='国、都道府県または市区町村を選んでください',
    expression='ボールの表情を選んでください',
    position='目の位置を選んでください'
)
@app_commands.choices(category=CATEGORY_CHOICES, expression=EXPRESSION_CHOICES, position=POSITION_CHOICES)
@app_commands.autocomplete(country=get_country_choices)
async def pb_maker(interaction: discord.Interaction, 
                   category: app_commands.Choice[str], 
                   country: str,  # Changed to a regular string annotation
                   expression: app_commands.Choice[str], 
                   position: app_commands.Choice[str]):

    # Fetch the corresponding image URLs
    flags = CATEGORY_FLAGS.get(category.value, {})
    flag_image = await fetch_image(flags.get(country, None))  # Use country directly
    expression_image = await fetch_image(EXPRESSION_IMAGES.get(expression.value, None))
    position_output = POSITION_COMMANDS.get(position.value, '位置設定が見つかりません')

    if flag_image and expression_image:
        # Merge the images
        merged_image = merge_images(flag_image, expression_image, position.value)

        # Save the merged image to a bytes buffer
        buffer = io.BytesIO()
        merged_image.save(buffer, format='PNG')
        buffer.seek(0)

        # Send the merged image
        await interaction.response.send_message(
            content=f"ポーランドボールの作成に成功しました",
            file=discord.File(buffer, filename='pbmakerball.png')
        )
    else:
        await interaction.response.send_message("画像の取得に失敗しました")

thread = threading.Thread(target=run_flask)
thread.start()

# Run the bot
bot.run(os.getenv("TOKEN"))
