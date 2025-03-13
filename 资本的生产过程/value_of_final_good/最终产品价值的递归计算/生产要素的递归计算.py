import pandas as pd


def search(good_before, goods_x):
    for good_current in goods_x:
        print(good_current)

        globals()["df_" + good_current] = pd.read_excel(
            good_current + "生产要素表.xlsx", index_col="生产要素")

        goods_next = globals()["df_" + good_current].query(
            "单价 == 'x'").index.tolist()

        if goods_next != []:
            print("Have other goods!\ngoods_next:", goods_next)
            search(good_current, goods_next)
        else:
            print("No other goods!")

        value = globals()["df_" + good_current]["数量"].dot(
            globals()["df_" + good_current]["单价"])

        if good_before != good_current:
            globals()["df_" + good_before].loc[good_current, '单价'] = value

        print(f"value of {good_current}: {value:.2f}")


good_before = "茶叶蛋"
goods_x = ["茶叶蛋"]
search(good_before, goods_x)
