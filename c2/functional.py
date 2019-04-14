input_list = [11, 2, 12, 15, 5, 10, 7, 14, 6, 9, 1, 3, 13, 8, 4]
print('输入：%s\n' % input_list)

output_list = []
for i in input_list:
    if i % 2 == 0 or i % 3 != 0:
        if i > 10:
            output_list.append('%d: 大于10！' % i)
        else:
            output_list.append('%d: 小于等于10！' % i)
for s in output_list:
    print(s)


print('\n---------------------------------\n')

output = map(
    lambda x: '%d: 大于10！' % x if x > 10 else '%d: 小于等于10！' % x,
    filter(
        lambda x: x % 2 == 0 or x % 3 != 0,
        sorted(input_list),
    )
)
for s in output:
    print(s)


