# EasyExcelComparetool
**注意事项：简单对比脚本只能用于Excel表格里拥有表头的标准表格类数据**

主要是利用pandas的merge函数进行Excel表格的对比，函数返回一个表格，dataframe，下面描述即将使用到的参数。

>pandas.merge(left, right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True, indicator=False, validate=None)

1. left和right都是传进去的表格参数，在这个情况下是两个需要对比的Excel表格，脚本中默认left为新的数据，right为更旧的数据；
2. how是指合并的方法，并没有仔细研究各种合并方法的区别，但查询资料是跟数据库合并表格的方法类似，这里使用'outer'；
3. on是指两个表格都需要拥有的一列数据，用于进行合并和比较的标杆列；
4. suffixes是指当两个表格合并拥有相同名字的列A的时候，给left和right表格上分别加的后缀('_x', '_y')；
5. indicator为true表示合并后会多出一列'merge'列，默认值是:'left_only','right_only','both'；传字符串则这一列的名字为传入的字符串。

参考:https://github.com/pretoriusdre/similarpanda.git