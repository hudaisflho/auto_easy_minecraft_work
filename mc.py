import ctypes
import sys
import time
import threading
from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener

# ========== 管理员权限提升 ==========
def is_admin():
    """检查是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_admin():
    """请求管理员权限并重启程序"""
    if not is_admin():
        # 重新以管理员身份运行脚本
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()  # 退出当前进程

# 调用管理员权限提升
elevate_admin()
print("✅ 已获得管理员权限！")
# ==================================

"""操作按键控制"""

jump = Key.space  # """跳跃"""
sneak = Key.shift_l  # """潜行"""
sprint = Key.ctrl_l  # """疾跑"""
strafe_left = KeyCode.from_char('a')  # """左"""
strafe_right = KeyCode.from_char('d')  # """右"""
walk_backward = KeyCode.from_char('s')  # """后"""
walk_forward = KeyCode.from_char('w')  # """前"""

attack_destroy = Button.left  # """攻击/摧毁"""
use_item_place_block = Button.right  # """使用物品/放置方块"""

drop_selected_item = KeyCode.from_char('q')  # """丢弃物品"""
hotbar_slot_1 = KeyCode.from_char('1')  # """快捷栏"""
open_close_inventory = KeyCode.from_char('e')  # """物品栏"""
swap_item_with_off_hand = KeyCode.from_char('f')  # """副手交换"""
hotbar_slot_2 = KeyCode.from_char('2')
hotbar_slot_3 = KeyCode.from_char('3')
hotbar_slot_4 = KeyCode.from_char('4')
hotbar_slot_5 = KeyCode.from_char('5')
hotbar_slot_6 = KeyCode.from_char('6')
hotbar_slot_7 = KeyCode.from_char('7')
hotbar_slot_8 = KeyCode.from_char('8')
hotbar_slot_9 = KeyCode.from_char('9')


"""技能按键控制"""

stop_event = False  # 终止线程

mine_forward_key = 'v'
rushing_key = 'c'
boating_key = 'x'
build_up_key = 'n'

class InputManager:
    def __init__(self):
        self.kb = KeyboardController()
        self.mouse = MouseController()
        self.pressed_items = set()  # 记录当前按下的键/按钮

    def press(self, item):
        """
        按下任意键或鼠标按钮
        """
        if isinstance(item, (Key, KeyCode, str)):
            self.kb.press(item)
        elif isinstance(item, Button):
            self.mouse.press(item)
        else:
            raise TypeError(f"不支持的输入类型: {type(item)}")
        self.pressed_items.add(item)

    def release(self, item):
        """
        释放任意键或鼠标按钮
        """
        if isinstance(item, (Key, KeyCode, str)):
            self.kb.release(item)
        elif isinstance(item, Button):
            self.mouse.release(item)
        else:
            raise TypeError(f"不支持的输入类型: {type(item)}")
        self.pressed_items.discard(item)

    def tap(self, item, count=1):
        """
        点击任意键或鼠标按钮
        """
        for _ in range(count):
            self.press(item)
            self.release(item)

    def release_all(self):
        """
        释放所有按下的键/按钮（紧急清理）
        """
        for item in list(self.pressed_items):
            self.release(item)
        self.pressed_items.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release_all()
        return False


im = InputManager()


def matches_key(key, target_char):
    """检测按键是否匹配目标字符，考虑Ctrl等修饰键按下时char可能变化的情况"""
    if hasattr(key, "char") and key.char == target_char:
        return True
    if hasattr(key, "vk") and key.vk is not None:
        try:
            if chr(key.vk).lower() == target_char:
                return True
        except (ValueError, OverflowError):
            pass
    return False


"""向前挖矿"""
mine_forward_active = False


def mine_forward(key):
    global mine_forward_active

    mine_forward_active = not mine_forward_active
    if mine_forward_active:
        im.press(walk_forward)
        im.press(attack_destroy)
        print("向前挖矿开始")
    else:
        im.release(walk_forward)
        im.release(attack_destroy)
        print("向前挖矿结束")


"""向前疾跑"""
rushing_active = False


def rushing(key):
    global rushing_active

    rushing_active = not rushing_active
    if rushing_active:
        im.tap(jump)
        im.press(walk_forward)
        im.press(sprint)
        im.press(jump)
        print("向前疾跑开始")
    else:
        im.release(walk_forward)
        im.release(sprint)
        im.release(jump)
        print("向前疾跑结束")


"""划船"""
boating_active = False


def boating(key):
    global boating_active

    boating_active = not boating_active
    if boating_active:
        im.press(walk_forward)
        im.press(sprint)
        print("划船开始")
    else:
        im.release(walk_forward)
        im.release(sprint)
        print("划船结束")


"""向上搭方块"""
build_up_active = False
build_up_thread = None


def build_up_loop():
    global build_up_active
    global stop_event
    i = 0
    while build_up_active and not stop_event:
        im.press(jump)
        time.sleep(0.3)
        im.release(jump)
        im.tap(use_item_place_block)
        time.sleep(0.1)
        i += 1
        print(i)


def build_up(key):
    global build_up_active
    global build_up_thread
    build_up_active = not build_up_active
    if build_up_active:
        print("向上搭方块开始")
        # 启动新线程执行搭方块循环
        build_up_thread = threading.Thread(target=build_up_loop, daemon=True)
        build_up_thread.start()
    else:
        im.release(jump)
        print("向上搭方块结束")


def on_press(key):
    if matches_key(key, boating_key):
        boating(key)
    if matches_key(key, rushing_key):
        rushing(key)
    if matches_key(key, mine_forward_key):
        mine_forward(key)
    if matches_key(key, build_up_key):
        build_up(key)


def on_release(key):
    global stop_event
    if hasattr(key, "char") and key.char == '0':
        print("\n程序结束")
        stop_event = True
        return False


if __name__ == "__main__":

    print("\nauto mc begins!\n")

    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    except KeyboardInterrupt:
        print("\nProgram interrupted by user\n")

    finally:
        globals()['stop_event'] = True
        all_vars = globals()

        # 遍历所有变量名，找到以 '_active' 结尾的
        for var_name in list(all_vars.keys()):
            if var_name.endswith('_active'):
                all_vars[var_name] = False

        im.release_all()