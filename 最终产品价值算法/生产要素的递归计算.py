import pandas as pd


def search(good_before, goods_x):
    for good in goods_x:  # traversal all goods in this list
        print(good)  # this is the good now.
        filePath = good + "生产要素表.xlsx"
        globals()["df_" + good] = pd.read_excel(filePath, index_col="生产要素")
        goods_next = globals()["df_" + good].query("单价 == 'x'").index.tolist()

        if goods_next != []:
            print("Have other goods!")
            print("goods_next:", goods_next)
            search(good, goods_next)
        else:
            print("No other goods!")

        numbers = globals()["df_" + good]["数量"]
        values = globals()["df_" + good]["单价"]
        value = numbers.dot(values)
        if good_before != good:
            globals()["df_" + good_before].loc[good, '单价'] = value

        print("\n", good, globals()["df_" + good])
        print("value:", value)


good_before = "茶叶蛋"  # string
goods_x = ["茶叶蛋"]  # list
search(good_before, goods_x)
