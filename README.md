# Drebin
python script to get apk features  

features based on Drebin  
1.get features from apk   
2.put features into vector   
3.use SVM to train and test  

Pscount function, get_permissions_and_API function and find_invoked_Android_APIs function conme from https://github.com/MLDroid/drebin  

usages:  
pip install -r requirements.txt  

put your apk in ./data/apk/original/normal and ./data/apk/original/malware  
the bakfile will be stored in ./data/apk/baksmali  
the features will be stored in ./data/feature/all/  
./data/feature/malware_sha256.csv shows malware apk file name  
 ![image](https://github.com/lightningwm/Drebin/blob/master/learning_process04092040.png)
