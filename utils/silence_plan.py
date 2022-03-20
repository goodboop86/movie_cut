from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = [20, 2]


def remove_short_detect(current_list, th=3):
    new_list = []
    print(len(new_list))
    popped = False

    for idx in range(len(current_list)):
        start, end, duration = current_list[idx]

        if popped:
            popped = False
            print(" -> passed : {}".format(current_list[idx]))
            continue

        if idx+1 >= len(current_list):
            new_list.append([start, end, duration])
            continue
        else:
            n_start, n_end, n_duration = current_list[idx + 1]

        # 無音区間の間の有音区間がth[s]未満の場合は無音区間をつなげる。
        if (n_start - end) < th:
            new_list.append([start, n_end, n_end - start])
            print(" -> update from : {} ~ {}".format(current_list[idx], current_list[idx + 1]))
            print(" ->              to : {}".format([start, n_end, n_end - start]))
            popped = True
        else:
            new_list.append([start, end, duration])
    return new_list


def main(**kwargs):
    with open(kwargs['silence_file']) as f:
        silence = f.readlines()
    silence_list = []

    for line in silence:
        end, duration = line.split(' ')
        elem = [float(end) - float(duration), float(end), float(duration)]
        silence_list.append(elem)

    # 更新前の無音発生区間
    x, y = [], []

    for line in silence_list:
        if line[0] > 1:
            x.append(line[0] - 0.0000001)
            y.append(0)
            x.append(line[0])
            y.append(1)
            x.append(line[1])
            y.append(1)
            x.append(line[1] + 0.0000001)
            y.append(0)

    # 無音発生時:1
    plt.clf()
    plt.plot(x, y)
    plt.fill_between(x, y, alpha=0.5)
    plt.savefig(kwargs['before_file'])

    new_silence_list = remove_short_detect(silence_list, th=kwargs['noise_second'])

    new_x = []
    new_y = []
    for line in new_silence_list:
        if line[0] > 1:
            new_x.append(line[0] - 0.0000001)
            new_y.append(0)
            new_x.append(line[0])
            new_y.append(1)
            new_x.append(line[1])
            new_y.append(1)
            new_x.append(line[1] + 0.0000001)
            new_y.append(0)

    # 無音発生時:1
    plt.clf()
    plt.plot(new_x, new_y)
    plt.fill_between(new_x, new_y, alpha=0.5)
    plt.savefig(kwargs['after_file'])

    with open(kwargs['out_file'], "w", newline='\n') as f:
        f.writelines(["{}\n".format(" ".join(map(str, line[1:]))) for line in new_silence_list])
