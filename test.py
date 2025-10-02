nums = [2, 3, 4, 5]
sum = 0
for num in nums:
    sum = sum + num
length = len(nums)

avg = sum/length

def avgfunc(nums):
    sum = 0

    for num in nums:
        sum = sum + num

    length = len(nums)

    avg = sum/length

    return avg

count = 0

while count < 3:

    count += 1

    print(count)
 