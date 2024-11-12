from tools.environment import *
from .genshin import Genshin
import os
from tools.software import get_pid, close
import json
from win32gui import FindWindow


class Domain(Genshin):
    def genshin_domain(self):
        # 确认BGI路径
        pid = get_pid("BetterGI.exe")
        if pid is not None:
            self.indicate("BGI已启动,准备重启")
            close(pid)
        _path = self.task["启动"]["BGI"]
        if os.path.isfile(_path):
            dire, name = os.path.split(_path)
            if name == "BetterGI.exe":
                pass
            else:
                self.indicate("BGI,无效启动路径")
                return True
        else:
            self.indicate("BGI,无效启动路径")
            return True
        
        # 检查树脂
        if self.task["resin"] is None:
            self.home()
            self.open_sub("背包")
            wait(2000)
            self.check_overdue()
            click((1247, 54))
            wait(800)
            sc = scshot()
            (x, y), val = find_pic(r"assets\genshin\picture\valu_tools\nssz.png",
                                   (110, 112, 1273, 805), sc)
            if val > 0.7:
                cond = int(ocr((x-15, y+65, x+15, y+92), sc)[0])
            else:
                cond = 0
            del sc
            click((1843, 46))
            wait(1500)
        else:
            cond = None
        self.open_sub("冒险之证")
        click((300, 440))
        wait(800)
        if self.task["resin"] is None:
            ori = int((ocr((1368, 200, 1462, 236))[0].split("/")[0]).strip(" "))
        else:
            [ori, cond] = self.task["resin"]
        self.indicate(f"当前树脂：\n"
                      f"  原粹树脂: {ori} / 160\n"
                      f"  浓缩树脂: {cond} 个")
        if (ori > 19) or (cond > 0):
            self.indicate("树脂足够,开始自动秘境")
            self.home()
        else:
            self.indicate("树脂不足,自动秘境停止")
            click((1673, 235))
            wait(1500)
            return 0
        # 传送至秘境
        _domain = self.task["秘境"]
        self.tp_domain(_domain[1])
        click((1690, 1008))
        wait(800)
        self.world()
        self.indicate(f"到达秘境:{_domain[0]} {_domain[1]}")

        # 切换战斗队伍(2号队)
        self.team_change_to(2)
        self.indicate("已切换至战斗队伍")

        if _domain[1] == "太山府":
            pass
        elif _domain[1] == "无妄引咎密宫":
            keydown("W")
            wait(500)
            keyup("W")
            wait(500)
            keydown("A")
            wait(1000)
            keyup("A")
        elif _domain[1] == "芬德尼尔之顶":
            pass
        else:
            keydown("W")
            wait(4000)
            keyup("W")
        # 读取快捷键
        _c = os.path.split(_path)[0] + "/User/config.json"
        with open(_c, 'r', encoding='utf-8') as c:
            _dir = json.load(c)
        # 启动BGI

        def run_bgi():
            cmd = f"start \"\" \"{_path}\""
            for n in range(2):
                run(cmd, shell=True)
                for sec in range(10):
                    wait(1000)
                    hwnd = FindWindow(None, "更好的原神")
                    if hwnd:
                        self.indicate("BGI启动成功")
                        return True
            self.indicate("BGI启动异常")
            return True
        run_bgi()
        wait(3000)
        _s = _dir["hotKeyConfig"]["bgiEnabledHotkey"]
        _d = _dir["hotKeyConfig"]["autoDomainHotkey"]
        from pyautogui import hotkey

        def dopress(key):
            if "+" in key:
                _l = key.split("+")
                for i in range(4-len(_l)):
                    _l += [""]
                _k1, _k2, _k3, _k4 = _l
                hotkey(_k1.strip(" "), _k2.strip(" "), _k3.strip(" "), _k4.strip(" "))
            else:
                press(key)
        dopress(_s)
        wait(1500)
        env.soft.foreground()
        wait(500)
        dopress(_d)
        wait(1000)
        self.indicate("BGI自动秘境运行中...")
        _dire = os.path.split(_path)[0] + "/log/"
        _name = os.listdir(_dire)[-1]
        path = _dire + _name
        while 1:
            wait(5000)
            f = open(path, encoding='utf-8')
            if "→ \"自动秘境结束\"" in f.readlines()[-2] or "→ \"任务结束\"" in f.readlines()[-2]:
                break
        # env.soft.kill()
        # 关闭BGI
        pid = get_pid("BetterGI.exe")
        if pid is not None:
            close(pid)
        self.indicate("BGI自动秘境运行完成")
        return False
