def twoComplement(string):
    if(string[0] == '1'):
        imm = 65535 - int(string, 2) +1
        imm = -imm
    else:
        imm = int(string, 2)
    return imm
    
def outputs(reg, IC, MI,  mem, branch):
    print("===============REGISTER VALUE===============")
    r = 0
    c = 0
    n = 8
    while c < 4:
        if(c == 0):
            print("${} = {}     ${} = {}    ${} = {}     ${} = {}".format(n, reg[n], n+1, reg[n+1], n+2, reg[n+2], n+3, reg[n+3]))
        else:
            print("${} = {}     ${} = {}       ${} = {}     ${} = {}".format(n, reg[n], n+1, reg[n+1], n+2, reg[n+2], n+3, reg[n+3]))
        n = n + 4
        c = c + 1
     
    n = 0;
    c = 8192;
    print("===============MEMORY VALUE===============")
    while(n < 20):
        if (n < 18):
            print("[{}] = {}     [{}] = {}       [{}] = {}".format(hex(c), mem[n], hex(c + 4), mem[n + 1], hex(c + 8), mem[n + 2]))
            c = c + 12;
            n = n + 3;
        else:
            print("[{}] = {}     [{}] = {}       [{}] = {} ".format(hex(c), mem[n], hex(c + 4), mem[n + 1], hex(c + 8), mem[n + 2]))
            n = n + 2;
    print("===============STATISTICS===============")
    print("Instruction count = {}".format(IC))
    print("Memory Count = {}".format(MI) )
    print("Branch Count =  {}".format(branch))





def disassemble(instructions, debugMode): 
    PC = 0                          #keeps track of what line of of instrcution form the txt file is being run
    IC  = 0                            #kee[s track of instruction count and the program counter 
    branch = 0                             # branch counter
    MI = 0                                 #memory instruction counter

    finished = False                        #is the program finished?
    reg = [0]*24                            #declare register array all initialized to 0
    mem = [0]*21                    #memory from 0x2000 ot 0x2050
    fetch = instructions[PC]
    #for fetch in instructions:
    while(not finished):
        fetch = instructions[PC]
        s = int(fetch[6:11], 2)        #read in the register
        t = int(fetch[11:16], 2)        #read in ther other register
        d = int(fetch[16:21], 2)
        if(fetch == "00010000000000001111111111111111"):
            finished = True
            outputs(reg, IC, MI, mem, branch)
        if(fetch[0:6] == "001000"):             #addi
            reg[t] = reg[s] + twoComplement(str(fetch[16:33]))
            IC += 1
            PC +=1
            if(debugMode):
                print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    addi $" + str(t) + ",$" + str(s) + "," + str(twoComplement(str(fetch[16:32]))))
        elif(fetch[0:6] == "001111"):   #LUI
            reg[t] = reg[int(fetch[16:332],2)] << 16
            PC+=1
            IC+=1
        elif (fetch[0:6] == "001101"):           #ori
            reg[t] = reg[s] | int(fetch[16:32],2)
            PC +=1

            IC += 1
            if(debugMode):
                print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    ori $" + str(t) + ",$" + str(s) + "," + hex(int(fetch[16:32], 2)))
        elif(fetch[0:6] == "000000"):           # R-type registers
            if (fetch[26:32] == "101010"):      #SLT
                if(reg[s] < reg[t]):
                    reg[d] = 1
                else:
                    reg[d] = 0
                PC +=1

                IC += 1
                if(debugMode):
                    print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    slt $" + str(d) + ",$" + str(s) + ",$" + str(t))
            elif (fetch[26:32] == "100000"):      #add
                reg[d] = reg[s] + reg[t]
                PC +=1
                IC += 1

                if(debugMode):
                    print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    add $" + str(d) + ",$" + str(s) + ",$" + str(t))
            elif (fetch[26:32] == "100001"):      #addu
                reg[d] = reg[s] + reg[t]
                PC +=1
                IC += 1
                
                if(debugMode):
                    print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    addu $" + str(d) + ",$" + str(s) + ",$" + str(t))
            elif (fetch[26:32] == "100101"):           #or
                reg[t] = reg[s] | reg[t]
                PC +=1
                
                IC += 1
                if(debugMode):
                    print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    ori $" + str(t) + ",$" + str(s) + "," + hex(int(fetch[16:32], 2)))
            elif (fetch[26:32] == "100010"):      #SUB
                reg[d] = reg[s] - reg[t]
                PC +=1
                IC += 1
                if(debugMode):
                    print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    sub $" + str(d) + ",$" + str(s) + ",$" + str(t))
            elif(fetch[26:32] == "100110"):          #XOR
                reg[d] = reg[s]**reg[t]
                PC+= 1
            elif(fetch[26:32] == "100100"):       #AND
                reg[d] = reg[s] & reg[t]
                PC +=1
                IC += 1

                if(debugMode):
                    print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    and $" + str(d) + ",$" + str(s) + ",$" + str(t))
            elif(fetch[26:32] == "000000"):
                h = int(fetch[21:26], 2)            #SLL
                reg[d]  = reg[t] << h
                i = 0
                if(reg[d] > (2**31)-1):
                   while(reg[d] > 0 ):
                        reg[d] -= (2**(32+i))
                        i = i +1
                PC +=1
                IC += 1

                if(debugMode):
                    print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    slal $" + str(d) + ",$" + str(t) + ", " + str(h))  #SLL
               
            elif(fetch[26:32] == "000010"):         #SRL
                h = int(fetch[21:26], 2)         
                PC +=1
                IC += 1

                #if the value is negetive follow the opposite logic of SLL

                i = 0
                temp = reg[t]
                while(temp < 0):
                    temp += (2**(32+i))
                    i = i +1
                reg[d]  = temp >> h

                if(debugMode):
                    print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    srl $" + str(d) + ",$" + str(t) + ", " + str(h))
        elif(fetch[0:6] == "000100"):               #BEQ
            PC +=1
            IC += 1
            branch +=1
            if(reg[s] == reg[t]):
                if fetch[16] == '1':
                   offset = -( 65536 - int( fetch[16:32],2 ) )
                else: 
                    offset = int(fetch[17:33],2)
                PC = PC + offset
            if(debugMode):
                print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    beq $" + str(s) + ",$" + str(t) + "," + "skip")
        elif(fetch[0:6] == "000101"):               #BNE
            PC +=1
            IC += 1
            branch +=1
            if(reg[s] != reg[t]):
                if fetch[16] == '1':
                   offset = -( 65536 - int( fetch[16:32],2 ) )
                PC = PC + offset
            if(debugMode):
                print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    bne $" + str(s) + ",$" + str(t) + "," + "loop")
        elif(fetch[0:6] == "101011"):               #SW
            PC +=1
            IC += 1
            MI +=1
            offset = twoComplement(str(fetch[16:32]))
            if(offset >  0):
                if(offset >= int(8192)):
                    mem[int(reg[s]/4)+int((-int(8192)+ offset)/4)] = reg[t]
                else:
                    mem[reg[s]-int(8192)+ int(offset/4)] = reg[t]
            elif(offset == 0):
                 mem[int((reg[s]-int(8192))/4)] = reg[t]
            else:
                mem[int((reg[s]-int(8192) + offset)/4)] = reg[t]

            if(debugMode):
                print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    sw $" + str(t) + ",{}".format(offset) + "($" + str(s) + ")")
        elif(fetch[0:6] == "100011"):               #LW
            PC +=1
            IC += 1
            MI+=1
            offset = twoComplement(str(fetch[16:32]))
            if(offset < 0):
                reg[t] = mem[int((reg[s] - int(8192) + offset)/4)]
            else :
                if(offset > int(8192)):
                   reg[t] = mem[int((offset - int(8192))/4)+ int(reg[s]/4)]
                else:
                    reg[t] = mem[reg[s] - int(8192) + int(offset/4)]
            if(debugMode):
                print("IC = " + str(PC).zfill(2) + "  PC = " + str(PC*4).zfill(2) + ":    lw $" + str(t) + ",{}".format(offset) + "($" + str(s) + ")")
        else:
            print("This opcode is not valid: ", str(fetch[0:6]) )
            finished = True
            print("Done!!!!")


def main():
    openFile = str(input("Enter the name of the file with the extention .txt : "))
    inFile = open(openFile, "r")       #opens the file
    instructions = []                       #declares an array
    
    for line in inFile:
        if(line == "\n" or line[0] == '#'): 
            continue
        line = line.replace('\n', '')
        line = format(int(line, 16), "032b")    #formats tthe number as 32bits and uses 0 as filler
        instructions.append(line)   
    inFile.close()
    debugMode = int(input("1: Debug Mode \n0: Normal Mode : "))
    disassemble(instructions, debugMode)

main()
