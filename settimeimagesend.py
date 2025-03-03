import os
import time
import schedule
from wxauto import WeChat
import argparse

# 定义发送图片的函数

def send_image():
    # 初始化微信
    global image_path,contact_name
    wx = WeChat()

    # 打开微信


    # 指定好友昵称


    # 跳转到指定好友的聊天窗口
    wx.ChatWith(contact_name)



    # 检查图片是否存在
    if os.path.exists(image_path):
        wx.SendFiles(image_path)
        print(f"图片已发送给 {contact_name}")
    else:
        print(f"图片路径无效：{image_path}")


# 定义定时任务


if __name__ == '__main__':
      # 每天上午10:00发送图片

    args = argparse.ArgumentParser()
    args.add_argument('--image_path','-i', type=str, default='./p2906950533.jpg', help='图片路径')
    args.add_argument('--name','-n', type=str, default='一爹四儿', help='微信联系人昵称')
    args.add_argument('--time', '-t', type=str, default='23:00:00', help='时间')
    args.add_argument('--every', '-e', type=str, default='day', help='时间间隔',choices=['day','hour','minute'])
    args.add_argument('--gap', '-g', type=int, default='day', help='时间间隔' )
    args = args.parse_args()
    if args.image_path:
        image_path = args.image_path
    if args.name:
        contact_name = args.name
    if  args.every=='day':
        schedule.every().day.at(args.time).do(send_image)
    elif args.every=='hour':
        schedule.every(args.gap).hour.do(send_image)
    elif args.every == 'minute':
        schedule.every(args.gap).minutes.do(send_image)
    while True:

            schedule.run_pending()
            time.sleep(5)
