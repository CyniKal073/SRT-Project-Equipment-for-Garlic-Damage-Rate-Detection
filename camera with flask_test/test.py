try:
    fd=open('C:/Users/admin/Desktop/666.txt','+r')
except FileNotFoundError:
    fd=open('C:/Users/admin/Desktop/666.txt','x')
try:
    line=fd.read()
except:
    line=''
fd.write('%s六百六十六\n'%line)

fd.close()