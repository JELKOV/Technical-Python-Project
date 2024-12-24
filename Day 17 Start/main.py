"""
클래스
1. 들여쓰기
2. 대문자 표기법 (Pascal Case)
"""
class User:
    def __init__(self, user_id, user_name):
        print("init 함수 실행")
        self.id = user_id
        self.name =user_name
        self.followers = 0
        self.following = 0
    
    # (user) 팔로우를 하는 사람
    def follow(self, user):
        user.followers += 1 
        self.following += 1

user_1 = User("002", "jaehoho") # 객체 초기화
# user_1.id = "001"
# user_1.name = "jaehoahn"

print(user_1.followers)
print(user_1.name)

user_2 = User("003", "suyeonyeon")
# user_2.id = "002"
# user_2.name = "suyeonoh"

print(user_2.name)

user_1.follow(user_2)
print(user_1.followers)
print(user_1.following)
print(user_2.followers)


"""
클래스 속성만들기
클래스 변수들을 매번 재 사용해서 만드는건 정말 어리석은 짓 

객체 초기화를 해줘야 한다.
원하는 만큼 매개변수를 추가할수 있다.
class Car:
    def __init__(self, seats): 
        self.seats = seats
"""
