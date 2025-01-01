from scipy.constants import carat


class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def breath(self):
        print("inhale, exhale")


class Dog(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)

    def breath(self):
        super().breath()  # 상위 클래스 메서드 호출
        print("Dog-specific breathing method!")


cat = Animal("cat", 20)
baduk = Dog("Baduk", 20)

cat.breath()      # 출력: inhale, exhale
baduk.breath()    # 출력: inhale, exhale
                  #        Dog-specific breathing method!
