MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,  # 필요한 물 양 (ml)
            "coffee": 18,  # 필요한 커피 양 (g)
        },
        "cost": 1.5,  # 가격 ($)
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,  # 필요한 우유 양 (ml)
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

# 수익 초기화
profit = 0

# 머신의 현재 재료 상태
resources = {
    "water": 300,  # 물의 초기 양 (ml)
    "milk": 200,  # 우유의 초기 양 (ml)
    "coffee": 100,  # 커피의 초기 양 (g)
}


# Todo 4: 자원 확인
# Todo 4-1:  음료의 필요 자원을 확인하여 충분한 자원이 있는지 체크합니다.
# Todo 4-2: 자원이 부족할 경우 적절한 메시지를 출력합니다.
def resource_check(order_ingredients):
    for ingredient in order_ingredients:
        if order_ingredients[ingredient] > resources[ingredient]:
            print(f"No Resource: {ingredient}")
            return False
    return True

#Todo 5: 동전 처리
#Todo 5-1: 사용자가 동전을 입력하면 총 금액을 계산합니다.
#Todo 5-2: 동전 금액 계산 로직 구현.
def coin_process ():
    print("Input your coin")
    total = int(input("how many quarters?: ")) * 0.25
    total += int(input("how many dimes?: ")) * 0.1
    total += int(input("how many nickles?: ")) * 0.05
    total += int(input("how many pennies?: ")) * 0.01
    return total


# Todo 6: 거래 성공 여부 확인
# Todo 6-1: 투입된 돈이 음료 가격보다 큰지 확인합니다.

# Todo 6-2: 금액이 부족하면 거래를 취소하고 돈을 반환합니다.
# Todo 6-3: 금액이 충분하면 음료 가격을 수익에 추가하고, 잔돈을 계산하여 반환합니다.
def check_coin(input_coin, drink_price):
    if input_coin >= drink_price:
        change_money = round(input_coin - drink_price, 2)
        print(f"Change_Money is : {change_money}")
        global profit
        profit += drink_price
        return True
    else:
        print(f"Not Enough Money : {drink_price-input_coin}")
        return False

#Todo 7: 커피 제조
def make_coffee(drink_name, order_ingredients):
    """자원을 차감하고 음료 제공"""
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]  # TODO 7-1: 자원 차감
    print(f"Here is your {drink_name} ☕️. Enjoy!")  # TODO 7-2: 음료 제공 메시지

is_working = True

while is_working:
    #Todo 1 : 사용자 입력 처리
    user_order = input("What would you like? (espresso/latte/cappuccino):" ).lower()
    #Todo 1-1 :  사용자 입력을 처리하여 메뉴 옵션 선택 (espresso/latte/cappuccino).
    # Todo 1-2 : 각 작업(음료 제공 또는 명령 실행) 후 입력 메시지를 반복적으로 표시.

    #Todo 2 : 커피 머신 종료
    #Todo 2-1 : 사용자가 "off"를 입력하면 프로그램을 종료합니다.
    if user_order == "off":
        is_working = False
    #Todo 3 : 리포트 출력
    #Todo 3-1 : "report" 명령 처리.
    #Todo 3-2 : 현재 자원 상태를 출력합니다.
    elif user_order == "report":
        print(f"Water: {resources['water']}ml")
        print(f"Milk: {resources['milk']}ml")
        print(f"Coffee: {resources['coffee']}ml")
        print(f"profit: {profit}")
    else:
        drink = MENU.get(user_order)
        if drink and resource_check(drink["ingredients"]):
            payment = coin_process()
            if check_coin(payment, drink["cost"]):
                make_coffee(user_order, drink["ingredients"])
        else:
            print("Invalid choice. Please select a valid drink.")