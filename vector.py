import pandas as pd
import os
import random
import numpy


class App2Vector(object):
    def __init__(self):
        print('start to construct feature vectors for apps...')
        self.features = set()
        self.malware_set = set()
        # self.ignore_type = set(['url', 'activity'])
        self.contain_type = {'RequiredPermission', 'HardwareComponent', 'Intent', 'Activity',
                             'Service', 'ContentProvider', 'BroadcastReceiver', 'Activity', 'Service',
                             'ContentProvider', 'BroadcastReceiver'}
        self.feature_dict = dict()
        self.build_malware_set()

    def build_malware_set(self, path='./data/feature/malware_sha256.csv'):
        df = pd.read_csv(path)
        index_name = 'sha256'
        for i in df[index_name]:
            self.malware_set.add(i)
        # print("total %d malwares" % len(self.malware_set))

    def build_feature_dict(self, all_apps, path='./data/feature/all/'):
        """build dict"""
        # all_apps = os.listdir(path)
        print("=== step1: scan all apps to build feature_dict.")
        cnt = 0
        for app in all_apps:
            cnt += 1
            if cnt % 500 == 0:
                print("scan %d apps up to now..." % cnt)
            with open(path + app, 'r') as file:
                for line in file.readlines():
                    feature_type = line.split('::')[0]
                    # if feature_type not in self.ignore_type:
                    if feature_type in self.contain_type:
                        self.features.add(line)
        for feature in self.features:
            self.feature_dict[feature] = 0
        print("total %d apps used to build feature_dict" % cnt)
        print("%d-features will be extracted for every app" % len(self.features))

    def get_feature_vectors(self, all_apps, path='./data/feature/all/'):
        """change apps to express vectors"""
        print("=== step2: extracting features for apps.")
        ret_vectors = []
        # all_apps = os.listdir(path)
        # outfile = open('features.csv', 'w+')
        cnt = 0
        for app in all_apps:
            cnt += 1
            if cnt % 500 == 0:
                print("extracted features for  %d apps up to now..." % cnt)
            vector = self.feature_dict.copy()
            flag = 0
            if app in self.malware_set:
                flag = 1
            with open(path + app, 'r') as file:
                for line in file.readlines():
                    feature_type = line.split('::')[0]
                    if feature_type in self.contain_type:
                        vector[line] = 1
            ret_vectors.append([app, numpy.array(list(vector.values())), flag])
            # outfile.write(app+';'+str(list(vector.values()))+';%d\n' %flag)
        return ret_vectors


def get_malwares():
    df = pd.read_csv('./data/feature/malware_sha256.csv')
    index_name = 'sha256'
    malware_set = set()
    for i in df[index_name]:
        malware_set.add(i)
    return malware_set


def get_inputapps(path='./data/feature/all', threshold=100):
    malware_set = get_malwares()
    all_apps = os.listdir(path)
    random.shuffle(all_apps)
    list_malware = []
    list_bengin = []
    cnt_app = 0
    cnt_malware = 0
    cnt_benign = 0
    for app in all_apps:
        if app in malware_set:
            cnt_malware += 1
            if cnt_malware <= threshold:
                list_malware.append(app)
        else:
            cnt_benign += 1
            if cnt_benign <= threshold:
                list_bengin.append(app)
        cnt_app += 1
    input_apps = list_malware + list_bengin
    random.shuffle(input_apps)
    print("total scan %d apps: %d malwares and %d bengins" % (cnt_app, cnt_malware, cnt_benign))
    print("only %d apps will be used: %d malwares and %d bengins" % (len(input_apps), len(list_malware), len(list_bengin)))
    return input_apps


def getData(threshold=100):
    input_apps = get_inputapps(threshold=threshold)
    V = App2Vector()
    V.build_feature_dict(input_apps)
    result = V.get_feature_vectors(input_apps)
    index = []
    data = []
    label = []
    for item in result:
        index.append(item[0])
        data.append(item[1])
        label.append(item[2])
    data = numpy.array(data)
    label = numpy.array(label)
    train_data, train_label, test_data, test_label = (data[:int(round(0.8 * len(data)))], label[:int(round(0.8 * len(label)))],
                                                      data[int(round(0.8 * len(data))):], label[int(round(0.8 * len(label))):])
    print(train_data.shape, train_label.shape, test_data.shape, test_label.shape)
    return train_data, train_label, test_data, test_label


if __name__ == '__main__':
    train_data, train_label, test_data, test_label = getData()
    print(train_label)
    print(test_label)
