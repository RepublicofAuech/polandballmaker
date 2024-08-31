import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import io
import os
from PIL import Image
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')

# Dictionaries to map inputs to corresponding images

ENEUROPE_COUNTRY = {
    'ポーランド': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/polandballpbmaker1.png?raw=true',
    'ロシア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/russiaballpbmaker.png?raw=true'
}
WSEUROPE_COUNTRY = {
    'フランス': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/franceballpbmaker.png?raw=true',
    'ドイツ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/germanyballpbmaker.png?raw=true',
    'イタリア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/italyballpbmaker.png?raw=true',
    'イギリス': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ukballpbmaker.png?raw=true',
    'トルコ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/turkeyballpbmaker.png?raw=true'
}

MIDEASCAUCASUS_COUNTRY = {
    'トルコ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/turkeyballpbmaker.png?raw=true',
    'エジプト': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/egyptpbmaker.png?raw=true',
    'サウジアラビア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/saudiarabiaballpbmaker.png?raw=true',
    'イスラエル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/israelballpbmaker.png?raw=true'
}

ESEASIA_COUNTRY = {
    '日本': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/japanballpbmaker.png?raw=true',
    '中国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/chinaballpbmaker.png?raw=true',
    '台湾': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/taiwanballpbmaker.png?raw=true',

    'インドネシア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/indonesiaballpbmaker.png?raw=true',
    'シンガポール': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/trianglesgballpbmaker.png?raw=true',
    '韓国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/southkoreaballpbmaker.png?raw=true',
}

CSASIA_COUNTRY = {
    'インド': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/indiaballpbmaker.png?raw=true',
    'ネパール': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nepalballpbmaker.png?raw=true'

}

NCAMERICA_COUNTRY = {
    'アメリカ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/usaballpbmaker.png?raw=true',
    'メキシコ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/mexicoballpbmaker.png?raw=true',
    'カナダ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/canadaballpbmaker.png?raw=true'

}

SAMERICA_COUNTRY = {
    'アルゼンチン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/argentinaballpbmaker.png?raw=true',
    'ブラジル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/brazilballpbmaker.png?raw=true'

}

NWAFRICA_COUNTRY = {
    'エジプト': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/egyptpbmaker.png?raw=true',
    'リビア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/libyapbmaker.png?raw=true',
    'モロッコ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/moroccopbmaker.png?raw=true',
    'チュニジア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tunisiapbmaker.png?raw=true',
    'アルジェリア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/algeriapbmaker.png?raw=true'

}

CSAFRICA_COUNTRY = {
    '南アフリカ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/southafricaballpbmaker.png?raw=true',

}

OCEANIA_COUNTRY = {
    'ニュージーランド': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/newzealandballpbmaker.png?raw=true',
    'オーストラリア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/australiaballpbmaker.png?raw=true',

}


TOHTOCHU_PREF = {
    '愛知県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/aichiballpbmaker.png?raw=true',
    '千葉県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/chibapbmaker.png?raw=true',
    '北海道': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/hokkaidopbmaker.png?raw=true',
    '茨城県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ibarakipbmaker.png?raw=true',
    '神奈川県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kanagawaballpbmaker.png?raw=true',
    '宮城県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/miyagipbmaker.png?raw=true',
    '新潟県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/niigataballpbmaker.png?raw=true',
    '埼玉県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/saitamaballpbmaker.png?raw=true',
    '東京都': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tokyoballpbmaker.png?raw=true',
    '東京都シンボルver': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tokyoballpbmaker2.png?raw=true',
    '静岡県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/shizuokapbmaker.png?raw=true',
    '長野県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/naganopbmaker.png?raw=true',
    '岐阜県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/gifupbmaker.png?raw=true',
    '福島県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/fukushimapbmaker.png?raw=true'
}

KINTOKYU_PREF = {
    '広島県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/hiroshimapbmaker.png?raw=true',
    '兵庫県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/hyogopbmaker.png?raw=true',
    '京都府': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kyotopbmaker.png?raw=true',
    '福岡県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/fukuokapbmaker.png?raw=true',
    '大阪府': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/osakaprefballpbmaker.png?raw=true',
    '熊本県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kumamotopbmaker.png?raw=true',
    '三重県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/miepbmaker.png?raw=true',
    '愛媛県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ehimepbmaker.png?raw=true',
    '岡山県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/okayamapbmaker.png?raw=true'
}

TOHTOKAN_CORE = {
    '宇都宮市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/utsunomiyaballpbmaker.png?raw=true',
    '水戸市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/mitoballpbmaker.png?raw=true'
}

CHUTOKIN_CORE = {
    '姫路市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/himejicitypbmaker.png?raw=true',
    '金沢市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kanazawaballpbmaker.png?raw=true',
    '豊田市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/toyotapbmaker.png?raw=true',

}


CHUTOKYU_CORE = {
    '鹿児島市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kagoshimaballpbmaker.png?raw=true',
    '大分市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/oitacitypbmaker.png?raw=true',
    '松山市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/matsuyamapbmaker.png?raw=true'
}

ORDINANCE_CITY = {
    '大阪市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/osakaballpbmaker.png?raw=true',
    '福岡市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/fukuokacitypbmaker.png?raw=true',
    '広島市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/hiroshimacitypbmaker.png?raw=true',
    '名古屋市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nagoyapbmaker.png?raw=true',
    '仙台市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/sendaipbmaker.png?raw=true',
    '札幌市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/sapporopbmaker.png?raw=true',
    '横浜市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/yokohamapbmaker.png?raw=true',
    '熊本市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kumamotocityballpbmaker.png?raw=true',
    '岡山市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/okayamaballpbmaker.png?raw=true',
    '静岡市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/shizuokaballpbmaker.png?raw=true',
    '新潟市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/niigatacityballpbmaker.png?raw=true',
    '北九州市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kitakyushuballpbmaker.png?raw=true',
    '川崎市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kawasakiballpbmaker.png?raw=true',
    'さいたま市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/saitamacityballpbmaker.png?raw=true',
    '浜松市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/hamamatsuballpbmaker.png?raw=true',
    '堺市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/sakaiballpbmaker.png?raw=true',
    '相模原市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/sagamiharaballpbmaker.png?raw=true'
}

OTHERS = {
    'EU': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/euballpbmaker.png?raw=true',
    'An Untitled Editor': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/aueballpbmaker.png?raw=true',
    '鳥取県信者ボール': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/believertottoripbmaker.png?raw=true',
    'きんら': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kinrapbmaker.png?raw=true',
    'きんら(旧)': 'https://raw.githubusercontent.com/RepublicofAuech/polandballmaker/main/flags/kinrapbmaker2.png?raw=true',
    '大日本帝国(mania)': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/japaneseempireballpbmaker.png?raw=true',
    'シンガポール(球状)': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/singaporeballpbmaker.png?raw=true',
    'カザフスタン(球状)': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/circlekazakhballpbmaker.png?raw=true',
    'ネパール(球状)': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/circlenepalballpbmaker.png?raw=true',
}

NONE = {
    'なし': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/invisibleimage.png?raw=true'
}

EXPRESSION_IMAGES = {
    '普通': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/normaleyes.png?raw=true',
    '楽しい': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/happyeyes.png?raw=true',
    'ニコニコ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/veryhappyeyes.png?raw=true',
    '悲しい': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/sadeyes.png?raw=true',
    '号泣': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/cryingeyes.png?raw=true',
    '真面目': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/kindaserious.png?raw=true',
    '怒り': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/angryeyes.png?raw=true',
    'なし': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/invisibleimage.png?raw=true'
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
    '西・南ヨーロッパの国々': WSEUROPE_COUNTRY,
    '東・北ヨーロッパの国々': ENEUROPE_COUNTRY,
    '東・東南アジアの国々': ESEASIA_COUNTRY,
    '中東・コーカサスの国々': MIDEASCAUCASUS_COUNTRY,
    '中央・南アジアの国々': CSASIA_COUNTRY,
    '北中米の国々': NCAMERICA_COUNTRY,
    '南米の国々': SAMERICA_COUNTRY,
    '北・西アフリカの国々': NWAFRICA_COUNTRY,
    '中央・南アフリカの国々': CSAFRICA_COUNTRY,
    'オセアニアの国々:': OCEANIA_COUNTRY,
    '都道府県（東北から中部）': TOHTOCHU_PREF,
    '都道府県（近畿から九州）': KINTOKYU_PREF,
    '政令市': ORDINANCE_CITY,
    '中核市（東北から関東）': TOHTOKAN_CORE,
    '中核市（中部から近畿）': CHUTOKIN_CORE,
    '中核市（中国から九州）': CHUTOKYU_CORE,
    'その他': OTHERS,
    'なし': NONE
}

CATEGORY_CHOICES = [
    app_commands.Choice(name='西・南ヨーロッパの国々', value='西・南ヨーロッパの国々'),
    app_commands.Choice(name='東・北ヨーロッパの国々', value='東・北ヨーロッパの国々'),
    app_commands.Choice(name='中東・コーカサスの国々', value='中東・コーカサスの国々'),
    app_commands.Choice(name='東・東南アジアの国々', value='東・東南アジアの国々'),
    app_commands.Choice(name='中央・南アジアの国々', value='中央・南アジアの国々'),
    app_commands.Choice(name='北中米の国々', value='北中米の国々'),
    app_commands.Choice(name='カリブ海の国々', value='カリブ海の国々'),
    app_commands.Choice(name='南米の国々', value='南米の国々'),
    app_commands.Choice(name='北・西アフリカの国々', value='北・西アフリカの国々'),
    app_commands.Choice(name='中央・南アフリカの国々', value='中央・南アフリカの国々'),
    app_commands.Choice(name='東アフリカの国々', value='東アフリカの国々'),
    app_commands.Choice(name='オセアニアの国々', value='オセアニアの国々'),
    app_commands.Choice(name='都道府県（東北から中部）', value='都道府県（東北から中部）'),
    app_commands.Choice(name='都道府県（近畿から九州）', value='都道府県（近畿から九州）'),
    app_commands.Choice(name='政令市', value='政令市'),
    app_commands.Choice(name='中核市（東北から関東）', value='中核市（東北から関東）'),
    app_commands.Choice(name='中核市（中部から近畿）', value='中核市（中部から近畿）'),
    app_commands.Choice(name='中核市（中国から九州）', value='中核市（中国から九州）'),
    app_commands.Choice(name='その他', value='その他'),
    app_commands.Choice(name='なし', value='なし')
]

EXPRESSION_CHOICES = [
    app_commands.Choice(name='普通', value='普通'),
    app_commands.Choice(name='楽しい', value='楽しい'),
    app_commands.Choice(name='ニコニコ', value='ニコニコ'),
    app_commands.Choice(name='悲しい', value='悲しい'),
    app_commands.Choice(name='号泣', value='号泣'),
    app_commands.Choice(name='真面目', value='真面目'),
    app_commands.Choice(name='怒り', value='怒り'),
    app_commands.Choice(name='なし', value='なし')
]

POSITION_CHOICES = [app_commands.Choice(
    name=pos, value=pos) for pos in POSITION_COMMANDS.keys()]

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
                image = Image.open(data)
                return image.convert('RGBA')
            else:
                print(f"Error fetching image: HTTP {response.status}")
                return None

# Function to merge the flag and expression images with more offset for each predefined position


def merge_images(flag_img, expression_img, position):
    if expression_img is None:
        print("No expression image provided.")
        # Optionally, you can handle this case differently, such as using a default image or skipping this step
        return flag_img

    # Convert expression_img to RGBA if not already
    if expression_img.mode != 'RGBA':
        expression_img = expression_img.convert('RGBA')

    # Resize the expression image to 100% of the flag's size
    new_width = int(flag_img.width * 1)
    new_height = int(flag_img.height * 1)
    expression_img = expression_img.resize(
        (new_width, new_height), Image.LANCZOS)

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
    x, y = positions.get(position, ((flag_img.width - expression_img.width) //
                         2, (flag_img.height - expression_img.height) // 2))

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
                   country: str,
                   expression: app_commands.Choice[str],
                   position: app_commands.Choice[str]):

    await interaction.response.defer()

    # Fetch the flag URL based on category and country
    flag_url = CATEGORY_FLAGS[category.value].get(country)
    if not flag_url:
        await interaction.response.send_message("指定された国や地域の旗画像が見つかりませんでした", ephemeral=True)
        return

    # Fetch the expression image URL or set to None if expression is 'なし'
    expression_url = EXPRESSION_IMAGES.get(expression.value, None)
    
    # Fetch the images
    flag_img = await fetch_image(flag_url)
    expression_img = await fetch_image(expression_url) if expression_url else None
    
    if not flag_img:
        await interaction.response.send_message("旗の画像を取得できませんでした。再試行してください", ephemeral=True)
        return

    # Merge images based on position
    try:
        combined_img = merge_images(flag_img, expression_img, position.value)
    except Exception as e:
        await interaction.response.send_message(f"画像の合成中にエラーが発生しました: {e}", ephemeral=True)
        return

    # Save and send the image
    with io.BytesIO() as output:
        combined_img.save(output, format='PNG')
        output.seek(0)
        file = discord.File(output, filename='polandball.png')
        await interaction.followup.send(file=file)

load_dotenv()
bot.run(os.getenv("TOKEN"))
