import os

path = 'K:/bbc'
listd = os.listdir(path)
for val, paths in enumerate(listd):
    subdir = path+'/'+paths
    for files in os.listdir(subdir):
        os.chdir(subdir)
        os.rename(files, files[0:files.index('.')]+'_'+str(val+1)+'.txt')
