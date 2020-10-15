import numpy as np
import random
from sys import exit
from random import shuffle

# numpy 提供数组对应位置相加。不用我门自己计算，用于多轮游戏分数统计
# shuffle 随机打乱列表

# 初始化扑克牌
playing_cards = {"黑桃A": 1, "黑桃2": 2, "黑桃3": 3, "黑桃4": 4, "黑桃5": 5, "黑桃6": 6, "黑桃7": 7, "黑桃8": 8, "黑桃9": 9,
                 "黑桃10": 10, "黑桃J": 10, "黑桃Q": 10, "黑桃K": 10, "红桃A": 1, "红桃2": 2, "红桃3": 3, "红桃4": 4,
                 "红桃5": 5, "红桃6": 6, "红桃7": 7, "红桃8": 8, "红桃9": 9, "红桃10": 10, "红桃J": 10, "红桃Q": 10,
                 "红桃K": 10, "方块A": 1, "方块2": 2, "方块3": 3, "方块4": 4, "方块5": 5, "方块6": 6, "方块7": 7, "方块8": 8,
                 "方块9": 9, "方块10": 10, "方块J": 10, "方块Q": 10, "方块K": 10, "梅花A": 1, "梅花2": 2, "梅花3": 3,
                 "梅花4": 4, "梅花5": 5, "梅花6": 6, "梅花7": 7, "梅花8": 8, "梅花9": 9, "梅花10": 10, "梅花J": 10,
                 "梅花Q": 10, "梅花K": 10}

# 扑克牌数
poker_name = list(playing_cards.keys())
poker_count = 1
poker_list = poker_count * poker_name

# 用于判断手中的牌是否有A，根据分数来判断A值为1还是11
four_A = {"黑桃A", "方块A", "红桃A", "梅花A"}

# 计分期
total_score = np.array([0, 0])

# 回合
game_round = 1

"""
洗牌，重新对扑克牌进行排列
"""


def random_card(poker_name_list):
    shuffle(poker_name_list)


"""
计算手里牌的分数, 参数是一个list
"""


def score_count(hand_poker):
    # 声明变量，记录拍的总分数
    poker_score = 0
    # 是否有A
    have_a = False

    for k in hand_poker:
        poker_score += playing_cards[k]

    for a in hand_poker:
        if a in four_A:
            have_a = True
            break
        else:
            continue

    if have_a:
        if poker_score + 10 <= 21:
            poker_score += 10

    return poker_score


"""
判断输赢的函数
"""


def who_win(your_score, pc_socre):
    if your_score > 21 and pc_socre > 21:
        print("平局了")
        return np.array([0, 0])
    elif your_score > 21 and pc_socre <= 21:
        print("你输了")
        return np.array([0, 1])
    elif your_score <= 21 and pc_socre > 21:
        print("这个得恭喜")
        return np.array([1, 0])
    elif your_score <= 21 and pc_socre <= 21:
        if your_score < pc_socre:
            print("你输了")
            return np.array([0, 1])
        elif your_score > pc_socre:
            print("你赢了")
            return np.array([1, 0])
        else:
            print("平局了")
            return np.array([0, 0])


"""
是否继续要牌
"""


def if_get_next_card():
    if_continue = input("是否继续要牌？(Y/N)>>>>>>>>>>:")
    if if_continue.upper() == "Y":
        return get_one_poker(poker_list)
    elif if_continue.upper() == "N":
        print("玩家停止要牌")
        return False
    else:
        print("请重新输入")
        return if_get_next_card()


"""
从排队随机取牌
"""


def get_one_poker(poker_list):
    # 必须要在牌堆中删除一张牌
    return poker_list.pop(random.randint(0, len(poker_list) - 1))


"""
一轮游戏之后询问玩家是否继续
"""


def continue_or_quit():
    if_next_round = input("你还想再玩一局吗（Y/N）?>>>>>")
    if if_next_round.upper() == "Y":
        if len(poker_list) < 15:
            print("剩余的牌数太少不能再玩了")
            exit(1)
        else:
            return True
    elif if_next_round.upper() == "N":
        print("玩家不玩了")
        exit(1)
    else:
        print("输入错误")
        continue_or_quit()


# 开局初始化的牌， 自动给玩家和电脑发两张
def start_game_init_poker(rest_poker_list):
    return [rest_poker_list.pop(random.randint(0, len(rest_poker_list) - 1)),
            rest_poker_list.pop(random.randint(0, len(rest_poker_list) - 1))]


"""
每一次游戏的流程
"""


def every_round(rest_poker_list):
    # 声明一个变量 代表手里的扑克和电脑手里的扑克
    your_hand_poker = []
    pc_hand_poker = []

    # 一个回合的游戏，首先自动抽取两张牌
    you_init_poker = start_game_init_poker(rest_poker_list)
    pc_init_poker = start_game_init_poker(rest_poker_list)

    print(f"玩家获得的扑克牌是{you_init_poker[0]}和{you_init_poker[1]}")
    print(f"电脑获得的扑克牌是{pc_init_poker[0]}和?")

    # 荷官同志把牌送到我们的手中
    your_hand_poker.extend(you_init_poker)
    pc_hand_poker.extend(pc_init_poker)

    # 计算初始牌面的分数
    score = np.array([score_count(you_init_poker), score_count(pc_init_poker)])

    # 首先判断牌面分数，有21的直接判定结果
    if score[0] == 21 or score[1] == 21:
        return who_win(score[0], score[1])
    else:
        while score[0] <= 21:
            get_new_poker = if_get_next_card()
            if get_new_poker:
                # 把新的扑克放到自己的手里
                your_hand_poker.append(get_new_poker)
                print("你手里的扑克牌是：{}".format(your_hand_poker))

                score[0] = score_count(your_hand_poker)
                # score 是否大于21
                if score[0] > 21:
                    print("手里的牌超过了21")
                    print("电脑手里的牌是{}".format(pc_hand_poker))
                    return who_win(score[0], score[1])
            elif get_new_poker == False:
                # 只要比玩家分数低就一直叫
                while score[1] < score[0]:
                    pc_poker = get_one_poker(rest_poker_list)
                    pc_hand_poker.append(pc_poker)

                    pc_score = score_count(pc_hand_poker)
                    score[1] = pc_score

                print("电脑手里的牌{}".format(pc_hand_poker))
                return who_win(score[0], score[1])
            else:
                continue


while True:
    input("Game begin, good luck. Press Y/N")
    print(f"Round {game_round}")
    random_card(poker_list)

    score = every_round(poker_list)

    total_score = np.add(total_score, score)
    print("Round over. You:{} : PC:{}".format(total_score[0], total_score[1]))

    game_round += 1
    continue_or_quit()
