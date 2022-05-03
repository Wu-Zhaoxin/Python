import asyncio
import time


# async def fun1():
#     time.sleep(3)
#     print("1")
#
#
# async def fun2():
#     time.sleep(3)
#     print("2")
#
#
# async def fun3():
#     time.sleep(3)
#     print("3")
#
#
# if __name__ == "__main__":
#     f1 = fun1()
#     f2 = fun2()
#     f3 = fun3()
#     tasks = [f1, f2, f3]
#     t1 = time.time()
#     asyncio.run(asyncio.wait(tasks))
#     t2 = time.time()
#     print(t2 - t1)

def fun1():
    time.sleep(3)
    print("1")


def fun2():
    time.sleep(3)
    print("2")


def fun3():
    time.sleep(3)
    print("3")


if __name__ == "__main__":
    t1 = time.time()
    fun1()
    fun2()
    fun3()
    t2 = time.time()
    print(t2 - t1)