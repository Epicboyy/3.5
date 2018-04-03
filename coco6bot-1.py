# -*- coding: utf-8 -*-
from linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse,timeit,data,atexit
from gtts import gTTS
from googletrans import Translator
botStart = time.time()
cl = LINE()
cl.log("Auth Token : " + str(cl.authToken))
channelToken = cl.getChannelResult()
cl.log("Channel Token : " + str(channelToken))
oepoll = OEPoll(cl)
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")
read = json.load(readOpen)
settings = json.load(settingsOpen)
myProfile = {
    "displayName": "",
    "statusMessage": "",
    "pictureStatus": ""
}
mid1 = 'ua4daf7f920d84266ddcfcac7faeab2ee' #總機
mid2 = 'u10e75d856b816c4e06ef4dfbf312dd5c' #群組機
mid3 = 'u54b2b72da19554aef5be810ada3e2092' #已讀機
mid4 = 'ua3eb62abc27454418e37a353c0518c3a' #查詢機
mid5 = 'ub0a37c52cd0726e467cbcff8974d0644' #踢人機
mid6 = 'uf80461d783a7cc1c02f83f50b88764a0' #特化機
lineSettings = cl.getSettings()
clProfile = cl.getProfile()
clMID = cl.profile.mid
myProfile["displayName"] = clProfile.displayName
myProfile["statusMessage"] = clProfile.statusMessage
myProfile["pictureStatus"] = clProfile.pictureStatus
admin = ['u28d781fa3ba9783fd5144390352b0c24', clMID, mid1, mid2, mid3, mid4, mid5, mid6]
wait2 = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
}
setTime = {}
setTime = wait2['setTime']
cctv={
    "cyduk":{},
    "point":{},
    "sidermem":{}
}
msg_dict = {}
bl = [""]
def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))
def restartBot():
    print ("[ 訊息 ] 機器 重新啟動")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)
def logError(text):
    cl.log("[ 錯誤 ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
def helpmessage():
    helpMessage = """
╔═══✪〘 查看指令表 〙✪════
↪ 「Help」查看指令列表
↪ 「Help Tag」查看標註指令
↪ 「Help Bot」查看機器指令
↪ 「Help Info」查看狀態指令
↪ 「Help Self」查看自己指令
↪ 「Help Kick」查看踢人指令
↪ 「Help Group」查看群組指令
↪ 「Help Special」查看特殊指令
╚═〘 Credits By: ©CoCo™  〙
"""
    return helpMessage
def helpmessageinfo():
    helpMessageInfo = """
╔═══✪〘 狀態 〙✪═══════
↪ 「Rebot」重新啟動機器
↪ 「Runtime」查看機器運行時間
↪ 「Speed」查看機器速度
↪ 「Set」查看設定
↪ 「About」查看自己的狀態
↪ 「Protect Info」查看這個群組的保護狀態
↪ 「Protectlist」查看保護中的群組
╚═〘 Credits By: ©CoCo™  〙
"""
    return helpmessageinfo
def helpmessagebot():
    helpMessageBot = """
╔═══✪〘 設定 〙✪═══════
↪ 「Add On/Off」自動加入好友 打開/關閉
↪ 「Join On/Off」邀請自動進入群組 打開/關閉
↪ 「Leave On/Off」自動離開副本 打開/關閉
↪ 「Read On/Off」自動已讀 打開/關閉
↪ 「Tag On/Off」標註提醒 打開/關閉
↪ 「Inviteprotect On/Off」邀請保護 打開/關閉
↪ 「Reread On/Off」查看收回 打開/關閉
╚═〘 Credits By: ©CoCo™  〙
"""
    return helpmessagebot
def helpmessageself():
    helpMessageSelf = """
╔═══✪〘 自己 〙✪═══════
↪ 「Me」丟出自己好友資料
↪ 「MyMid」查看自己系統識別碼
↪ 「MyName」查看自己名字
↪ 「MyBio」查看自己個簽
↪ 「MyPicture」查看自己頭貼網址
↪ 「MyCover」查看自己封面網址
↪ 「Contact @」標註查看好友資料
↪ 「Mid @」標註查看系統識別碼
↪ 「Picture @」標註查看頭貼
↪ 「Cover @」標注查看封面
╚═〘 Credits By: ©CoCo™  〙
"""
    return helpmessageself
def helpmessagegroup():
    helpMessageGroup = """
╔═══✪〘 群組 〙✪═══════
↪ 「Gowner」查看群組擁有者
↪ 「Gid」查看群組識別碼
↪ 「Gname」查看群組名稱
↪ 「Gurl」丟出群組網址
↪ 「O/Curl」打開/關閉群組網址
↪ 「Ginfo」查看群組狀態
↪ 「Ri @」標註來回機票
↪ 「Tk @」標注踢出成員
↪ 「Vk @」標註踢出並清除訊息
↪ 「NT Name」使用名子標註成員
↪ 「Zt」標註名字0字成員
↪ 「Zm」丟出0字成員的系統識別碼
↪ 「Zc」丟出0字成員好友資料
↪ 「Cancel」取消所有成員邀請
↪ 「Gcancel」取消所有群組邀請
↪ 「Gn Name」更改群組名稱
↪ 「Gc @」標註查看個人資料
↪ 「Inv mid」使用系統識別碼邀請進入群組
↪ 「Ban @」標註加入黑單
↪ 「Unban @」標註解除黑單
↪ 「Clear Ban」清空黑單
↪ 「Kill Ban」剔除黑單
╚═〘 Credits By: ©CoCo™  〙
"""
    return helpmessagegroup
def helpmessagespecial():
    helpMessageSpecial = """
╔═══✪〘 特殊 〙✪═══════
↪ 「Tagall」標註群組所有成員
↪ 「S N/F」已讀點 開啟/關閉
↪ 「Ar」重置全部已讀點
↪ 「R」查看已讀
↪ 「F/Gbc」好友/群組廣播
↪ 「/invitemeto:」使用群組識別碼邀請至群組
↪ 「Time」查看現在的時間
↪ 「Sc gid」使用群組識別碼查看群組狀態
↪ 「Mc mid」使用系統識別碼查看好友資料
╚═〘 Credits By: ©CoCo™  〙
"""
    return helpmessagespecial
def helpmessagekick():
    helpMessageKick = """
╔═══✪〘 踢人 〙✪═══════
↪ 「Ri @」標註來回機票
↪ 「Tk @」標注踢出成員
↪ 「Vk @」標註踢出並清除訊息
↪ 「NT Name」使用名子標註成員
↪ 「Kill Ban」剔除黑單
╚═〘 Credits By: ©CoCo™  〙
"""
    return helpmessagekick
def helpmessagetag():
    helpMessageTag = """
╔═══✪〘 標註 〙✪═══════
↪ 「Ri @」標註來回機票
↪ 「Tk @」標注踢出成員
↪ 「Vk @」標註踢出並清除訊息
↪ 「Ban @」標註加入黑單
↪ 「Unban @」標註解除黑單
↪ 「Gc @」標註查看個人資料
↪ 「Contact @」標註查看好友資料
↪ 「Mid @」標註查看系統識別碼
↪ 「Picture @」標註查看頭貼
↪ 「VideoProfile @」標註查看動態頭貼
↪ 「Cover @」標注查看封面
╚═〘 Credits By: ©CoCo™  〙
"""
    return helpmessagetag

def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            contact = cl.getContact(param2)
            print ("[ 5 ] 通知添加好友 名字: " + contact.displayName)
            if settings["autoAdd"] == True:
                cl.sendMessage(op.param1, "你好 {} 謝謝你加本機為好友 :D\n       本機為CoCo製作\n       line.me/ti/p/1MRX_Gjbmv".format(str(cl.getContact(op.param1).displayName)))
        if op.type == 11:
            group = cl.getGroup(op.param1)
            contact = cl.getContact(op.param2)
            print ("[11]有人打開群組網址 群組名稱: " + str(group.name) + "\n" + op.param1 + "\n名字: " + contact.displayName)
            if op.param1 in settings["qrprotect"]:
                if op.param2 in admin:
                    pass
                else:
                    gs = cl.getGroup(op.param1)
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    gs.preventJoinByTicket = True
                    cl.updateGroup(gs)
        if op.type == 13:
            contact1 = cl.getContact(op.param2)
            contact2 = cl.getContact(op.param3)
            group = cl.getGroup(op.param1)
            print ("[ 13 ] 通知邀請群組: " + str(group.name) + "\n邀請者: " + contact1.displayName + "\n被邀請者" + contact2.displayName)
            if op.param1 in settings["inviteprotect"]:
                if op.param2 in admin:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param3)
            if clMID in op.param3:
                if settings["autoJoin"] == True:
                    print ("進入群組: " + str(group.name))
                    cl.acceptGroupInvitation(op.param1)
        if op.type == 19:
            contact1 = cl.getContact(op.param2)
            group = cl.getGroup(op.param1)
            contact2 = cl.getContact(op.param3)
            print ("[19]有人把人踢出群組 群組名稱: " + str(group.name) + "\n" + op.param1 +"\n踢人者: " + contact1.displayName + "\nMid: " + contact1.mid + "\n被踢者" + contact2.displayName + "\nMid:" + contact2.mid )
            if mid2 in op.param3:
                if op.param2 in admin:
                    pass
                else:
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    settings["blacklist"][op.param2] = True
                    group = cl.getGroup(op.param1)
                    try:
                        group.preventedJoinByTicket = False
                        cl.updateGroup(group)
                        str1 = cl.reissueGroupTicket(op.param1)
                    except Exception as e:
                        print(e)
                    cl.sendMessage(mid2, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid3, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid4, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid5, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid6, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
            if mid3 in op.param3:
                if op.param2 in admin:
                    pass
                else:
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    settings["blacklist"][op.param2] = True
                    group = cl.getGroup(op.param1)
                    try:
                        group.preventedJoinByTicket = False
                        cl.updateGroup(group)
                        str1 = cl.reissueGroupTicket(op.param1)
                    except Exception as e:
                        print(e)
                    cl.sendMessage(mid2, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid3, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid4, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid5, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid6, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
            if mid4 in op.param3:
                if op.param2 in admin:
                    pass
                else:
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    settings["blacklist"][op.param2] = True
                    group = cl.getGroup(op.param1)
                    try:
                        group.preventedJoinByTicket = False
                        cl.updateGroup(group)
                        str1 = cl.reissueGroupTicket(op.param1)
                    except Exception as e:
                        print(e)
                    cl.sendMessage(mid2, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid3, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid4, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid5, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid6, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
            if mid5 in op.param3:
                if op.param2 in admin:
                    pass
                else:
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    settings["blacklist"][op.param2] = True
                    group = cl.getGroup(op.param1)
                    try:
                        group.preventedJoinByTicket = False
                        cl.updateGroup(group)
                        str1 = cl.reissueGroupTicket(op.param1)
                    except Exception as e:
                        print(e)
                    cl.sendMessage(mid2, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid3, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid4, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid5, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid6, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
            if mid6 in op.param3:
                if op.param2 in admin:
                    pass
                else:
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    settings["blacklist"][op.param2] = True
                    group = cl.getGroup(op.param1)
                    try:
                        group.preventedJoinByTicket = False
                        cl.updateGroup(group)
                        str1 = cl.reissueGroupTicket(op.param1)
                    except Exception as e:
                        print(e)
                    cl.sendMessage(mid2, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid3, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid4, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid5, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    cl.sendMessage(mid6, "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
        if op.type == 24:
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 13:
                if settings["contact"] == True:
                    msg.contentType = 0
                    if 'displayName' in msg.contentMetadata:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = cl.getProfileCoverURL(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                            cl.sendMessage(msg.to,"[顯示名稱]:\n" + msg.contentMetadata["顯示名稱"] + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[狀態消息]:\n" + contact.statusMessage + "\n[圖片網址]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[封面網址]:\n" + str(cu))
                    else:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = cl.getProfileCoverURL(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                        cl.sendMessage(msg.to,"[顯示名稱]:\n" + contact.displayName + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[狀態消息]:\n" + contact.statusMessage + "\n[圖片網址]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[封面網址]:\n" + str(cu))
            elif msg.contentType == 16:
                if settings["timeline"] == True:
                    msg.contentType = 0
                    msg.text = "作者" + cl.getContact(sender).displayName + "文章網址\n" + msg.contentMetadata["postEndUrl"]
                    cl.sendMessage(msg.to,msg.text)
            if msg.contentType == 0:
                if text is None:
                    return
            if sender in admin:
                if text.lower() == 'help':
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                    cl.sendContact(to, "u28d781fa3ba9783fd5144390352b0c24")
                elif text.lower() == 'help info':
                    helpMessageInfo = helpmessageinfo()
                    cl.sendMessage(to, str(helpMessageInfo))
                    cl.sendContact(to, "u28d781fa3ba9783fd5144390352b0c24")
                elif text.lower() == 'help bot':
                    helpMessageBot = helpmessagebot()
                    cl.sendMessage(to, str(helpMessageBot))
                    cl.sendContact(to, "u28d781fa3ba9783fd5144390352b0c24")
                elif text.lower() == 'help self':
                    helpMessageSelf = helpmessageself()
                    cl.sendMessage(to, str(helpMessageSelf))
                    cl.sendContact(to, "u28d781fa3ba9783fd5144390352b0c24")
                elif text.lower() == 'help group':
                    helpMessageGroup = helpmessagegroup()
                    cl.sendMessage(to, str(helpMessageGroup))
                    cl.sendContact(to, "u28d781fa3ba9783fd5144390352b0c24")
                elif text.lower() == 'help special':
                    helpMessageSpecial = helpMessagespecial()
                    cl.sendMessage(to, str(helpMessageSpecial))
                    cl.sendContact(to, "u28d781fa3ba9783fd5144390352b0c24")
                elif text.lower() == 'help kick':
                    helpMessagespecial = helpmessagekick()
                    cl.sendMessage(to, str(helpMessageKick))
                    cl.sendContact(to, "u28d781fa3ba9783fd5144390352b0c24")
                elif text.lower() == 'help tag':
                    helpMessageTag = helpmessagetag()
                    cl.sendMessage(to, str(helpMessageTag))
                    cl.sendContact(to, "u28d781fa3ba9783fd5144390352b0c24")
                elif "Fbc:" in msg.text:
                    bctxt = text.replace("Fbc:","")
                    t = cl.getAllContactIds()
                    for manusia in t:
                        cl.sendMessage(manusia,(bctxt))
                elif "Gbc:" in msg.text:
                    bctxt = text.replace("Gbc:","")
                    n = cl.getGroupIdsJoined()
                    for manusia in n:
                        cl.sendMessage(manusia,(bctxt))
                elif 'invitebot' in text.lower():
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        try:
                            group.preventedJoinByTicket = False
                            cl.updateGroup(group)
                            str1 = cl.reissueGroupTicket(to)
                        except Exception as e:
                            print(e)
                        cl.sendMessage(mid2, "/jgurlx gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                        cl.sendMessage(mid3, "/jgurlx gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                        cl.sendMessage(mid4, "/jgurlx gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                        cl.sendMessage(mid5, "/jgurlx gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                        cl.sendMessage(mid6, "/jgurlx gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                elif text.startswith("/jgurlx"):
                    str1 = find_between_r(msg.text, "gid: ", " gid")
                    str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                    cl.acceptGroupInvitationByTicket(str1, str2)
                    JoinedGroups.append(str1)
                    group = cl.getGroup(str1)
                    try:
                        cl.reissueGroupTicket(str1)
                        group.preventedJoinByTicket = True
                        cl.updateGroup(group)
                    except Exception as e:
                        print(e)
                elif "Ri " in msg.text:
                    Ri0 = text.replace("Ri ","")
                    Ri1 = Ri0.rstrip()
                    Ri2 = Ri1.replace("@","")
                    Ri3 = Ri2.rstrip()
                    _name = Ri3
                    gs = cl.getGroup(msg.to)
                    targets = []
                    for s in gs.members:
                        if _name in s.displayName:
                            targets.append(s.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            if target in admin:
                                pass
                            else:
                                try:
                                    cl.kickoutFromGroup(to,[target])
                                    cl.findAndAddContactsByMid(target)
                                    cl.inviteIntoGroup(to,[target])
                                except:
                                    pass
                elif "Tk " in msg.text:
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    targets = []
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        if target in admin:
                            pass
                        else:
                            try:
                                cl.kickoutFromGroup(to,[target])
                            except:
                                pass
                elif "Nk " in msg.text:
                    _name = text.replace("Nk ","")
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            if target in admin:
                                pass
                            else:
                                try:
                                    cl.kickoutFromGroup(to,[target])
                                except:
                                    pass
                elif "Vk " in msg.text:
                        vkick0 = msg.text.replace("Vk ","")
                        vkick1 = vkick0.rstrip()
                        vkick2 = vkick1.replace("@","")
                        vkick3 = vkick2.rstrip()
                        _name = vkick3
                        gs = cl.getGroup(msg.to)
                        targets = []
                        for s in gs.members:
                            if _name in s.displayName:
                                targets.append(s.mid)
                        if targets == []:
                            pass
                        else:
                            for target in targets:
                                try:
                                    cl.kickoutFromGroup(msg.to,[target])
                                    cl.findAndAddContactsByMid(target)
                                    cl.inviteIntoGroup(msg.to,[target])
                                    cl.cancelGroupInvitation(msg.to,[target])
                                except:
                                    pass
                elif "NT " in msg.text:
                    _name = text.replace("NT ","")
                    gs = cl.getGroup(to)
                    targets = []
                    net_ = ""
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        cl.sendMessage(to, "這個群組沒有這個人")
                    else:
                        for target in targets:
                            try:
                                sendMessageWithMention(to,target)
                            except:
                                pass
                elif text.lower() == 'zt':
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        cl.sendMessage(to, "這個群組沒有名字0字的人")
                    else:
                        mc = ""
                        for target in targets:
                            mc += sendMessageWithMention(to,target) + "\n"
                        cl.sendMessage(to, mc)
                elif text.lower() == 'zm':
                    gs = cl.getGroup(to)
                    lists = []
                    for g in gs.members:
                        if g.displayName in "":
                            lists.append(g.mid)
                    if lists == []:
                        cl.sendMessage(to, "這個群組沒有名字0字的人")
                    else:
                        mc = ""
                        for mi_d in lists:
                            mc += "->" + mi_d + "\n"
                        cl.sendMessage(to,mc)
                elif text.lower() == 'zc':
                    gs = cl.getGroup(to)
                    lists = []
                    for g in gs.members:
                        if g.displayName in "":
                            lists.append(g.mid)
                    if lists == []:
                        cl.sendMessage(to, "這個群組沒有名字0字的人")
                    else:
                        for ls in lists:
                            contact = cl.getContact(ls)
                            mi_d = contact.mid
                            cl.sendContact(to, mi_d)
                elif "Mc " in msg.text:
                    mmid = msg.text.replace("Mc ","")
                    cl.sendContact(to, mmid)
                elif "Sc " in msg.text:
                    ggid = msg.text.replace("Sc ","")
                    group = cl.getGroup(ggid)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "未找到"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "沒有"
                    else:
                        gQr = "開啟"
                        gTicket = "https://cl.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ 群組資料 ]"
                    ret_ += "\n╠ 顯示名稱 : {}".format(str(group.name))
                    ret_ += "\n╠ 群組ＩＤ : {}".format(group.id)
                    ret_ += "\n╠ 群組作者 : {}".format(str(gCreator))
                    ret_ += "\n╠ 成員數量 : {}".format(str(len(group.members)))
                    ret_ += "\n╠ 邀請數量 : {}".format(gPending)
                    ret_ += "\n╠ 群組網址 : {}".format(gQr)
                    ret_ += "\n╠ 群組網址 : {}".format(gTicket)
                    ret_ += "\n╚══[ 完 ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif msg.text in ["c","C","cancel","Cancel"]:
                  if msg.toType == 2:
                    X = cl.getGroup(msg.to)
                    if X.invitee is not None:
                        gInviMids = (contact.mid for contact in X.invitee)
                        ginfo = cl.getGroup(msg.to)
                        sinvitee = str(len(ginfo.invitee))
                        start = time.time()
                        for cancelmod in gInviMids:
                            cl.cancelGroupInvitation(msg.to, [cancelmod])
                        elapsed_time = time.time() - start
                        cl.sendMessage(to, "已取消完成\n取消時間: %s秒" % (elapsed_time))
                        cl.sendMessage(to, "取消人數:" + sinvitee)
                    else:
                        cl.sendMessage(to, "沒有任何人在邀請中！！")
                elif text.lower() == 'gcancel':
                    gid = cl.getGroupIdsInvited()
                    start = time.time()
                    for i in gid:
                        cl.rejectGroupInvitation(i)
                    elapsed_time = time.time() - start
                    cl.sendMessage(to, "全部群組邀請已取消")
                    cl.sendMessage(to, "取消時間: %s秒" % (elapsed_time))
                elif "Gn " in msg.text:
                    if msg.toType == 2:
                        X = cl.getGroup(msg.to)
                        X.name = msg.text.replace("Gn ","")
                        cl.updateGroup(X)
                    else:
                        cl.sendMessage(msg.to,"無法使用在群組外")
                elif "Gc" in msg.text:
                    if msg.toType == 2:
                        key = eval(msg.contentMetadata["MENTION"])
                        u = key["MENTIONEES"][0]["M"]
                        contact = cl.getContact(u)
                        cu = cl.getProfileCoverURL(mid=u)
                        try:
                            cl.sendMessage(msg.to,"名字:\n" + contact.displayName + "\n\n系統識別碼:\n" + contact.mid + "\n\n個性簽名:\n" + contact.statusMessage + "\n\n頭貼網址 :\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n\n封面網址 :\n" + str(cu))
                        except:
                            cl.sendMessage(msg.to,"名字:\n" + contact.displayName + "\n\n系統識別碼:\n" + contact.mid + "\n\n個性簽名:\n" + contact.statusMessage + "\n\n封面網址:\n" + str(cu))
                elif "Inv " in msg.text:
                    midd = msg.text.replace("Inv ","")
                    cl.findAndAddContactsByMid(midd)
                    cl.inviteIntoGroup(msg.to,[midd])
                elif "Ban" in msg.text:
                    if msg.toType == 2:
                        print ("[Ban] 成功")
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        if targets == []:
                            pass
                        else:
                            for target in targets:
                                try:
                                    settings["blacklist"][target] = True
                                    cl.sendMessage(to, "已加入黑名單")
                                except:
                                    pass
                elif "Unban" in msg.text:
                    if msg.toType == 2:
                        print ("[UnBan] 成功")
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        if targets == []:
                            pass
                        else:
                            for target in targets:
                                try:
                                    del settings["blacklist"][target]
                                    cl.sendMessage(to, "已解除黑名單")
                                except:
                                    pass
                elif text.lower() == 'clear ban':
                    for mi_d in settings["blacklist"]:
                        settings["blacklist"] = {}
                    cl.sendMessage(to, "已清空黑名單")
                elif text.lower() == 'banlist':
                    if settings["blacklist"] == {}:
                        cl.sendMessage(to, "沒有黑名單")
                    else:
                        cl.sendMessage(to, "以下是黑名單")
                        mc = ""
                        for mi_d in settings["blacklist"]:
                            mc += "->" + cl.getContact(mi_d).displayName + "\n"
                        cl.sendMessage(to, mc)
                elif text.lower() == 'kill ban':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                        for tag in settings["blacklist"]:
                            matched_list+=filter(lambda str: str == tag, gMembMids)
                        if matched_list == []:
                            print ("1")
                            cl.sendMessage(to, "沒有黑名單")
                            return
                        for jj in matched_list:
                            cl.kickoutFromGroup(to, [jj])
                        cl.sendMessage(to, "黑名單以踢除")
                elif "/invitemeto:" in msg.text:
                    gid = msg.text.replace("/invitemeto:","")
                    if gid == "":
                        cl.sendMessage(to,"請輸入群組ID")
                    else:
                        try:
                            cl.findAndAddContactsByMid(msg.from_)
                            cl.inviteIntoGroup(gid,[msg.from_])
                        except:
                            cl.sendMessage(to,"我不在那個群組裡")
                elif msg.text in ["主機離開全部群組"]:
                    gid = cl.getGroupIdsJoined()
                    for i in gid:
                        cl.leaveGroup(i)
                        cl.sendText(msg.to,"已離開全部群組")
                elif msg.text in ["SR","Setread"]:
                    cl.sendMessage(msg.to, "設置已讀點")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                    except:
                        pass
                    now2 = datetime.now()
                    wait2['readPoint'][msg.to] = msg.id
                    wait2['readMember'][msg.to] = ""
                    wait2['setTime'][msg.to] = datetime.strftime(now2,"%H:%M")
                    wait2['ROM'][msg.to] = {}
                    print ("設置已讀點")
                elif msg.text in ["LR","Lookread"]:
                    if msg.to in wait2['readPoint']:
                        print ("查詢已讀")
                        if wait2["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait2["ROM"][msg.to].items():
                                chiya += rom[1] + "\n"
                        cl.sendMessage(msg.to, "||已讀順序||%s\n\n||已讀的人||\n\n%s\n[%s]" % (wait2['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        cl.sendMessage(msg.to, "請輸入SR設置已讀點")
                elif msg.text in ["Friendlist"]:
                    anl = cl.getAllContactIds()
                    ap = ""
                    for q in anl:
                        ap += "• "+cl.getContact(q).displayName + "\n"
                    cl.sendMessage(msg.to,"「 朋友列表 」\n"+ap+"人數 : "+str(len(anl)))
                elif text.lower() == 'speed':
                    time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                    str1 = str(time0)
                    start = time.time()
                    cl.sendMessage(to,'處理速度\n' + str1 + '秒')
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,'指令反應\n' + format(str(elapsed_time)) + '秒')
                elif text.lower() == 'rebot':
                    cl.sendMessage(to, "重新啟動")
                    restartBot()
                elif text.lower() == 'runtime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    cl.sendMessage(to, "機器運行時間 {}".format(str(runtime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        owner = "u28d781fa3ba9783fd5144390352b0c24"
                        creator = cl.getContact(owner)
                        contact = cl.getContact(clMID)
                        grouplist = cl.getGroupIdsJoined()
                        contactlist = cl.getAllContactIds()
                        blockedlist = cl.getBlockedContactIds()
                        ret_ = "╔══[ 關於自己 ]"
                        ret_ += "\n╠ 名稱 : {}".format(contact.displayName)
                        ret_ += "\n╠ 群組 : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ 好友 : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ 黑單 : {}".format(str(len(blockedlist)))
                        ret_ += "\n╠══[ 關於機器 ]"
                        ret_ += "\n╠ 版本 : 淫蕩6主機測試版"
                        ret_ += "\n╠ 作者 : {}".format(creator.displayName)
                        ret_ += "\n╚══[ 未經許可禁止重製 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'set':
                    try:
                        ret_ = "╔══[ 設定 ]"
                        if settings["autoAdd"] == True: ret_ += "\n╠ 自動加入好友 ✅"
                        else: ret_ += "\n╠ 自動加入好友 ❌"
                        if settings["autoJoin"] == True: ret_ += "\n╠ 自動加入群組 ✅"
                        else: ret_ += "\n╠ 自動加入群組 ❌"
                        if settings["autoLeave"] == True: ret_ += "\n╠ 自動離開副本 ✅"
                        else: ret_ += "\n╠ 自動離開副本 ❌"
                        if settings["autoRead"] == True: ret_ += "\n╠ 自動已讀 ✅"
                        else: ret_ += "\n╠ 自動已讀 ❌"
                        if settings["detectMention"] == True: ret_ += "\n╠ 標注提醒 ✅"
                        else: ret_ += "\n╠ 標注提醒 ❌"
                        if settings["contact"] == True: ret_ += "\n╠ 詳細資料 ✅"
                        else: ret_ += "\n╠ 詳細資料 ❌"
                        if settings["reread"] == True: ret_ += "\n╠ 查詢收回開啟 ✅"
                        else: ret_ += "\n╠ 查詢收回關閉 ❌"
                        ret_ += "\n╚══[ 設定 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'add on':
                    settings["autoAdd"] = True
                    cl.sendMessage(to, "自動加入好友已開啟")
                elif text.lower() == 'add off':
                    settings["autoAdd"] = False
                    cl.sendMessage(to, "自動加入好友已關閉")
                elif text.lower() == 'join on':
                    settings["autoJoin"] = True
                    cl.sendMessage(to, "自動加入群組已開啟")
                elif text.lower() == 'join off':
                    settings["autoJoin"] = False
                    cl.sendMessage(to, "自動加入群組已關閉")
                elif text.lower() == 'leave on':
                    settings["autoLeave"] = True
                    cl.sendMessage(to, "自動離開副本已開啟")
                elif text.lower() == 'leave off':
                    settings["autoLeave"] = False
                    cl.sendMessage(to, "自動離開副本已關閉")
                elif text.lower() == 'read on':
                    settings["autoRead"] = True
                    cl.sendMessage(to, "自動已讀已開啟")
                elif text.lower() == 'read off':
                    settings["autoRead"] = False
                    cl.sendMessage(to, "自動已讀已關閉")
                elif text.lower() == 'tag on':
                    settings["detectMention"] = True
                    cl.sendMessage(to, "標註提醒已開啟")
                elif text.lower() == 'tag off':
                    settings["detectMention"] = False
                    cl.sendMessage(to, "標註提醒已關閉")
                elif text.lower() == 'contact on':
                    settings["contact"] = True
                    cl.sendMessage(to, "查看好友資料詳情開啟")
                elif text.lower() == 'contact off':
                    settings["contact"] = False
                    cl.sendMessage(to, "查看好友資料詳情關閉")
                elif text.lower() == 'inviteprotect on':
                    gid = cl.getGroup(to)
                    settings["inviteprotect"][gid.id] = True
                    cl.sendMessage(to, "群組邀請保護已開啟")
                elif text.lower() == 'inviteprotect off':
                    del settings["inviteprotect"][gid.id]
                    cl.sendMessage(to, "群組邀請保護已關閉")
                elif  text.lower() == 'inviteprotect list':
                    if settings["inviteprotect"] == {}:
                        cl.sendMessage(to, "沒有網址保護中的群組")
                    else:
                        cl.sendMessage(to, "以下是網址保護中的群組")
                        mc = ""
                        for gi_d in settings["inviteprotect"]:
                            mc += "->" + cl.getGroup(gi_d).name + "\n"
                        cl.sendMessage(to, mc)
                elif text.lower() == 'qr on':
                    gid = cl.getGroup(to)
                    settings["qrprotect"][gid.id] = True
                    cl.sendMessage(to, "群組網址保護已開啟")
                elif text.lower() == 'qr off':
                    gid = cl.getGroup(to)
                    del settings["qrprotect"][gid.id]
                    cl.sendMessage(to, "群組網址保護已關閉")
                elif  text.lower() == 'qr list':
                    if settings["qrprotect"] == {}:
                        cl.sendMessage(to, "沒有網址保護中的群組")
                    else:
                        cl.sendMessage(to, "以下是網址保護中的群組")
                        mc = ""
                        for gi_d in settings["qrprotect"]:
                            mc += "->" + cl.getGroup(gi_d).name + "\n"
                        cl.sendMessage(to, mc)
                elif text.lower() == 'allprotect on':
                    gid = cl.getGroup(to)
                    settings["qrprotect"][gid.id] = True
                    settings["protect"][gid.id] = True
                    settings["inviteprotect"][gid.id] = True
                    cl.sendMessage(to, "這群已經開啟全部保護")
                elif text.lower() == 'allprotect off':
                    gid = cl.getGroup(to)
                    del settings["qrprotect"][gid.id]
                    del settings["qrprotect"][gid.id]
                    del settings["inviteprotect"][gid.id]
                    cl.sendMessage(to, "這群已經關閉全部保護")
                elif text.lower() == 'protect on':
                    gid = cl.getGroup(to)
                    settings["protect"][gid.id] = True
                    cl.sendMessage(to, "群組保護已開啟")
                elif text.lower() == 'protect off':
                    gid = cl.getGroup(to)
                    del settings["protect"][gid.id]
                    cl.sendMessage(to, "群組保護已關閉")
                elif text.lower() == 'protectlist':
                    if settings["protect"] == {}:
                        cl.sendMessage(to, "沒有保護中的群組")
                    else:
                        cl.sendMessage(to, "以下是保護中的群組")
                        mc = ""
                        for gi_d in settings["protect"]:
                            mc += "->" + cl.getGroup(gi_d).name + "\n"
                        cl.sendMessage(to, mc)
                elif text.lower() == 'pi' or text.lower() == 'protect info':
                    ret_ = "╔══[ 保護狀態 ]"
                    gid = cl.getGroup(to)
                    if gid in settings["protect"]: ret_ += "\n╠ 群組保護 ✅"
                    else: ret_ += "\n╠ 群組保護 ❌"
                    if gid in settings["qrprotect"]: ret_ += "\n╠ 網址保護 ✅"
                    else: ret_ += "\n╠ 網址保護 ❌"
                    if gid in settings["inviteprotect"]: ret_ += "\n╠ 邀請保護 ✅"
                    else: ret_ += "\n╠ 邀請保護 ❌"
                    ret_ += "\n╚══[ 這個群組 ]"
                    cl.sendMessage(to, str(ret_))
                elif text.lower() == 'reread on':
                    settings["reread"] = True
                    cl.sendMessage(to, "查詢收回開啟")
                elif text.lower() == 'reread off':
                    settings["reread"] = False
                    cl.sendMessage(to, "查詢收回關閉")
                elif text.lower() == 'me':
                    sendMessageWithMention(to, sender)
                    cl.sendContact(to, sender)
                elif text.lower() == 'mid':
                    cl.sendMessage(msg.to,"[MID]\n" +  sender)
                elif msg.text.lower().startswith("contact "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            mi_d = contact.mid
                            cl.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("mid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = ""
                        for ls in lists:
                            ret_ += "" + ls
                        cl.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("picture "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + cl.getContact(ls).pictureStatus
                            cl.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("cover "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = cl.getProfileCoverURL(ls)
                                cl.sendImageWithURL(msg.to, str(path))
                elif text.lower() == 'gowner':
                    group = cl.getGroup(to)
                    GS = group.creator.mid
                    cl.sendContact(to, GS)
                elif text.lower() == 'gid':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, "[群組ID : ]\n" + gid.id)
                elif text.lower() == 'gname':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, "[群組名稱 : ]\n" + gid.name)
                elif text.lower() == 'gurl':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = cl.reissueGroupTicket(to)
                            cl.sendMessage(to, "[ 群組網址 ]\nhttps://cl.me/R/ti/g/{}".format(str(ticket)))
                        else:
                            cl.sendMessage(to, "群組網址未開啟，請用Ourl先開啟".format(str(settings["keyCommand"])))
                elif text.lower() == 'ourl':
                    if msg.toType == 2:
                        G = cl.getGroup(to)
                        if G.preventedJoinByTicket == False:
                            cl.sendMessage(to, "群組網址已開啟")
                        else:
                            G.preventedJoinByTicket = False
                            cl.updateGroup(G)
                            cl.sendMessage(to, "成功開啟群組網址")
                elif text.lower() == 'curl':
                    if msg.toType == 2:
                        G = cl.getGroup(to)
                        if G.preventedJoinByTicket == True:
                            cl.sendMessage(to, "群組網址已關閉")
                        else:
                            G.preventedJoinByTicket = True
                            cl.updateGroup(G)
                            cl.sendMessage(to, "成功關閉群組網址")
                elif text.lower() == 'ginfo':
                    group = cl.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "未找到"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "沒有"
                    else:
                        gQr = "開啟"
                        gTicket = "https://cl.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ 群組資料 ]"
                    ret_ += "\n╠ 顯示名稱 : {}".format(str(group.name))
                    ret_ += "\n╠ 群組ＩＤ : {}".format(group.id)
                    ret_ += "\n╠ 群組作者 : {}".format(str(gCreator))
                    ret_ += "\n╠ 成員數量 : {}".format(str(len(group.members)))
                    ret_ += "\n╠ 邀請數量 : {}".format(gPending)
                    ret_ += "\n╠ 群組網址 : {}".format(gQr)
                    ret_ += "\n╠ 群組網址 : {}".format(gTicket)
                    ret_ += "\n╚══[ 完 ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'tagall':
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        cl.sendMessage(to, "總共 {} 個成員".format(str(len(nama))))
                elif text.lower() == 'sn':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read['readPoint']:
                            try:
                                del read['readPoint'][msg.to]
                                del read['readMember'][msg.to]
                                del read['readTime'][msg.to]
                            except:
                                pass
                            read['readPoint'][msg.to] = msg.id
                            read['readMember'][msg.to] = ""
                            read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                            read['ROM'][msg.to] = {}
                            with open('read.json', 'w') as fp:
                                json.dump(read, fp, sort_keys=True, indent=4)
                                cl.sendMessage(msg.to,"已讀點已開始")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        read['readPoint'][msg.to] = msg.id
                        read['readMember'][msg.to] = ""
                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        read['ROM'][msg.to] = {}
                        with open('read.json', 'w') as fp:
                            json.dump(read, fp, sort_keys=True, indent=4)
                            cl.sendMessage(msg.to, "設定已讀點:\n" + readTime)
                elif text.lower() == 'sf':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to not in read['readPoint']:
                        cl.sendMessage(msg.to,"已讀點已經關閉")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                              pass
                        cl.sendMessage(msg.to, "刪除已讀點:\n" + readTime)
                elif text.lower() == 'ar':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\n時間 : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read["readPoint"]:
                        try:
                            read["readPoint"] = {}
                            read["readMember"] = {}
                            read["readTime"] = {}
                        except:
                            pass
                        cl.sendMessage(msg.to, "重置已讀點:\n" + readTime)
                    else:
                        cl.sendMessage(msg.to, "已讀點未設定")
                        
                elif text.lower() == 'r':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\n時間 : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if receiver in read['readPoint']:
                        if read["ROM"][receiver].items() == []:
                            cl.sendMessage(receiver,"[ 已讀者 ]:\n沒有")
                        else:
                            chiya = []
                            for rom in read["ROM"][receiver].items():
                                chiya.append(rom[1])
                            cmem = cl.getContacts(chiya)
                            zx = ""
                            zxc = ""
                            zx2 = []
                            xpesan = '[ 已讀者 ]:\n'
                        for x in range(len(cmem)):
                            xname = str(cmem[x].displayName)
                            pesan = ''
                            pesan2 = pesan+"@c\n"
                            xlen = str(len(zxc)+len(xpesan))
                            xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                            zx2.append(zx)
                            zxc += pesan2
                        text = xpesan+ zxc + "\n[ 已讀時間 ]: \n" + readTime
                        try:
                            cl.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                        except Exception as error:
                            print (error)
                        pass
                    else:
                        cl.sendMessage(receiver,"已讀點未設定")
                elif text.lower() == 'time':
                    tz = pytz.timezone("Asia/Makassar")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\n時間 : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    cl.sendMessage(msg.to, readTime)
        if op.type == 26:
            try:
                msg = op.message
                if settings["reread"] == True:
                    if msg.toType == 0:
                        cl.log("[%s]"%(msg._from)+msg.text)
                    else:
                        cl.log("[%s]"%(msg.to)+msg.text)
                    if msg.contentType == 0:
                        msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
                else:
                    pass
            except Exception as e:
                print(e)
        if op.type == 65:
            try:
                at = op.param1
                msg_id = op.param2
                if settings["reread"] == True:
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"] not in bl:
                            cl.sendMessage(at,"%s\n[收回了]\n%s"%(cl.getContact(msg_dict[msg_id]["from"]).displayName,msg_dict[msg_id]["text"]))
                            print ["收回訊息"]
                        del msg_dict[msg_id]
                else:
                    pass
            except Exception as e:
                print(e)
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    cl.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                   text = msg.text
                   if text is not None:
                       cl.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in clMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if clMID in mention["M"]:
                                if settings["detectMention"] == True:
                                    contact = cl.getContact(sender)
                                    cl.sendMessage(to, "標我幹嘛?")
                                    sendMessageWithMention(to, contact.mid)
                                break
        if op.type == 55:
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
            try:
                if op.param1 in wait2['readPoint']:
                    Name = cl.getContact(op.param2).displayName
                    if Name in wait2['readMember'][op.param1]:
                        pass
                    else:
                        wait2['readMember'][op.param1] += "\n[•]" + Name
                        wait2['ROM'][op.param1][op.param2] = "[•]" + Name
                        print (time.time() + name)
                else:
                    pass
            except:
                pass
    except Exception as error:
        logError(error)
def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
