
with open("encrypted.txt", "r") as f:
    data = f.read()

test = """
<--------------GE2Q====----00110001 00110100-----<--------------GE2Q====----00110001 00110100-----<0a<-----GE2Q====--------------------<-----GE2Q====--------------------<0a<--------00110001 00110100-31 32----00110001 00110100----00110001 00110100--<--------00110001 00110100-31 32----00110001 00110100----00110001 00110100--<0a<--31 32-----------------------<--31 32-----------------------<0a<---------------------------<---------------------------<0a<---------------------------<---------------------------<0a<--------------GE2Q====----00110001 00110100-----<--------------GE2Q====----00110001 00110100-----<0a<-----GE2Q====--------------------<-----GE2Q====--------------------<0a<--------00110001 00110100-31 32----00110001 00110100----00110001 00110100--<--------00110001 00110100-31 32----00110001 00110100----00110001 00110100--<0a<--00110001 00110100-----------------------<--00110001 00110100-----------------------<0a<---------------------------<---------------------------<0a<---------------------------<---------------------------<0a<--------------GE2Q====----00110001 00110100-----<--------------GE2Q====----00110001 00110100-----<0a<-----GE2Q====--------------------<-----GE2Q====--------------------<0a<--31 32----00110001 00110100-31 32----00110001 00110100----00110001 00110100--<--31 32----00110001 00110100-31 32----00110001 00110100----00110001 00110100--<0a<---------------------------<---------------------------<0a<---------------------------<---------------------------<0a<---------------------------<---------------------------<0a<--------------GE2Q====----00110001 00110100-----<--------------GE2Q====----00110001 00110100-----<0a<-----GE2Q====--------------------<-----GE2Q====--------------------<0a<--------00110001 00110100-31 32----00110001 00110100----00110001 00110100--<--------00110001 00110100-31 32----00110001 00110100----00110001 00110100--<0a<--31 32-----------------------<--31 32-----------------------<0a<---------------------------<---------------------------<0a<---------------------------<---------------------------<
"""

test_len = len("<--------------GE2Q====----00110001 00110100-----")

for i in range(0, len(data), )
