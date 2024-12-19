# import another_module
#
# print(another_module.another_variable)
#
# from turtle import Turtle, Screen
#
# ahn = Turtle()
# print(ahn)
# ahn.shape("turtle")
# # 펜 색상과 채우기 색상 모두 설정
# ahn.color("black", "DarkGrey")
# ahn.forward(100)
# ahn.begin_fill()
# ahn.circle(50)  # 반지름 50인 원을 그림
# ahn.end_fill()  # 내부를 채움
#
#
# my_screen = Screen()
# print(my_screen.canvheight)
# my_screen.exitonclick()

# from prettytable import PrettyTable
#
# table = PrettyTable()
# table.add_column("Pokemon Name",["Pikachu", "Squirtle","Charmander"])
# table.add_column("Type", ["Electric", "Water", "Fire"])
# table.align = "l"
# print(table)

import random
from prettytable import PrettyTable

# 포켓몬 데이터
pokemon_list = [
    {"name": "피카츄", "type": "전기", "cp": 120},
    {"name": "꼬부기", "type": "물", "cp": 100},
    {"name": "파이리", "type": "불", "cp": 130},
    {"name": "이상해씨", "type": "풀", "cp": 90},
    {"name": "푸린", "type": "요정", "cp": 80},
]

# 플레이어 상태
player = {
    "pokeballs": 5,
    "caught_pokemon": []
}


def display_pokemon_table():
    """포켓몬 목록 출력"""
    table = PrettyTable()
    table.add_column("포켓몬 이름", [p["name"] for p in pokemon_list])
    table.add_column("타입", [p["type"] for p in pokemon_list])
    table.add_column("CP", [p["cp"] for p in pokemon_list])
    table.align = "l"
    print(table)


def spawn_pokemon():
    """랜덤 포켓몬 생성"""
    return random.choice(pokemon_list)


def catch_pokemon(pokemon):
    """포켓몬 잡기"""
    print(f"야생 {pokemon['name']}이(가) 나타났다! 타입: {pokemon['type']}, CP: {pokemon['cp']}")

    # 잡을 확률 계산
    catch_rate = 50 - (pokemon["cp"] // 10)  # 높은 CP일수록 잡기 어려움
    chance = random.randint(1, 100)

    if chance <= catch_rate:
        print(f"{pokemon['name']}을(를) 잡았다!")
        player["caught_pokemon"].append(pokemon)
        return True
    else:
        print(f"{pokemon['name']}이(가) 도망쳤다!")
        return False


def play_game():
    """게임 루프"""
    print("포켓몬 잡기 게임에 오신 것을 환영합니다!")
    display_pokemon_table()

    while player["pokeballs"] > 0:
        print(f"\n남은 몬스터볼: {player['pokeballs']}개")

        # 포켓몬 생성
        wild_pokemon = spawn_pokemon()

        # 포켓몬 잡기 시도
        action = input(f"{wild_pokemon['name']}을(를) 잡으시겠습니까? (예/아니오): ").lower()
        if action == "예":
            player["pokeballs"] -= 1
            success = catch_pokemon(wild_pokemon)
            if success:
                continue
        elif action == "아니오":
            print(f"{wild_pokemon['name']}을(를) 무시했습니다.")
        else:
            print("잘못된 입력입니다. 턴을 건너뜁니다.")

        # 몬스터볼이 다 떨어지면 게임 종료
        if player["pokeballs"] == 0:
            print("\n몬스터볼이 모두 소진되었습니다! 게임 종료.")
            break

    # 결과 출력
    print("\n게임 종료! 잡은 포켓몬 목록:")
    if player["caught_pokemon"]:
        caught_table = PrettyTable()
        caught_table.add_column("포켓몬 이름", [p["name"] for p in player["caught_pokemon"]])
        caught_table.add_column("타입", [p["type"] for p in player["caught_pokemon"]])
        caught_table.add_column("CP", [p["cp"] for p in player["caught_pokemon"]])
        print(caught_table)
    else:
        print("아무 포켓몬도 잡지 못했습니다. 다음 기회에 도전하세요!")


# 게임 실행
play_game()
