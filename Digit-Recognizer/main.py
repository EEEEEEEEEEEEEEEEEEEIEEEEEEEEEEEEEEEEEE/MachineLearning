#!/usr/bin/env python
# coding:utf-8

from PIL import Image
import sys
import os
import random
import time

def build_image(data, width, height):
    Im = Image.new("L", (28,28), 0)
    for i in xrange(width):
        for j in xrange(height):
            pixel = data[j * width + i]
            Im.putpixel((i, j), pixel)
    Im.show()


train_data = []
label = []
test_data = []

def init_test_data():
    global test_data
    with open("./test.csv", "r") as f:
        head = f.readline()
        for content in f:
            data = [int(i) for i in [i for i in content.split(",")]]
            test_data.append(data)

def init():
    global train_data
    global label
    with open("./train.csv", "r") as f:
        head = f.readline()
        for content in f:
            data = [int(i) for i in [i for i in content.split(",")]]
            correct = data[0]
            # print "[+] Corrent : [%d]" % (correct)
            data = data[1:]
            # print "[+] Data length : [%d]" % (len(data))
            width = 28
            height = 28
            # add to train data
            train_data.append(data)
            # add to label
            label.append(correct)

def get_distance(pointA, pointB):
    length = len(pointA)
    total = 0
    for i in xrange(length):
        total += (pointA[i] - pointB[i]) ** 2
    return total ** 0.5

def clear_screen():
    os.system("clear")

'''
def guess(data, k):
    distances = []
    index = 0
    for i in train_data:
        # sys.stdout.write("[+] %d / %d\r" % (index + 1, len(train_data)))
        # sys.stdout.flush()
        distance = get_distance(data, i)
        distances.append((index, distance))
        index += 1
    #print ""
    #print "[+] Cacl finished!"
    #print "[+] Sorting..."
    distances = sorted(distances, key = lambda i:i[1])
    #print "[+] Sorted"
    results = []
    for i in distances[0:k]:
        result = label[i[0]]
        distance = i[1]
        results.append(result)
        #print "[!] Distance : [%d] Result : [%d]" % (distance, result)
    return get_frequently(results)
'''


def guess(data, k):
    # print_data(data, 28, 28)
    distances = []
    index = 0
    min_distance = get_distance(data, train_data[0])
    min_index = 0
    for i in train_data[1:]:
        # sys.stdout.write("[+] %d / %d\r" % (index + 1, len(train_data)))
        # sys.stdout.flush()
        distance = get_distance(data, i)
        if distance < min_distance:
            min_distance = distance
            # print "[+] Flushing min distance : [%d]" % (min_distance)
            min_index = index
        index += 1
    return label[min_index + 1]

def get_frequently(words):
    dict_num = list((i,words.count(i)) for i in set(words))
    return sorted(dict_num, key = lambda i:i[1])[::-1][0][0]


def print_data(data, width, height):
    for i in xrange(width):
        for j in xrange(height):
            if data[i * width + j] > 0:
                sys.stdout.write("*")
                sys.stdout.flush()
            else:
                sys.stdout.write(" ")
                sys.stdout.flush()
        sys.stdout.write("\n")
        sys.stdout.flush()

def print_time():
    print "[+] Now time : [%s]" % (time.strftime('%H:%M:%S',time.localtime(time.time())))
    return time.time()

def get_line_number(filename):
    with open(filename, "r") as f:
        return len(list(f))

def main():
    print_time()
    print "[+] Initing train data..."
    init()
    print "[+] Train data : [%d]" % (len(train_data))
    print "[+] Initing test data..."
    init_test_data()
    print "[+] Test data : [%d]" % (len(test_data))
    print "[+] Testing"
    output = open("result.csv", "a+")
    total = len(test_data)
    print_time()
    start_time = time.time()

    start_index = get_line_number("./result.csv") - 1
    print "[+] 上次运行到第 %d 个数据 , 正在恢复..." % (start_index)
    index = start_index

    for i in test_data[start_index:]:
        index += 1
        print "=" * 32
        print "[!] ( %d / %d ) = ( %f %%)" % (index, total, ((index * 1.0) / (total)) * 100.0)
        # print_data(i, 28, 28)
        result = guess(i, 10)
        print "[+] Result = %d" % (result)
        output.write("%d,%d\n" % (index, result))
        output.flush()
        cost_time = print_time() - start_time
        total_time = (total / index) * cost_time
        print "[+] 预计总花费时间 : [%d] min" % (total_time / 60)
        end_time = start_time + total_time
        print "[+] 预计结束时间 : [%s]" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(end_time)))
    output.close()


def test_print_data():
    with open("./test.csv", "r") as f:
        head = f.readline()
        content = f.readline()
        data = [int(i) for i in [i for i in content.split(",")]]
        return data

if __name__ == "__main__":
    main()
