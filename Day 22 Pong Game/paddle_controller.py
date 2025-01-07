from turtle import Screen
from paddle import Paddle

class PaddleController:
    """
    PaddleController 클래스는 Paddle의 움직임과 키 입력 로직을 관리합니다.
    """

    def __init__(self, screen: Screen, paddle: Paddle, up_key: str, down_key: str):
        """
        PaddleController 초기화 메서드.

        Args:
            screen (Screen): Turtle 화면 객체.
            paddle (Paddle): Paddle 객체.
            up_key (str): Paddle을 위로 움직이는 키.
            down_key (str): Paddle을 아래로 움직이는 키.
        """
        self.screen = screen
        self.paddle = paddle
        self.keys_pressed = {up_key: False, down_key: False}  # 키 입력 상태 추적.
        self.up_key = up_key
        self.down_key = down_key

        # 위/아래 키에 대한 키 입력 및 키 해제 이벤트 설정.
        self.screen.listen()
        self.screen.onkeypress(lambda: self.press_key(up_key), up_key)
        self.screen.onkeyrelease(lambda: self.release_key(up_key), up_key)
        self.screen.onkeypress(lambda: self.press_key(down_key), down_key)
        self.screen.onkeyrelease(lambda: self.release_key(down_key), down_key)

    def press_key(self, key):
        """
        키 입력 이벤트를 처리하는 메서드.

        Args:
            key (str): 입력된 키.
        """
        self.keys_pressed[key] = True  # 해당 키를 '입력됨'으로 설정.

    def release_key(self, key):
        """
        키 해제 이벤트를 처리하는 메서드.

        Args:
            key (str): 해제된 키.
        """
        self.keys_pressed[key] = False  # 해당 키를 '해제됨'으로 설정.

    def move(self):
        """
        현재 키 입력 상태에 따라 Paddle을 이동합니다.
        """
        if self.keys_pressed[self.up_key]:  # 위쪽 키가 입력되었으면 Paddle을 위로 이동.
            self.paddle.go_up()
        if self.keys_pressed[self.down_key]:  # 아래쪽 키가 입력되었으면 Paddle을 아래로 이동.
            self.paddle.go_down()
