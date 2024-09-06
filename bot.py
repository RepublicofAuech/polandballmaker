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
    'チェコ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/czechiaballpbmaker.png?raw=true',
    'スロバキア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/slovakiaballpbmaker.png?raw=true',
    'スロベニア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/sloveniaballpbmaker.png?raw=true',
    'ハンガリー': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/hungaryballpbmaker.png?raw=true',
    'セルビア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/serbiaballpbmaker.png?raw=true',
    'クロアチア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/croatiaballpbmaker.png?raw=true',
    'ボスニア・ヘルツェゴビナ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/bosniaballpbmaker.png?raw=true',
    'モンテネグロ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/montenegroballpbmaker.png?raw=true',
    'アルバニア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/albaniaballpbmaker.png?raw=true',
    '北マケドニア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/northmacedoniaballpbmaker.png?raw=true',
    'ブルガリア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/bulgariaballpbmaker.png?raw=true',
    'ルーマニア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/romaniaballpbmaker.png?raw=true',
    'ベラルーシ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/belarusballpbmaker.png?raw=true',
    'モルドバ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/moldovaballpbmaker.png?raw=true',
    'ウクライナ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ukraineballpbmaker.png?raw=true',
    'エストニア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/estoniaballpbmaker.png?raw=true',
    'ラトビア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/latviaballpbmaker.png?raw=true',
    'リトアニア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/lithuaniaballpbmaker.png?raw=true',
    'フィンランド': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/finlandballpbmaker.png?raw=true',
    'スウェーデン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/swedenballpbmaker.png?raw=true',
    'ノルウェー': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/norwayballpbmaker.png?raw=true',
    'アイスランド': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/icelandballpbmaker.png?raw=true',
    'ロシア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/russiaballpbmaker.png?raw=true',
    'コソボ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kosovoballpbmaker.png?raw=true'
}
WSEUROPE_COUNTRY = {
    'フランス': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/franceballpbmaker.png?raw=true',
    'ドイツ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/germanyballpbmaker.png?raw=true',
    'イタリア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/italyballpbmaker.png?raw=true',
    'バチカン市国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/vaticanballpbmaker.png?raw=true',
    'イギリス': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ukballpbmaker.png?raw=true',
    'アイルランド': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/irelandballpbmaker.png?raw=true',
    'オランダ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/netherlandsballpbmaker.png?raw=true',
    'ルクセンブルク': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/luxembourgballpbmaker.png?raw=true',
    'ベルギー': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/belgiumballpbmaker.png?raw=true',
    'スペイン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/spainballpbmaker.png?raw=true',
    'ポルトガル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/portugalballpbmaker.png?raw=true',
    'スイス': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/switzerlandballpbmaker.png?raw=true',
    'オーストリア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/austriaballpbmaker.png?raw=true',
    'デンマーク': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/denmarkballpbmaker.png?raw=true',
    'ギリシャ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/greeceballpbmaker.png?raw=true',
    'トルコ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/turkeyballpbmaker.png?raw=true'
}

WASIA_COUNTRY = {
    'トルコ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/turkeyballpbmaker.png?raw=true',
    'イスラエル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/israelballpbmaker.png?raw=true',
    'サウジアラビア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/saudiarabiaballpbmaker.png?raw=true',
    'レバノン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/lebanonballpbmaker.png?raw=true',
    'シリア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/syriaballpbmaker.png?raw=true',
    'オマーン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/omanballpbmaker.png?raw=true',
    'パレスチナ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/palestineballpbmaker.png?raw=true',
    'イスラエル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/israelballpbmaker.png?raw=true',
    'バーレーン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/bahrainballpbmaker.png?raw=true',
    'カタール': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/qatarballpbmaker.png?raw=true',
    'クウェート': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kuwaitballpbmaker.png?raw=true',
    'イラク': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/iraqballpbmaker.png?raw=true',
    'イラン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/iranballpbmaker.png?raw=true',
    'イエメン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/yemenballpbmaker.png?raw=true',
    'アルメニア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/armeniaballpbmaker.png?raw=true',
    'アゼルバイジャン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/azerbaijanballpbmaker.png?raw=true',
    'ジョージア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/georgiaballpbmaker.png?raw=true',
    'キプロス': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/cyprusballpbmaker.png?raw=true',
    'アラブ首長国連邦': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/uaeballpbmaker.png?raw=true'
}

ESEASIA_COUNTRY = {
    '日本': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/japanballpbmaker.png?raw=true',
    '中国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/chinaballpbmaker.png?raw=true',
    '台湾': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/taiwanballpbmaker.png?raw=true',
    'インドネシア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/indonesiaballpbmaker.png?raw=true',
    'シンガポール': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/trianglesgballpbmaker.png?raw=true',
    '韓国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/southkoreaballpbmaker.png?raw=true',
    '香港': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/hongkongballpbmaker.png?raw=true',
    'マカオ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/macauballpbmaker.png?raw=true',
    'モンゴル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/mongoliaballpbmaker.png?raw=true',
    'タイ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/thailandballpbmaker.png?raw=true',
    'ベトナム': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/vietnamballpbmaker.png?raw=true',
    'マレーシア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/malaysiaballpbmaker.png?raw=true',
    'フィリピン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/philippinesballpbmaker.png?raw=true',
    'カンボジア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/cambodiaballpbmaker.png?raw=true',
    'ミャンマー': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/myanmarballpbmaker.png?raw=true',
    'ラオス': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/laosballpbmaker.png?raw=true',
    '北朝鮮': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/northkoreaballpbmaker.png?raw=true'
}

CSASIA_COUNTRY = {
    'ウズベキスタン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/uzbekistanballpbmaker.png?raw=true',
    'キルギス': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kyrgyzstanballpbmaker.png?raw=true',
    'トルクメニスタン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/turkmenistanballpbmaker.png?raw=true',
    'タジキスタン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tajikistanballpbmaker.png?raw=true',
    'カザフスタン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kazakhstanballpbmaker.png?raw=true',
    'インド': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/indiaballpbmaker.png?raw=true',
    'パキスタン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/pakistanballpbmaker.png?raw=true',
    'ネパール': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nepalballpbmaker.png?raw=true',
    'アフガニスタン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/afghanistanballpbmaker.png?raw=true',
    'アフガニスタン(旧)': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/afghanistanballpbmaker2.png?raw=true',
    'バングラデシュ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/bangladeshballpbmaker.png?raw=true',
    'ブータン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/bhutanballpbmaker.png?raw=true',
    'スリランカ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/srilankaballpbmaker.png?raw=true'
}

NCAMERICA_COUNTRY = {
    'アメリカ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/usaballpbmaker.png?raw=true',
    'メキシコ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/mexicoballpbmaker.png?raw=true',
    'カナダ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/canadaballpbmaker.png?raw=true',
    'グアテマラ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/guatemalaballpbmaker.png?raw=true',
    'ニカラグア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nicaraguaballpbmaker.png?raw=true',
    'ベリーズ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/belizeballpbmaker.png?raw=true',
    'エルサルバドル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/elsalvadorballpbmaker.png?raw=true',
    'ホンジュラス': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/hondurasballpbmaker.png?raw=true',
    'コスタリカ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/costaricaballpbmaker.png?raw=true',
    'パナマ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/panamballpbmaker.png?raw=true'
}

CARIBBEAN_COUNTRY = {
    'アンティグア・バーブーダ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/antiguaballpbmaker.png?raw=true',
    'キューバ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/cubaballpbmaker.png?raw=true',
    'ジャマイカ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/jamaicaballpbmaker.png?raw=true',
    'ドミニカ国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/dominicaballpbmaker.png?raw=true',
    'ドミニカ共和国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/dominicanrepballpbmaker.png?raw=true',
    'ハイチ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/haitiballpbmaker.png?raw=true',
}

SAMERICA_COUNTRY = {
    'アルゼンチン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/argentinaballpbmaker.png?raw=true',
    'チリ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/chileballpbmaker.png?raw=true',
    'スリナム': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/surinameballpbmaker.png?raw=true',
    'ガイアナ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/guyanaballpbmaker.png?raw=true',
    'フランス領ギアナ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/frenchguianaballpbmaker.png?raw=true',
    'ベネズエラ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/venezuelaballpbmaker.png?raw=true',
    'コロンビア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/colombiaballpbmaker.png?raw=true',
    'エクアドル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ecuadorballpbmaker.png?raw=true',
    'ペルー': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/peruballpbmaker.png?raw=true',
    'ウルグアイ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/uruguayballpbmaker.png?raw=true',
    'ボリビア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/boliviaballpbmaker.png?raw=true',
    'パラグアイ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/paraguayballpbmaker.png?raw=true',
    'ブラジル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/brazilballpbmaker.png?raw=true'

}

NWAFRICA_COUNTRY = {
    'エジプト': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/egyptpbmaker.png?raw=true',
    'リビア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/libyapbmaker.png?raw=true',
    'モロッコ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/moroccopbmaker.png?raw=true',
    'チュニジア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tunisiapbmaker.png?raw=true',
    'アルジェリア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/algeriapbmaker.png?raw=true',
    'スーダン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/sudanballpbmaker.png?raw=true',
    '西サハラ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/westernsaharaballpbmaker.png?raw=true',
    'モーリタニア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/mauritaniaballpbmaker.png?raw=true',
    'マリ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/maliballpbmaker.png?raw=true',
    'ニジェール': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nigerballpbmaker.png?raw=true',
    'ナイジェリア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nigeriaballpbmaker.png?raw=true',
    'ブルキナファソ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/burkinafasoballpbmaker.png?raw=true',
    'ベナン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/beninballpbmaker.png?raw=true',
    'トーゴ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/togoballpbmaker.png?raw=true',
    'ガーナ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ghanaballpbmaker.png?raw=true',
    'コートジボワール': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ivorycoastballpbmaker.png?raw=true',
    'リベリア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/liberiaballpbmaker.png?raw=true',
    'シエラレオネ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/sierraleoneballpbmaker.png?raw=true',
    'ギニア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/guineaballpbmaker.png?raw=true',
    'ギニアビサウ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/guineabissauballpbmaker.png?raw=true',
    'セネガル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/senegalballpbmaker.png?raw=true',
    'ガンビア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/thegambiaballpbmaker.png?raw=true',
    'カーボベルデ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/capeverdeballpbmaker.png?raw=true'
}

CSAFRICA_COUNTRY = {
    'アンゴラ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/angolaballpbmaker.png?raw=true',
    'カメルーン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/cameroonballpbmaker.png?raw=true',
    '中央アフリカ共和国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/carballpbmaker.png?raw=true',
    'チャド': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/chadballpbmaker.png?raw=true',
    'コンゴ民主共和国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/drcballpbmaker.png?raw=true',
    'コンゴ共和国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/congoballpbmaker.png?raw=true',
    '赤道ギニア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/equatorialguineaballpbmaker.png?raw=true',
    'ガボン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/gabonballpbmaker.png?raw=true',
    'サントメ・プリンシペ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/saotomeballpbmaker.png?raw=true',
    '南アフリカ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/southafricaballpbmaker.png?raw=true',
    'レソト': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/lesothoballpbmaker.png?raw=true',
    'エスワティニ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/eswatiniballpbmaker.png?raw=true',
    'ボツワナ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/botswanaballpbmaker.png?raw=true',
    'ナミビア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/southafricaballpbmaker.png?raw=true'
}

EAFRICA_COUNTRY = {
    'エリトリア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/eritreaballpbmaker.png?raw=true',
    'ジブチ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/djiboutiballpbmaker.png?raw=true',
    'エチオピア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ethiopiaballpbmaker.png?raw=true',
    'ソマリア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/somaliaballpbmaker.png?raw=true',
    'ソマリランド': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/somalilandballpbmaker.png?raw=true',
    'エチオピア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ethiopiaballpbmaker.png?raw=true',
    '南スーダン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/southsudanballpbmaker.png?raw=true',
    'ケニア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kenyaballpbmaker.png?raw=true',
    'ウガンダ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ugandaballpbmaker.png?raw=true',
    'ルワンダ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/rwandaballpbmaker.png?raw=true',
    'ブルンジ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/burundiballpbmaker.png?raw=true',
    'タンザニア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tanzaniaballpbmaker.png?raw=true',
    'マラウイ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/malawiballpbmaker.png?raw=true',
    'モザンビーク': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/mozambiqueballpbmaker.png?raw=true',
    'ザンビア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/zambiaballpbmaker.png?raw=true',
    'ジンバブエ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/zimbabweballpbmaker.png?raw=true',
    'マダガスカル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/madagascarballpbmaker.png?raw=true',
    'モーリシャス': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/mauritiusballpbmaker.png?raw=true',
    'セーシェル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/seychellesballpbmaker.png?raw=true',
    'コモロ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/comorosballpbmaker.png?raw=true'
}

OCEANIA_COUNTRY = {
    'ニュージーランド': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/newzealandballpbmaker.png?raw=true',
    'オーストラリア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/australiaballpbmaker.png?raw=true',
    'ツバル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tuvaluballpbmaker.png?raw=true',
    'キリバス': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kiribatiballpbmaker.png?raw=true',
    'サモア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/samoaballpbmaker.png?raw=true',
    'マーシャル諸島': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/marshallballpbmaker.png?raw=true',
    'ソロモン諸島': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/solomonballpbmaker.png?raw=true',
    'ナウル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nauruballpbmaker.png?raw=true',
    'ミクロネシア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/micronesiaballpbmaker.png?raw=true',
    'バヌアツ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/vanuatuballpbmaker.png?raw=true',
    'パラオ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/palauballpbmaker.png?raw=true',
    'トンガ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tongaballpbmaker.png?raw=true',
    'パプアニューギニア': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/papuaballpbmaker.png?raw=true'
}


TOHTOCHU_PREF = {
    '愛知県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/aichiballpbmaker.png?raw=true',
    '青森県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/aomoriballpbmaker.png?raw=true',
    '岩手県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/iwateballpbmaker.png?raw=true',
    '秋田県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/akitaballpbmaker.png?raw=true',
    '山形県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/yamagataballpbmaker.png?raw=true',
    '栃木県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tochigiballpbmaker.png?raw=true',
    '群馬県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/gunmaballpbmaker.png?raw=true',
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
    '富山県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/toyamaballpbmaker.png?raw=true',
    '石川県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ishikawaballpbmaker.png?raw=true',
    '福井県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/fukuiballpbmaker.png?raw=true',
    '山梨県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/yamanashiballpbmaker.png?raw=true',
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
    '滋賀県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/shigaballpbmaker.png?raw=true',
    '奈良県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/naraballpbmaker.png?raw=true',
    '和歌山県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/wakayamaballpbmaker.png?raw=true',
    '鳥取県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tottoriballpbmaker.png?raw=true',
    '島根県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/shimaneballpbmaker.png?raw=true',
    '山口県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/yamaguchiballpbmaker.png?raw=true',
    '徳島県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tokushimaballpbmaker.png?raw=true',
    '香川県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kagawaballpbmaker.png?raw=true',
    '高知県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kochiballpbmaker.png?raw=true',
    '佐賀県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/sagaballpbmaker.png?raw=true',
    '長崎県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nagasakiballpbmaker.png?raw=true',
    '大分県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/oitaballpbmaker.png?raw=true',
    '宮崎県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/miyazakiballpbmaker.png?raw=true',
    '鹿児島県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kagoshimaprefballpbmaker.png?raw=true',
    '鹿児島県(シンボル)': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kagoshimaprefballpbmaker2.png?raw=true',
    '沖縄県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/okinawaballpbmaker.png?raw=true',
    '岡山県': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/okayamapbmaker.png?raw=true'
}

TOHTOKAN_CORE = {
    '宇都宮市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/utsunomiyaballpbmaker.png?raw=true',
    '函館市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/hakodateballpbmaker.png?raw=true',
    '金沢市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kanazawaballpbmaker.png?raw=true',
    '水戸市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/mitoballpbmaker.png?raw=true',
    '青森市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/aomoricityballpbmaker.png?raw=true',
    '八戸市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/hachinoheballpbmaker.png?raw=true',
    '盛岡市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/moriokaballpbmaker.png?raw=true',
    '秋田市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/akitacityballpbmaker.png?raw=true',
    '山形市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/yamagatacityballpbmaker.png?raw=true',
    'いわき市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/iwakiballpbmaker.png?raw=true',
    '郡山市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/koriyamaballpbmaker.png?raw=true',
    '福島市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/fukushimacityballpbmaker.png?raw=true',
    '前橋市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/maebashiballpbmaker.png?raw=true',
    '高崎市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/takasakiballpbmaker.png?raw=true',
    '柏市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kashiwaballpbmaker.png?raw=true',
    '横須賀市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/yokosukaballpbmaker.png?raw=true',
    '越谷市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/koshigayaballpbmaker.png?raw=true',
    '川越市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kawagoeballpbmaker.png?raw=true',
    '川口市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kawaguchiballpbmaker.png?raw=true',
    '旭川市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/asahikawaballpbmaker.png?raw=true',
    '船橋市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/funabashiballpbmaker.png?raw=true',
    '八王子市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/hachioujiballpbmaker.png?raw=true'
}

CHUTOKIN_CORE = {
    '姫路市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/himejicitypbmaker.png?raw=true',
    '金沢市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kanazawaballpbmaker.png?raw=true',
    '豊田市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/toyotapbmaker.png?raw=true',
    '岡崎市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/okazakiballpbmaker.png?raw=true',
    '豊橋市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/toyohashiballpbmaker.png?raw=true',
    '一宮市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ichinomiyaballpbmaker.png?raw=true',
    '福井市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/fukuicityballpbmaker.png?raw=true',
    '富山市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/toyamacityballpbmaker.png?raw=true',
    '長野市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/naganocitypbmaker.png?raw=true',
    '岐阜市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/gifucityballpbmaker.png?raw=true',
    '高槻市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/takatsukiballpbmaker.png?raw=true',
    '東大阪市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/higashiosakaballpbmaker.png?raw=true',
    '寝屋川市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/neyagawaballpbmaker.png?raw=true',
    '吹田市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/suitaballpbmaker.png?raw=true',
    '枚方市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/hirakataballpbmaker.png?raw=true',
    '八尾市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/yaoballpbmaker.png?raw=true',
    '豊中市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/toyonakaballpbmaker.png?raw=true',
    '西宮市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nishinomiyaballpbmaker.png?raw=true',
    '明石市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/akashiballpbmaker.png?raw=true',
    '大津市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/otsuballpbmaker.png?raw=true',
    '奈良市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/naracityballpbmaker.png?raw=true',
    '和歌山市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/wakaymacityballpbmaker.png?raw=true',
    '甲府市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kofuballpbmaker.png?raw=true',
    '松本市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/matsumotoballpbmaker.png?raw=true'
}


CHUTOKYU_CORE = {
    '呉市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kureballpbmaker.png?raw=true',
    '下関市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/shimonosekiballpbmaker.png?raw=true',
    '鳥取市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tottoricityballpbmaker.png?raw=true',
    '松江市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/matsueballpbmaker.png?raw=true',
    '高知市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kochicityballpbmaker.png?raw=true',
    '久留米市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kurumeballpbmaker.png?raw=true',
    '長崎市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nagasakicityballpbmaker.png?raw=true',
    '佐世保市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/saseboballpbmaker.png?raw=true',
    '宮崎市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/miyazakicityballpbmaker.png?raw=true',
    '那覇市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nahaballpbmaker.png?raw=true',
    '高松市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/takamatsuballpbmaker.png?raw=true',
    '倉敷市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kurashikiballpbmaker.png?raw=true',
    '福山市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/fukuyamaballpbmaker.png?raw=true',
    '鹿児島市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kagoshimaballpbmaker.png?raw=true',
    '大分市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/oitacitypbmaker.png?raw=true',
    '松山市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/matsuyamapbmaker.png?raw=true'
}

ORDINANCE_CITY = {
    '大阪市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/osakaballpbmaker.png?raw=true',
    '神戸市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kobepbmaker.png?raw=true',
    '京都市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kyotocitypbmaker.png?raw=true',
    '千葉市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/chibacitypbmaker.png?raw=true',
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

TERRITORIES = {
    'グリーンランド': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/greenlandballpbmaker.png?raw=true',
    '東トルキスタン': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/eastturkestanballpbmaker.png?raw=true',
    'チベット': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tibetballpbmaker.png?raw=true',
    '内モンゴル': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/innermongoliaballpbmaker.png?raw=true',
    'シーランド': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/sealandballpbmaker.png?raw=true',
}

ORGANIZATIONS = {
    'ヨーロッパ連合 (EU)': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/euballpbmaker.png?raw=true',
    '国際連合 (UN)': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/unballpbmaker.png?raw=true',
    'アフリカ連合 (AU)': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/auballpbmaker.png?raw=true',
    '国際連盟 (LoN)': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/lonballpbmaker.png?raw=true',
    '北大西洋条約機構 (NATO)': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/natoballpbmaker.png?raw=true',
    'ワルシャワ条約機構': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/warsawpactballpbmaker.png?raw=true',
}

TOKYO23WARDS = {
    '中央区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/chuouballpbmaker.png?raw=true',
    '千代田区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/chiyodaballpbmaker.png?raw=true',
    '港区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/minatoballpbmaker.png?raw=true',
    '新宿区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/shinjukuballpbmaker.png?raw=true',
    '渋谷区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/shibuyaballpbmaker.png?raw=true',
    '豊島区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/toyoshimaballpbmaker.png?raw=true',
    '江東区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kotoballpbmaker.png?raw=true',
    '品川区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/shinagawaballpbmaker.png?raw=true',
    '文京区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/bunkyoballpbmaker.png?raw=true',
    '台東区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/taitoballpbmaker.png?raw=true',
    '墨田区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/sumidaballpbmaker.png?raw=true',
    '目黒区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/meguroballpbmaker.png?raw=true',
    '大田区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/odaballpbmaker.png?raw=true',
    '世田谷区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/setagayaballpbmaker.png?raw=true',
    '中野区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nakanoballpbmaker.png?raw=true',
    '杉並区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/suginamiballpbmaker.png?raw=true',
    '北区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kitaballpbmaker.png?raw=true',
    '板橋区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/itabashiballpbmaker.png?raw=true',
    '足立区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/adachiballpbmaker.png?raw=true',
    '練馬区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nerimaballpbmaker.png?raw=true',
    '葛飾区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/katsushikaballpbmaker.png?raw=true',
    '荒川区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/arakawaballpbmaker.png?raw=true',
    '江戸川区': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/edogawaballpbmaker.png?raw=true'
}

OLDCOUNTRY = {
    'ソ連': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ussrballpbmaker.png?raw=true',
    'スペイン帝国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/spanishempireballpbmaker.png?raw=true',
    'ナ〇スドイツ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/germanreichballpbmaker.png?raw=true',
    'ローマ帝国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/romanempireballpbmaker.png?raw=true',
    'オスマン帝国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ottomanempireballpbmaker.png?raw=true',
    '大日本帝国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/japaneseempireballpbmaker.png?raw=true',
    '大韓帝国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/koreanempireballpbmaker.png?raw=true',
    'ロシア帝国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/russianempireballpbmaker.png?raw=true',
    '南ベトナム': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/southvietnamballpbmaker.png?raw=true',
    '清': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/qingballpbmaker.png?raw=true',
    '満州国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/manchuriaballpbmaker.png?raw=true',
    'ドイツ帝国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/germanempireballpbmaker.png?raw=true',
}

OTHERS = {
    'An Untitled Editor': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/aueballpbmaker.png?raw=true',
    '鳥取県信者ボール': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/believertottoripbmaker.png?raw=true',
    '鳥取県信者共栄圏': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tottorikyoueikenballpbmaker.png?raw=true',
    'きんら': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kinrapbmaker.png?raw=true',
    'きんら(旧)': 'https://raw.githubusercontent.com/RepublicofAuech/polandballmaker/main/flags/kinrapbmaker2.png?raw=true',
    'シンガポール(球状)': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/singaporeballpbmaker.png?raw=true',
    'カザフスタン(球状)': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/circlekazakhballpbmaker.png?raw=true',
    'らいる': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/rairuballpbmaker.png?raw=true',
    'なめこch': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/namekoballpbmaker.png?raw=true',
    '四国連邦': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/shikokurenpoballpbmaker.png?raw=true',
    'チャワストム共和国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/cawastomballpbmaker.png?raw=true',
    'アウイック共和国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/auechballpbmaker.png?raw=true',
    'フォノッサ共和国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/fonossaballpbmaker.png?raw=true',
    'アハネウ民主共和国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ahaneuballpbmaker.png?raw=true',
    'AHNU反地理系支部': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ahaneuantiballpbmaker.png?raw=true',
    'アドラフ民主主義共和国連邦': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/adorafuballpbmaker.png?raw=true',
    'ミネラル共和国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/mineralballpbmaker.png?raw=true',
    'サフォーニウ共和国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/safoniuballpbmaker.png?raw=true',
    'アレテーカ共和国': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/arretecaballpbmaker.png?raw=true',
    '吹奏楽部のイメージ旗': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/brassbandballpbmaker.png?raw=true',
}

SPECIAL_CITY = {
    '佐賀市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/sagacityballpbmaker.png?raw=true',
    '四日市市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/yokkaichiballpbmaker.png?raw=true',
    'つくば市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tsukubaballpbmaker.png?raw=true',
    '厚木市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/atsugiballpbmaker.png?raw=true',
    '長岡市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nagaokaballpbmaker.png?raw=true',
    '沼津市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/numazuballpbmaker.png?raw=true',
    '加古川市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kakogawaballpbmaker.png?raw=true',
    '茨木市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ibarakicityballpbmaker.png?raw=true',
    '伊勢崎市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/isezakiballpbmaker.png?raw=true',
    '太田市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/otaballpbmaker.png?raw=true',
    '小田原市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/odawaraballpbmaker.png?raw=true',
    '富士市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/fujiballpbmaker.png?raw=true',
    '春日部市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kasukabeballpbmaker.png?raw=true',
    '草加市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kusakaballpbmaker.png?raw=true',
    '春日井市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kasugaiballpbmaker.png?raw=true',
    '茅ヶ崎市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/chigasakiballpbmaker.png?raw=true',
    '岸和田市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kishiwadaballpbmaker.png?raw=true',
    '平塚市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/hiratsukaballpbmaker.png?raw=true',
    '上越市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/joetsuballpbmaker.png?raw=true',
    '宝塚市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/takarazukaballpbmaker.png?raw=true',
    '大和市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/yamatoballpbmaker.png?raw=true',
    '熊谷市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kumagawaballpbmaker.png?raw=true',
    '所沢市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tokorozawaballpbmaker.png?raw=true',
    '宝塚市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/takarazukaballpbmaker.png?raw=true',
}

OTHER_CITY_TOHTOKAN = {
    '松戸市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/matsudoballpbmaker.png?raw=true',
    '市川市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ichikawaballpbmaker.png?raw=true',
    '藤沢市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/fujisawaballpbmaker.png?raw=true',
    '鶴岡市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tsuruokaballpbmaker.png?raw=true',
    '館林市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/datebayashiballpbmaker.png?raw=true',
}

OTHER_CITY_CHUTOKIN = {
    '長浜市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/nagahamaballpbmaker.png?raw=true',
    '東海市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tokaiballpbmaker.png?raw=true',
    '津市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tsuballpbmaker.png?raw=true',
    '橿原市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/kashiwaraballpbmaker.png?raw=true',
    '安城市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/anjoballpbmaker.png?raw=true',
    '伊勢市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/iseballpbmaker.png?raw=true',
    '宇治市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/ujiballpbmaker.png?raw=true',
}

OTHER_CITY_CHUTOKYU = {
    '徳島市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/tokushimacityballpbmaker.png?raw=true',
    '山口市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/yamaguchicityballpbmaker.png?raw=true',
    '今治市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/imabariballpbmaker.png?raw=true',
    '米子市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/yonagoballpbmaker.png?raw=true',
    '唐津市': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/karatsuballpbmaker.png?raw=true',
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
    'びっくり': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/scaredeyes.png?raw=true',
    'ぐっすり': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/closedeyes.png?raw=true',
    'かわいい': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/cuteeyes.png?raw=true',
    'ほっとしてる': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/relievedeyes.png?raw=true',
    '疑問（左目ver）': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/confusedeyes1.png?raw=true',
    '疑問（右目ver）': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/confusedeyes2.png?raw=true',
    '左目ウインク': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/winkeyes1.png?raw=true',
    '右目ウインク': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/winkeyes2.png?raw=true',
    'じーっと見てる': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/staringeyes.png?raw=true',
    'ﾁｰﾝ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/deadeyes.png?raw=true',
    '細目': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/thineyes.png?raw=true',
    '退屈': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/boredeyes.png?raw=true',
    'イライラ': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/eyes/frustratedeyes.png?raw=true',
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

SHADOW_ONOFF = {
    'あり': 'https://github.com/RepublicofAuech/polandballmaker/blob/main/flags/shadowpbmaker.png?raw=true',
    'なし': None
}    

CATEGORY_FLAGS = {
    '西・南ヨーロッパの国々': WSEUROPE_COUNTRY,
    '東・北ヨーロッパの国々': ENEUROPE_COUNTRY,
    '東・東南アジアの国々': ESEASIA_COUNTRY,
    '西アジアの国々': WASIA_COUNTRY,
    '中央・南アジアの国々': CSASIA_COUNTRY,
    '北中米の国々': NCAMERICA_COUNTRY,
    'カリブ海の国々': CARIBBEAN_COUNTRY,
    '南米の国々': SAMERICA_COUNTRY,
    '北・西アフリカの国々': NWAFRICA_COUNTRY,
    '中央・南アフリカの国々': CSAFRICA_COUNTRY,
    '東アフリカの国々': EAFRICA_COUNTRY,
    'オセアニアの国々': OCEANIA_COUNTRY,
    '都道府県（東北から中部）': TOHTOCHU_PREF,
    '都道府県（近畿から九州）': KINTOKYU_PREF,
    '政令市': ORDINANCE_CITY,
    '中核市（東北から関東）': TOHTOKAN_CORE,
    '中核市（中部から近畿）': CHUTOKIN_CORE,
    '中核市（中国から九州）': CHUTOKYU_CORE,
    '海外領土・自治領、未承認国家': TERRITORIES,
    '組織': ORGANIZATIONS,
    '東京23区': TOKYO23WARDS,
    '特例市': SPECIAL_CITY,
    'その他の都市（東北から関東）': OTHER_CITY_TOHTOKAN,
    'その他の都市（中部から近畿）': OTHER_CITY_CHUTOKIN,
    'その他の都市（中国から九州）': OTHER_CITY_CHUTOKYU,
    '昔あった国': OLDCOUNTRY,
    'その他': OTHERS,
    'なし': NONE
}

WORLD_CHOICES = [
    app_commands.Choice(name='西・南ヨーロッパの国々', value='西・南ヨーロッパの国々'),
    app_commands.Choice(name='東・北ヨーロッパの国々', value='東・北ヨーロッパの国々'),
    app_commands.Choice(name='西アジアの国々', value='西アジアの国々'),
    app_commands.Choice(name='東・東南アジアの国々', value='東・東南アジアの国々'),
    app_commands.Choice(name='中央・南アジアの国々', value='中央・南アジアの国々'),
    app_commands.Choice(name='北中米の国々', value='北中米の国々'),
    app_commands.Choice(name='カリブ海の国々', value='カリブ海の国々'),
    app_commands.Choice(name='南米の国々', value='南米の国々'),
    app_commands.Choice(name='北・西アフリカの国々', value='北・西アフリカの国々'),
    app_commands.Choice(name='中央・南アフリカの国々', value='中央・南アフリカの国々'),
    app_commands.Choice(name='東アフリカの国々', value='東アフリカの国々'),
    app_commands.Choice(name='オセアニアの国々', value='オセアニアの国々'),
    app_commands.Choice(name='海外領土・自治領、未承認国家', value='海外領土・自治領、未承認国家'),
    app_commands.Choice(name='組織', value='組織'),
    app_commands.Choice(name='昔あった国', value='昔あった国'),
    app_commands.Choice(name='その他', value='その他'),
    app_commands.Choice(name='なし', value='なし')
]

JAPAN_CHOICES = [
    app_commands.Choice(name='都道府県（東北から中部）', value='都道府県（東北から中部）'),
    app_commands.Choice(name='都道府県（近畿から九州）', value='都道府県（近畿から九州）'),
    app_commands.Choice(name='政令市', value='政令市'),
    app_commands.Choice(name='東京23区', value='東京23区'),
    app_commands.Choice(name='中核市（東北から関東）', value='中核市（東北から関東）'),
    app_commands.Choice(name='中核市（中部から近畿）', value='中核市（中部から近畿）'),
    app_commands.Choice(name='中核市（中国から九州）', value='中核市（中国から九州）'),
    app_commands.Choice(name='特例市', value='特例市'),
    app_commands.Choice(name='その他の都市（東北から関東）', value='その他の都市（東北から関東）'),
    app_commands.Choice(name='その他の都市（中部から近畿）', value='その他の都市（中部から近畿）'),
    app_commands.Choice(name='その他の都市（中国から九州）', value='その他の都市（中国から九州）'),
    app_commands.Choice(name='なし', value='なし')
]

OTHER_CHOICES = [
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
    app_commands.Choice(name='びっくり', value='びっくり'),
    app_commands.Choice(name='ぐっすり', value='ぐっすり'),
    app_commands.Choice(name='かわいい', value='かわいい'),
    app_commands.Choice(name='ほっとしてる', value='ほっとしてる'),
    app_commands.Choice(name='疑問（左目ver）', value='疑問（左目ver）'),
    app_commands.Choice(name='疑問（右目ver）', value='疑問（右目ver）'),
    app_commands.Choice(name='左目ウインク', value='左目ウインク'),
    app_commands.Choice(name='右目ウインク', value='右目ウインク'),
    app_commands.Choice(name='じーっと見てる', value='じーっと見てる'),
    app_commands.Choice(name='ﾁｰﾝ', value='ﾁｰﾝ'),
    app_commands.Choice(name='イライラ', value='イライラ'),
    app_commands.Choice(name='細目', value='細目'),
    app_commands.Choice(name='退屈', value='退屈'),
    app_commands.Choice(name='なし', value='なし')
]

SHADOW_CHOICES = [
    app_commands.Choice(name='あり', value='あり'),
    app_commands.Choice(name='なし', value='なし')
]

POSITION_CHOICES = [app_commands.Choice(
    name=pos, value=pos) for pos in POSITION_COMMANDS.keys()]

async def get_country_choices(interaction: discord.Interaction, current: str):
    category = interaction.namespace.category
    flags = CATEGORY_FLAGS.get(category, {})
    return [app_commands.Choice(name=name, value=name) for name in flags.keys() if current.lower() in name.lower()]

# Function to download an image from a URL


async def fetch_image(url):
    if not isinstance(url, str) or not url:  # Check if URL is a valid string
        print(f"Invalid URL provided: {url}")
        return None
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
def merge_images(shadow_img, flag_img, expression_img, position):
        
    if expression_img is None:
        print("No expression image provided.")
        return flag_img

    # Convert expression_img to RGBA if not already
    if expression_img.mode != 'RGBA':
        expression_img = expression_img.convert('RGBA')

    # Resize the expression image to 100% of the flag's size
    expression_img = expression_img.resize(
        (flag_img.width, flag_img.height), Image.LANCZOS)

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
    if shadow_img:
        combined_img.paste(shadow_img, (0, 0), shadow_img)
    combined_img.paste(expression_img, (x, y), expression_img)

    return combined_img

# Command to create the Polandball image


@bot.tree.command(name='pbmaker_japan', description='日本の都市などのポーランドボールを作成します')
@app_commands.describe(
    shadow='影の有無を選択してください',
    category='柄のカテゴリーを選んでください',
    country='国、都道府県または市区町村を選んでください',
    expression='ボールの表情を選んでください',
    position='目の位置を選んでください'
)
@app_commands.choices(shadow=SHADOW_CHOICES, category=JAPAN_CHOICES, expression=EXPRESSION_CHOICES, position=POSITION_CHOICES)
@app_commands.autocomplete(country=get_country_choices)
async def pb_maker(interaction: discord.Interaction,
                   shadow: app_commands.Choice[str],
                   category: app_commands.Choice[str],
                   country: str,
                   expression: app_commands.Choice[str],
                   position: app_commands.Choice[str]):

    await interaction.response.defer()

    # Correctly fetch the URL or None based on the shadow selection
    shadow_url = SHADOW_ONOFF.get(shadow.value)
    print(f"Fetched shadow URL: {shadow_url}")  # Debugging output to check the correct URL

    flag_url = CATEGORY_FLAGS[category.value].get(country)
    if not flag_url:
        await interaction.followup.send("指定された国や地域の旗画像が見つかりませんでした", ephemeral=True)
        return

    # Fetch the expression image URL or set to None if expression is 'なし'
    expression_url = EXPRESSION_IMAGES.get(expression.value, None)
    
    # Fetch the images
    shadow_img = await fetch_image(shadow_url) if shadow_url else None  # Fetch shadow image only if URL is valid
    flag_img = await fetch_image(flag_url)
    expression_img = await fetch_image(expression_url) if expression_url else None
    
    if not flag_img:
        await interaction.followup.send("旗の画像を取得できませんでした。再試行してください", ephemeral=True)
        return

    # Merge images based on position
    try:
        combined_img = merge_images(shadow_img, flag_img, expression_img, position.value)
    except Exception as e:
        await interaction.followup.send(f"画像の合成中にエラーが発生しました: {e}", ephemeral=True)
        return

    # Save and send the image
    with io.BytesIO() as output:
        combined_img.save(output, format='PNG')
        output.seek(0)
        file = discord.File(output, filename='polandball.png')
        await interaction.followup.send(file=file)
        
@bot.tree.command(name='pbmaker_world', description='世界の国、組織などのポーランドボールを作成します')
@app_commands.describe(
    shadow='影の有無を選択してください',
    category='柄のカテゴリーを選んでください',
    country='国、都道府県または市区町村を選んでください',
    expression='ボールの表情を選んでください',
    position='目の位置を選んでください'
)
@app_commands.choices(shadow=SHADOW_CHOICES, category=WORLD_CHOICES, expression=EXPRESSION_CHOICES, position=POSITION_CHOICES)
@app_commands.autocomplete(country=get_country_choices)
async def pb_maker(interaction: discord.Interaction,
                   shadow: app_commands.Choice[str],
                   category: app_commands.Choice[str],
                   country: str,
                   expression: app_commands.Choice[str],
                   position: app_commands.Choice[str]):

    await interaction.response.defer()

    # Correctly fetch the URL or None based on the shadow selection
    shadow_url = SHADOW_ONOFF.get(shadow.value)
    print(f"Fetched shadow URL: {shadow_url}")  # Debugging output to check the correct URL

    flag_url = CATEGORY_FLAGS[category.value].get(country)
    if not flag_url:
        await interaction.followup.send("指定された国や地域の旗画像が見つかりませんでした", ephemeral=True)
        return

    # Fetch the expression image URL or set to None if expression is 'なし'
    expression_url = EXPRESSION_IMAGES.get(expression.value, None)
    
    # Fetch the images
    shadow_img = await fetch_image(shadow_url) if shadow_url else None  # Fetch shadow image only if URL is valid
    flag_img = await fetch_image(flag_url)
    expression_img = await fetch_image(expression_url) if expression_url else None
    
    if not flag_img:
        await interaction.response.send_message("旗の画像を取得できませんでした。再試行してください", ephemeral=True)
        return

    # Merge images based on position
    try:
        combined_img = merge_images(shadow_img, flag_img, expression_img, position.value)
    except Exception as e:
        await interaction.followup.send(f"画像の合成中にエラーが発生しました: {e}", ephemeral=True)
        return

    # Save and send the image
    with io.BytesIO() as output:
        combined_img.save(output, format='PNG')
        output.seek(0)
        file = discord.File(output, filename='polandball.png')
        await interaction.followup.send(file=file)
        
@bot.tree.command(name='pbmaker_other', description='世界または日本とは関係ないポーランドボールを作成します')
@app_commands.describe(
    shadow='影の有無を選択してください',
    category='柄のカテゴリーを選んでください',
    country='国、都道府県または市区町村を選んでください',
    expression='ボールの表情を選んでください',
    position='目の位置を選んでください'
)
@app_commands.choices(shadow=SHADOW_CHOICES, category=OTHER_CHOICES, expression=EXPRESSION_CHOICES, position=POSITION_CHOICES)
@app_commands.autocomplete(country=get_country_choices)
async def pb_maker(interaction: discord.Interaction,
                   shadow: app_commands.Choice[str],
                   category: app_commands.Choice[str],
                   country: str,
                   expression: app_commands.Choice[str],
                   position: app_commands.Choice[str]):

    await interaction.response.defer()

    # Correctly fetch the URL or None based on the shadow selection
    shadow_url = SHADOW_ONOFF.get(shadow.value)
    print(f"Fetched shadow URL: {shadow_url}")  # Debugging output to check the correct URL

    flag_url = CATEGORY_FLAGS[category.value].get(country)
    if not flag_url:
        await interaction.followup.send("指定された国や地域の旗画像が見つかりませんでした", ephemeral=True)
        return

    # Fetch the expression image URL or set to None if expression is 'なし'
    expression_url = EXPRESSION_IMAGES.get(expression.value, None)
    
    # Fetch the images
    shadow_img = await fetch_image(shadow_url) if shadow_url else None  # Fetch shadow image only if URL is valid
    flag_img = await fetch_image(flag_url)
    expression_img = await fetch_image(expression_url) if expression_url else None
    
    if not flag_img:
        await interaction.followup.send("旗の画像を取得できませんでした。再試行してください", ephemeral=True)
        return

    # Merge images based on position
    try:
        combined_img = merge_images(shadow_img, flag_img, expression_img, position.value)
    except Exception as e:
        await interaction.followup.send(f"画像の合成中にエラーが発生しました: {e}", ephemeral=True)
        return

    # Save and send the image
    with io.BytesIO() as output:
        combined_img.save(output, format='PNG')
        output.seek(0)
        file = discord.File(output, filename='polandball.png')
        await interaction.followup.send(file=file)
        
load_dotenv()
bot.run(os.getenv("TOKEN"))
