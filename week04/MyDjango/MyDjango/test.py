class A:
    def a(self):
        print('a')

class B(A):
    def foo(self):
        super().a()
    def a(self):
        print('b')


class C(B):
    pass

if __name__ == '__main__':
    c = C()
    c.foo()