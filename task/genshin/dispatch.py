from tools.environment import *
from .genshin import Genshin


class Dispatch(Genshin):
    def genshin_dispatch(self):
        temp_dir = \
            {"区域坐标": [[136, 162], [132, 237], [134, 304], [132, 378], [133, 447],[132,528]],
             "name": ["蒙德", "璃月", "稻妻", "须弥", "枫丹","纳塔"],
             0: [[1049, 342], [1173, 661], [565, 405],
                 [1120, 450], [814, 244], [740, 531]],
             1: [[960, 453], [810, 558], [563, 564],
                 [724, 330], [1173, 614], [731, 820]],
             2: [[830, 827], [1099, 281], [586, 804],
                 [725, 695], [934, 343], [1146, 435]],
             3: [[1030, 611], [1049, 249], [796, 303],
                 [680, 640], [957, 374], [901, 556]],
             4: [[1055, 249], [898, 455], [1027, 584],
                 [822, 641], [654, 315], [616, 552]],
             5: [[941,190], [728,239], [1121,357],
                 [681,512], [843,508], [984,713]],
             "name0": ["水晶矿,白银矿(1)", "水晶矿,白银矿(2)", "摩拉",
                       "兽肉,禽肉", "禽蛋,甜甜花", "白萝卜,胡萝卜"],
             "name1": ["水晶矿,白银矿", "摩拉1", "摩拉2",
                       "马尾,金鱼草", "白萝卜,胡萝卜", "莲蓬,松茸"],
             "name2": ["摩拉1", "摩拉2", "兽肉,禽蛋",
                       "禽肉,海草", "白萝卜,堇瓜", "甜甜花,日落果"],
             "name3": ["摩拉", "蔷薇,苹果", "松茸,蘑菇",
                       "禽蛋,日落果", "香辛果,胡萝卜", "墩墩桃,松果"],
             "name4": ["摩拉", "汐藻,蘑菇", "茉洁草,禽蛋",
                       "久雨莲,兽肉", "泡泡桔,禽肉", "甜甜花,薄荷"],
             "name5": ["颗粒果,蘑菇", "兽肉,苹果", "烬芯花,白萝卜",
                       "摩拉", "苦种,胡萝卜", "澄晶实,薄荷"],
             "y_list": [123, 228, 332, 440, 545]}

        for i in range(3):
            self.tp_fontaine1()
            self.indicate("前往枫丹凯瑟琳")
            keydown("W")
            wait(2700)
            keyup("W")
            wait(500)
            keydown("A")
            wait(1500)
            keyup("A")
            wait(500)
            press("F")
            wait(1000)
            click((960, 900))
            wait(1500)
            x, y = find_pic(r"assets\genshin\picture\dispatch\dispatch.png",
                            (1253,397,1846,843))[0]
            if (x, y) == (0, 0):
                if i ==3:
                    self.indicate("派遣未知错误,重试多次")
                    return True
                else:
                    self.indicate(f"error:派遣未知错误,开始重试第{i+1}次")
                    continue
            else:
                break

        if  find_color("yellow", (x+20,y-20, x+150, y+20))[1]: #判断是否有探索派遣几个字是否变黄色
            self.indicate("存在可领取派遣")
        else:
            self.indicate("无派遣可领取，尝试重新派遣")

        click((x + 30, y)) #点击进入派遣页面
        wait(2000)

        if "全部领取" in ocr((108, 992, 252, 1045))[0]:
            click((169, 1020))
            wait(2000)
            if self.task["再次派遣"]:
                self.indicate("再次派遣")
                click((1151, 1015))
            else:
                click((786, 1016))
            wait(2000)

        # 检查派遣
        for i in range(3):
            _num = ocr((1565,31,1780,58))[0]
            if str.isdigit(_num[-3]):
                _num = int(_num[-3])
                break
            if i == 2:
                self.indicate("派遣未知错误,重试多次")
                return True

        if _num == 5:
            self.indicate("派遣已满，跳过")
            return False
        elif 0 <= _num < 5:
            for num in range(5):  # 派遣
                _r, _m = self.task[f"派遣{num}"]
                _n = temp_dir["name"][_r]
                cname = "%s-%s" % (_n, temp_dir[f"name{_r}"][_m])
                self.indicate("检查派遣:\n  %s" % cname)
                x, y = temp_dir["区域坐标"][_r]
                click((x, y))
                wait(800)
                x, y = temp_dir[_r][_m]
                click((x, y))
                wait(800)
                _text = ocr((1490, 979, 1823, 1050))[0]
                if "召回" in _text:
                    self.indicate("执行中:\n  " + cname)
                elif "选择角色" in _text:
                    self.indicate("可以开始派遣:\n  " + cname)
                    click((1793, 683))
                    wait(500)
                    click((1692, 1024))
                    wait(1000)
                    alist, blist, clist = [], [], []
                    sc = screenshot()
                    for y in temp_dir["y_list"]:
                        if "探险中" in ocr((221, y, 429, y + 46), sc)[0]:
                            continue
                        else:
                            _t = ocr((221, y + 46, 429, y + 82), sc)[0]
                            if "时长为" in _t:
                                alist += [y]
                            elif "探索派遣" in _t:
                                blist += [y]
                            elif "无加成" in _t:
                                clist += [y]
                            else:
                                self.indicate("原神:派遣选择角色异常")
                                remove(sc)
                                raise RuntimeError("原神:派遣检查异常")
                    remove(sc)
                    if alist:
                        y = alist[0]
                    elif blist:
                        y = blist[0]
                    else:
                        y = clist[0]
                    click((269, y + 40))
                    self.indicate("开始派遣:" + cname)
                    wait(800)
                    _num += 1
                    if _num == 5:
                        self.indicate("已重新派遣")
                        break
                else:
                    self.indicate("派遣检查异常")
                    raise RuntimeError("原神:派遣检查异常")
        else:
            self.indicate("派遣检查异常")
            raise RuntimeError("原神:派遣检查异常")
        # 关闭派遣
        click((1853, 51))
        self.indicate("派遣任务完成")
        wait(3500)
        self.home()
        return False