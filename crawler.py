# -*- coding: utf-8 -*-
import random
import ConfigParser
import re
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#汉字判断模块
def cncheck(k):
    if k == 'Magic 2015' or k == 'Magic 2010' or k == 'Magic 2011' or k == 'Eternal Masters' or k == 'Modern Masters 2015 Edition' or k == 'Conspiracy' or k == 'Commander 2015' or k == 'Commander 2014 Edition' or k == 'Portal Three Kingdoms' or k == 'Alara Reborn' or k == 'Time Spiral' or k == 'Time Spiral "Timeshifted"' or k == 'Saviors of Kamigawa' or k == 'Welcome Deck 2016' or k == 'Ninth Edition Box Set' or k == 'Conspiracy: Take the Crown' or k == "Ugin's Fate" or k == 'Theros':
        return True
    else:
        for r in k:
            if r >= u'\u4e00' and r <= u'\u9fa5':
                return True
            else:
                return False


#mtginfo爬虫抓取
sname = raw_input("系列缩写：")
snamen = raw_input("系列卡牌数量：")
i1 = raw_input("输入起始录入编号：")
#获取卡牌数据库文件
cardfile = ConfigParser.ConfigParser()
cardfile.read("data/card.conf")
ecardfile = ConfigParser.ConfigParser()
ecardfile.read("data/ecard.conf")
sections = cardfile.sections()
esections = ecardfile.sections()
engine = webdriver.PhantomJS()
i = int(i1)
sm = 0
while (i <= int(snamen)):
    if sm == 2:
        i = i - 1
        url = "http://magiccards.info/" + sname + "/cn/"+ str(i) +"b.html"
        sm = 0
    else:
        url = "http://magiccards.info/" + sname + "/cn/"+ str(i) +".html"
    engine.get(url)
    #获取牌名
    name = engine.find_elements_by_xpath('/html/body/table[3]/tbody/tr/td[2]/span/a')
    #cardfile.add_section(name1)
    if len(name) == 0:
        sm = 1
        url = "http://magiccards.info/" + sname + "/cn/"+ str(i) +"a.html"
        engine.get(url)
        name = engine.find_elements_by_xpath('/html/body/table[3]/tbody/tr/td[2]/span/a')
        sm = 2
    for t in name:
        cname = t.text
    if cname in sections:
        print cname + "已经录入，不做处理"
    else:
        #写入section
        cardfile.add_section(cname)
        print "牌名：" + cname
        #获取英文牌名
        ename = engine.find_elements_by_xpath('/html/body/table[3]/tbody/tr/td[3]/small/a[1]')
        for u in ename:
            check = cncheck(u.text)
            a = 1
            while check is True:
                a = a + 1
                #if sm == 1:
                #    url = "http://magiccards.info/" + sname + "/cn/" + str(i) + "a.html"
                # url = "http://magiccards.info/" + sname + "/cn/"+ str(i) +".html"
                # engine.get(url)
                ename = engine.find_elements_by_xpath('/html/body/table[3]/tbody/tr/td[3]/small/a[' + str(a) + ']')
                for u in ename:
                    check = cncheck(u.text)
            cename = u.text
            cardfile.set(cname, "ename", cename)
            cardfile.set(cname, "url", url)
            if cename in esections:
                pass
            else:
                ecardfile.add_section(cename)
            ecardfile.set(cename, "name", cname)
            print "英文牌名：" + cename
        info = engine.find_elements_by_xpath('/html/body/table[3]/tbody/tr/td[2]/p[1]')
        xginfo = engine.find_elements_by_xpath('/html/body/table[3]/tbody/tr/td[2]/p[2]/b')
        for w in xginfo:
            xg = w.text
        for p in info:
            match = re.compile('\s')
            infom = match.split(p.text)
        num = len(infom)
        xg = xg.replace(' ','')
        xg = xg.replace('\n','')
        if num == 3:
            if "生物" in infom[0]:
                #费用为X的生物
                lb = infom[0].strip(',')
                gf = infom[1].strip(',')
                fy = infom[2].strip(',')
                cardfile.set(cname, "类别", lb)
                cardfile.set(cname, "攻防", gf)
                cardfile.set(cname, "费用", fy)
                cardfile.set(cname, "规则叙述", xg)
                print "类别：" + lb + "\n" + "攻防：" + gf + "\n" + "费用：" + fy + "\n" + "效果：" + xg
            else:
                lb = infom[0].strip(",")
                #gf = infom[1].strip(",")
                fy = infom[1].strip(",")
                cardfile.set(cname, "类别", lb)
                #cardfile.set(cname, "攻防", gf)
                cardfile.set(cname, "费用", fy)
                cardfile.set(cname, "规则叙述", xg)
                print  "类别：" + lb + "\n" + "费用：" + fy + "\n" + "效果：" + xg
        elif num == 4:
            lb = infom[0].strip(",")
            gf = infom[1].strip(",")
            fy = infom[2].strip(",")
            cardfile.set(cname, "类别", lb)
            cardfile.set(cname, "攻防", gf)
            cardfile.set(cname, "费用", fy)
            cardfile.set(cname, "规则叙述", xg)
            print "类别：" + lb + "\n" + "攻防：" + gf + "\n" + "费用：" + fy + "\n" + "效果：" + xg
        elif num >= 5:
            if "鹏洛客" in infom[0].strip(",") :
                lb = infom[0].strip(",")
                gf = infom[2].strip(",")
                fy = infom[3].strip(",")
                cardfile.set(cname, "类别", lb)
                cardfile.set(cname, "攻防", gf)
                cardfile.set(cname, "费用", fy)
                cardfile.set(cname, "规则叙述", xg)
                print "类别：" + lb + "\n" + "忠诚度：" + gf + "\n" + "费用：" + fy + "\n" + "效果：" + xg
            else :
                lb = "格式错误"
                cardfile.set(cname, "类别", lb)
                print t.text + "格式错误，未输入，请手工录入"
        elif num == 2:
            lb = infom[0].strip(",")
            fy = infom[1].strip(",")
            cardfile.set(cname, "规则叙述", xg)
            cardfile.set(cname, "类别", lb)
            cardfile.set(cname, "费用", fy)
            print "类别：" + lb + "\n" + "费用：" + fy + "\n" + "效果：" + xg
        elif num <= 1:
            lb = infom[0].strip(",")
            cardfile.set(cname, "类别", lb)
            cardfile.set(cname, "规则叙述", xg)
            print "类别：" + lb + "\n" + "效果：" + xg
        else :
            print "查无此牌"
    cardfile.write(open("data/card.conf", "w"))
    ecardfile.write(open("data/ecard.conf", "w"))
    i = i + 1

print "处理完毕"
engine.quit()





'''
#mtginfo爬虫抓取
cname = raw_input("Cname:")
driver = webdriver.PhantomJS()
cname = cname.encode('utf-8')
driver.get("http://magiccards.info/query?q=" + cname + "&v=card&s=cname")
data = driver.find_elements_by_xpath('//*[@id="TCGPHiLoTable"]/tbody/tr/td[2]/a')
for t in data:
    print t.text
driver.quit()


#cname = raw_input("牌名：")
url = "http://www.guokr.com/"
page = requests.get(url).content

s = etree.HTML(page)
h = s.xpath('//*[@id="newGroups"]/ul[1]/li[1]/div/span/text()')

for i in h:
    print i

'''



