def jiujiu():
    for i in range(1,10):

        for j in range(1,i+1):

             print('%s*%s=%s'%(j,i,j*i),end = '   ')
        print('')
if __name__ == '__main__':
    jiujiu()