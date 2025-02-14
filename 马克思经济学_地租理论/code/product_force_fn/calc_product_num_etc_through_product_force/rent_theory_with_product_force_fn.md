参数：

土地等级（取决于生产力函数）

土地面积

单位面积投资（总投资）

平均利润率

供需关系（决定生产价格）

这里需要得出的结果：

生产价格，产量（总产量），利润，地租……

---

特殊的地方：

其他条件缺省情况下，改变投资额，会引起什么变化。

投资额会影响的主要因素：

1. 产量

2. 实际面积

3. ……

---

新建与追加，替代关系。

---

对相关函数图像，提示一点小秘密：

小农业的精耕细作与大农业的集约生产。等产量线。地租导致的轻土地、重资本的投资倾向。

---

单一土地情况：

单位面积产量：

$$ln(\frac{investment\_sum}{area\_sum})$$

总产量：
$$ln(\frac{investment\_sum}{area\_sum}) \times area$$

总产值：

$$ln(\frac{investment\_sum}{area\_sum}) \times area \times product\_price$$

毛利润：

$$ln(\frac{investment\_sum}{area\_sum}) \times area \times product\_price - investment$$

毛利润率：

$$\frac{ln(\frac{investment\_sum}{area\_sum}) \times area \times product\_price - investment}{investment}$$

超额利润：

$$ln(\frac{investment\_sum}{area\_sum}) \times area \times product\_price - investment * (1.0 + profit\_rate\_avg)$$

超额利润率：

$$\frac{ln(\frac{investment\_sum}{area\_sum}) \times area \times product\_price - investment * (1.0 + profit\_rate\_avg)}{investment}$$

多级土地情况：

总产量：

$$\sum_{0}^{i} pf_i(investment, area) \cdot area_i$$
总产值：

$$\sum_{0}^{i} pf_i(investment, area) \cdot area_i \cdot product\_price$$

毛利润：

$$\sum_{0}^{i} (pf_i(investment, area) \cdot area_i \cdot product\_price - investment_i)$$

平均毛利润率：

$$\frac{\sum_{0}^{i} (pf_i(investment, area) \cdot area_i \cdot product\_price - investment_i)}{\sum_{0}^{i}investment_i}$$

超额利润：

$$\sum_{0}^{i} (pf_i(investment, area) \cdot area_i \cdot product\_price - investment_i \cdot (1.0 + profit\_rate\_avg))$$

平均超额利润率：

$$\frac{\sum_{0}^{i} (pf_i(investment, area) \cdot area_i \cdot product\_price - investment_i \cdot (1.0 + profit\_rate\_avg))}{\sum_{0}^{i}investment_i}$$
平均地租率：

$$\frac{\sum_{0}^{i} (pf_i(investment, area) \cdot area_i \cdot product\_price - investment_i \cdot (1.0 + profit\_rate\_avg)) \cdot transform\_rate\_sr}{\sum_{0}^{i}investment_i}$$

其中，生产力函数形如：

$$pf_i(investment, area) = ln(\frac{investment}{area})$$
