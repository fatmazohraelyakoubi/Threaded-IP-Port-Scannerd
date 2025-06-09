import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor
import threading
import time
from colorama import Fore ,init
init()


threading_look=threading.Lock()
 
def scan_ip(ip,start_port,end_port,file,error_file):
    try:
        try:
           hostname=socket.gethostbyaddr(str(ip))[0]
        except :
            with threading_look:
             hostname =Fore.BLUE+f"Unknown"
             hostname_error=Fore.RED + f"! Failled to resolve hostname for {ip} \n"
             print(f"{hostname_error}")
             error_file.write(hostname_error)  

               

        for i in range (start_port,end_port+1):
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result=sock.connect_ex((str(ip),i))
           
            if result==0:
                 result_msg=Fore.GREEN +f'[+] Online {ip}  port {i} is OPEN  Hostname:{hostname} \n'
            else:   
                 result_msg=Fore.RED+ f'[-] No Response  {ip}  port {i} is CLOSE Hostname:{hostname} \n'
                 
            sock.close()   

            with threading_look:
              print(f"{result_msg.strip()} \n")
              file.write(result_msg)
            
                 
    except Exception as e:
       with threading_look: 
         error_msg=Fore.RED+f"Error Scanning {ip}:{e} \n"
         print(f"{error_msg}")
         error_file.write(error_msg)
    


subnet_input=str(input(Fore.LIGHTMAGENTA_EX+f"Enter your subnet:"))
full_scan=input(Fore.LIGHTMAGENTA_EX+f"do you want to scan the full Subnet Y/N ?")
network=ipaddress.ip_network(subnet_input,strict=False)
if subnet_input=="y":
   IPs = list(network.hosts())
else:
  count=int(input(Fore.LIGHTMAGENTA_EX+f"Enter How many hosts you want to scan:"))
  IPs=list(network.hosts())[:count]




start_port=int(input(Fore.LIGHTMAGENTA_EX+f"Enter Start Port:"))
end_port=int(input(Fore.LIGHTMAGENTA_EX+f"Enter End Port:"))

if network.num_addresses>200:
    print(Fore.CYAN+f'Warning Lagre Subnet,This may take a while...')



with open("result.txt","w") as f: 
  with open("error.log","w") as Er: 
    start_time=time.time()  
    with ThreadPoolExecutor (max_workers=100) as executer:
      for ip in IPs:
          executer.submit(scan_ip, ip, start_port, end_port,f,Er)
end_time=time.time()
total_time=round(end_time-start_time,2)
print(Fore.BLUE+f"Scan time  {total_time} seconds")
print(Fore.YELLOW+f"total IPs scaned {len(IPs)}")       
       
              

