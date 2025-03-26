#single port numberr
import socket
import threading

def scanport(ip,port):
    s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    s.settimeout(1)

    result=s.connect_ex((ip,port))

    if result==0:
        print(f"port {port} is open")

    else:
        print(f"port {port}is closed")

    

    
    s.close()    


def scanport_numbers(ip,startpoint,endpoint):

    a=[]


    for i in range(startpoint,endpoint):

        thread =threading.Thread(target=scanport,args=(ip,i))

        thread.start()

        a.append(thread)


    for i in range(startpoint,endpoint):

        thread.join()


    






scanport("google.com",4000)
scanport_numbers("google.com",1,100)
