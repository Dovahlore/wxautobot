from openai import OpenAI
import time
import argparse
from collections import deque
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="**",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

from wxauto import WeChat
chat_history ={}

def process_new_message():
    # 读取最新一条微信消息
    global chat_history
    msgs = wx.GetListenMessage()


    for chat, msgs in msgs.items():
        chat = chat.who

        if chat not in chat_message.keys():
            chat_message[chat] = [{"role": 'user',
                                   "content": "你是一个我的的微信自动回复机器，为我自动回复消息."}]
        has_new_message = False
        for msg in msgs:

            # 获取聊天会话框的消息

            if msg[0] == "Self":
                chat_message[chat].append({"role": 'assistant', "content": "我/自动回复机器人的发言：" + msg[1]})
                chat_history[chat].append("我/自动回复机器人的发言：" + msg[1])

            elif msg[0] in ["SYS", "Super"]:
                continue
            else:
                chat_history[chat].append("好友%s的发言：" % msg[0] + msg[1])

                has_new_message = True

        if  has_new_message:
            prompt = f"""请使用下方过往聊天群中的对话记录（<<<context>>><<</context>>>之间的部分）来模仿我进行聊天回复，请根据自己的理解进行回答，回答一定是不能有想机器人客服的感觉。
                聊天记录是按照时间顺序排列的,最新的消息在最后面。最好以最新消息来进行回复，可以对带有一些攻击性（指的是开玩笑的攻击）。
                还有每句话前最好加一个“说白了。”这是我的口头禅。
                        <<<context>>>  
                        {list(chat_history[chat])}  
                        <<</context>>>  
                        请直接回复聊天，不要以"我/自动回复机器人的发言："开头：  
                        """
            chat_message[chat].append({"role": 'user', "content": prompt})
            # 调用 OpenAI 生成回复

            res = client.chat.completions.create(model="deepseek-r1", messages=chat_message[chat])

            response = res.choices[0].message.content
            # Extract the model's response
            print("Model's response:", response)

            wx.SendMsg(who=chat, msg=response)


# 循环监听微信消息
if __name__ == "__main__":
    wx = WeChat()
    args = argparse.ArgumentParser()
    args.add_argument('--listen',"-l",  nargs='+' )
    args=args.parse_args()
    Listen = args.listen
    print(type(Listen))
    if not Listen:
        print("请指定需要监听的微信群，例如：python autobot.py -l 群1 群2 群3")
        exit()
    for i in Listen:
        print(i)
        chat_history[i] = deque(maxlen=20)
        wx.AddListenChat(who=i)

    print("正在监听微信消息...")
    chat_message = {}

    while True:
        process_new_message()
        time.sleep(30)
