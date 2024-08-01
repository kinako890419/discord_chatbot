"""
注意事項
1. @bot.event 要改成 @commands.Cog.listener()
2. @bot.command() 要改成 @commands.command()
3. 原指令用 bot 在 Cog 寫法下，都要變成 self.bot
4. 每個指令的第一個參數要是 self
"""

import os
from dotenv import load_dotenv, find_dotenv
import random

import google.generativeai as genai

import discord
from discord.ext import commands

from random_tarot import get_random_tarot_info

load_dotenv(find_dotenv())
# CHANNEL_ID = os.getenv("CHANNEL_ID")
GOOGLE_API_KEY = os.getenv("GEMINI_API_TOKEN")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # intents = discord.Intents.default()
    # intents.message_content = True

    # bot = commands.Bot(command_prefix='!', intents=intents)

    @commands.Cog.listener()
    async def on_ready(self):
        game = discord.Game('潑你熱水')
        # discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
        await self.bot.change_presence(status=discord.Status.online, activity=game)

        # # automatic send a message when the bot is online
        # channel = self.bot.get_channel(CHANNEL_ID)
        # await channel.send("原神 啟動！")
        #
        # print(f'Logged in as {self.bot.user.name}')

    @commands.command()
    async def question(self, ctx, *, question):
        try:

            card_result, card_name, card_info = get_random_tarot_info()
            # context = "我不想寫論文"

            tarot_reply = (f"你是一個占卜師，在進行塔羅占卜。接下來的對話我會提出我的問題，以下是我抽到的三張牌。"
                           f"解釋牌面的意義後，利用繁體中文根據我的問題給出解答，最後再做出總結與建議。"
                           f"請注意你的答覆越完整與全面越好，但是要限縮在800字以內，務必考慮卡片正逆位的差異。"
                           f"我抽到的牌是：{card_info}"
                           f"以下是我的疑問，請用繁體中文回答：{question}")

            response = model.generate_content(tarot_reply)

            # card_result, card_name, card_info = get_random_tarot_info()
            # # print(card_result)
            # formatted_prompt = prompt.format(card_info=card_info, context=question)
            #
            # result = model.generate_content(formatted_prompt)

            # # 去掉提示模板部分，只保留生成的回應
            # result = result[len(formatted_prompt):].strip()

            ans = f"### 你抽到的牌是：{card_result[0]}、{card_result[1]}、{card_result[2]}\n{response.text}"

            # 如果結果超過2000字元，進行分段處理
            if len(ans) > 2000:
                parts = [ans[i:i + 2000] for i in range(0, len(ans), 2000)]
                for part in parts:
                    await ctx.send(part)
            else:
                # await ctx.send(card_result)
                await ctx.send(ans)

        except Exception as e:
            print(f"Error occurred: {e}")
            await ctx.send("你給我去跟神父告解")

    @commands.command()
    async def chat(self, ctx, *, chat):
        try:
            # formatted_prompt = chat_prompt.format(context=chat)

            reply = (f"你是一個稱職的聊天機器人，你的對話內容會依據對象的心情改變。"
                     f"如果今天的話題是一個很沉重的話題，請適當的鼓勵。如果今天的話題輕鬆愉快，你可以試著開玩笑。"
                     f"注意，請使用繁體中文，謝謝。"
                     f"我想說的是：{chat}")

            result = model.generate_content(reply)

            ans = result.text

            # 如果結果超過2000字元，進行分段處理
            if len(ans) > 2000:
                parts = [ans[i:i + 2000] for i in range(0, len(ans), 2000)]
                for part in parts:
                    await ctx.send(part)
            else:
                await ctx.send(ans)

        except Exception as e:
            print(f"Error occurred: {e}")
            await ctx.send("你給我去跟神父告解")

    @commands.command()
    async def complain(self, ctx, *, bad):

        # Return a random bad advice
        def get_bad_advice():
            bad_advices = ["說不定他其實很討厭你", "你不能自己處理一下嗎？",
                           "這有什麼好難過的？", "多喝熱水。"]
            bad_ans = random.choice(bad_advices)
            return bad_ans

        try:
            choice = get_bad_advice()
            bad_advice_prompt_template = \
                (f"你是一個沒什麼同理心的男朋友，今天你的女朋友在跟你訴苦，"
                 f"你的女朋友抱怨是：{bad}"
                 f"你要用這個開頭來回覆他一句話：{choice}"
                 f"產生一句話，盡量讓他覺得你很不在乎，或者是你很不想聽他說話。")

            result = model.generate_content(bad_advice_prompt_template)

            ans = result.text

            # 如果結果超過2000字元，進行分段處理
            if len(ans) > 2000:
                parts = [ans[i:i + 2000] for i in range(0, len(ans), 2000)]
                for part in parts:
                    await ctx.send(part)
            else:
                # print(choice)
                await ctx.send(ans)

        except Exception as e:
            print(f"Error occurred: {e}")
            await ctx.send("你給我去跟神父告解")

    @commands.command()
    async def why(self, ctx, *, why_question):
        try:
            why_generate_prompt_template = f"用繁體中文回答我所有的問題。\
            我的問題是：{why_question}\
            你必須用這個格式回答，其中的<問題>填入的是與我的問題相關的主旨，<名詞>是與問題相關的主詞。\
            注意：<問題>一定要是四個字，<名詞>一定要是兩個字。\
            回答格式如下：\
            為什麼你不能<我的問題>\
            是因為\
            你在<問題>上面\
            你在<問題>上面\
            你在<問題>上面\
            你跟<名詞>唱反調：）\
            \
            以下是範例：\
            我的問題是：我為什麼不能加薪？\
            範例回答如下：\
            為什麼你不能加薪\
            是因為\
            你在薪水問題上面\
            你在老闆情緒上面\
            你在工作處理上面\
            你跟公司唱反調：）\
            \
            注意，請回傳你的回覆就好。\
            "

            result = model.generate_content(why_generate_prompt_template)

            ans = result.text

            # 如果結果超過2000字元，進行分段處理
            if len(ans) > 2000:
                parts = [ans[i:i + 2000] for i in range(0, len(ans), 2000)]
                for part in parts:
                    await ctx.send(part)
            else:
                await ctx.send(ans)

        except Exception as e:
            print(f"Error occurred: {e}")
            await ctx.send("你給我去跟神父告解")

    # message listener
    @commands.Cog.listener()
    async def on_message(self, msg):
        # 防止機器人自己觸發
        if msg.author == self.bot.user:
            return
        if msg.content == "謝謝" or msg.content == "謝囉" or msg.content == "謝謝你"\
                or msg.content == "......" or msg.content == "幹":
            await msg.channel.send("不客氣")

    @commands.command()
    # type !tutorial to return tutorial message
    async def tutorial(self, ctx):
        try:
            mes = f"""
## 指令教學
1. 使用 !question <問題> 進行塔羅占卜
2. 使用 !chat <對話> 聊天
3. 使用 !complain <抱怨> 抱怨，AI可能會兇你
4. 使用 !why <問題> 進行問答

## 注意事項
使用頻率不要太高，不然我不知道哪天google (跟 AWS?) 會不會跟我收費
            """
            await ctx.send(mes)

        except Exception as e:
            print(f"Error occurred: {e}")
            await ctx.send("為什麼連這個都會報錯...可能網路問題吧")

    # bot.run(os.environ.get("DISCORD_TOKEN"))


async def setup(bot):
    await bot.add_cog(Main(bot))

# if __name__ == "__main__":
#     # print(card_info)
#
#     pass
