import time
import os
import pathlib
from manifest_features import get_manifest_fetures
from smali_features import get_smali_features
from get_malware_to_csv import GetMalwareList


if __name__ == '__main__':
    start = time.clock()
    jobs = ['normal/', 'malware/']
    FeatureFile = './data/feature/all/'
    print("Get apps from %s." % FeatureFile)
    allCnt = len(os.listdir('../data/decompiled/' + jobs[0])) + len(os.listdir('../data/decompiled/' + jobs[1]))
    for job in jobs:
        # input apk dir
        # file_dir = './data/apk/original/' + job
        # output feature store in FeatureFile
        # FeatureFile = '.\\data\\feature\\all\\'
        # files = os.listdir(file_dir)
        files = os.listdir('../data/decompiled/' + job)
        for file in files:
            # processing apk is APK_FIle
            # APK_File = file_dir + file
            # bakAPK store in bak_APK_File
            # bak_APK_File = '.\\data\\apk\\baksmali\\' + job + file.split('.apk')[0]
            if pathlib.Path(FeatureFile + file.split('.apk')[0]).is_file():
                print('feature file exists!')
                continue
            # os.system('.\\apktool\\apktool.bat d -f ' + APK_File + ' -o ' + bak_APK_File)

            bak_APK_File = '../data/decompiled/' + job + file
            if not os.path.exists(bak_APK_File) or not os.path.exists(bak_APK_File + '/manifest.xml'):
                print("file not exists")
                continue
            # S1 S2 S3 S4
            required_permissions, hardware_components, intents, components = get_manifest_fetures(
                bak_APK_File + '/manifest.xml')
            # S5 S6 S7 S8
            used_permission, network_address, suspicious_apicall, restricted_apicall = \
                get_smali_features(bak_APK_File + '/smali', required_permissions)

            # write feature file
            with open(FeatureFile + file.split('.apk')[0], 'w') as f:
                for p in required_permissions:
                    f.write('RequiredPermission::' + str(p) + '\n')
                for p in hardware_components:
                    f.write('HardwareComponent::' + str(p) + '\n')
                for p in intents:
                    f.write('Intent::' + str(p) + '\n')

                kind_name = ['Activity::', 'Service::', 'ContentProvider::', 'BroadcastReceiver::']
                kind = [r'activity', r'service', r'provider', r'receiver']
                for index, item in enumerate(kind):
                    for p in components[item]:
                        f.write(str(kind_name[index]) + str(p) + '\n')

                for p in used_permission:
                    f.write('UsedPermission::' + str(p) + '\n')
                for p in network_address:
                    f.write('NetAddress::' + str(p) + '\n')
                for p in suspicious_apicall:
                    f.write('SuspiciousAPI::' + str(p) + '\n')
                for p in restricted_apicall:
                    f.write('RestrictedAPI::' + str(p) + '\n')

    elapsed = (time.clock() - start)
    print("Get features from %d apps... cost :%f s." % (allCnt, elapsed))

    # generate malware list
    GetMalwareList()
