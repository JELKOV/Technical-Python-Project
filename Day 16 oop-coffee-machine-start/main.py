from coffee_maker import CoffeeMaker
from menu import Menu
from money_machine import MoneyMachine

class CoffeeMachine:
    def __init__(self):
        # CoffeeMachine 클래스 초기화: Menu, CoffeeMaker, MoneyMachine 객체 생성
        self.menu = Menu()  # 음료 메뉴를 관리하는 객체
        self.coffee_maker = CoffeeMaker()  # 커피 머신의 자원과 음료 제조를 관리하는 객체
        self.money_machine = MoneyMachine()  # 결제를 관리하는 객체

    def run(self):
        # CoffeeMachine 작동 메서드: 사용자와의 상호작용을 처리하는 메인 루프
        is_running = True  # 머신 작동 여부를 제어하는 플래그
        while is_running:
            # 사용자에게 메뉴 옵션 표시
            options = self.menu.get_items()  # 메뉴에서 가능한 음료 리스트 가져오기
            choice = input(f"What would you like? ({options}): ").lower()  # 사용자 입력 받기

            if choice == "off":
                # "off" 입력 시 머신 종료
                is_running = False
                print("Turning off the coffee machine. Goodbye!")  # 종료 메시지 출력
            elif choice == "report":
                # "report" 입력 시 현재 자원 및 수익 보고
                self.coffee_maker.report()  # 자원 상태 출력
                self.money_machine.report()  # 수익 상태 출력
            else:
                # 음료 선택 처리
                drink = self.menu.find_drink(choice)  # 선택한 음료를 메뉴에서 검색
                if drink:
                    # 선택한 음료가 메뉴에 있을 경우 처리
                    if self.coffee_maker.is_resource_sufficient(drink):
                        # 자원이 충분한지 확인
                        if self.money_machine.make_payment(drink.cost):
                            # 결제가 성공하면 음료 제조
                            self.coffee_maker.make_coffee(drink)

if __name__ == "__main__":
    # 프로그램 시작점
    coffee_machine = CoffeeMachine()  # CoffeeMachine 객체 생성
    coffee_machine.run()  # CoffeeMachine 실행
