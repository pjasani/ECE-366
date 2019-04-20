
def display (mem, reg, line, MI, branch, DIC):
    outFile = open("p3_g_15_prpg_sim_out_79.txt", "w")
    outFile.write("\n===================REGISTER VALUE===================")
    n = 0
    while(n < 9):
        outFile.write("\n${: <2} = {: <3}         ${: <2} = {: <3}            ${: <2} = {: <3}".format(n, reg[n], n+1, reg[n+1], n+2, reg[n+2]))
        n += 3

    outFile.write("\n====================MEMORY VALUE=====================")
    n= 0
    while(n < 48):
        outFile.write("\nM[{:<2}] = {:<3}         M[{:<2}] = {:<3}            M[{:<2}] = {:<3}".format(n, mem[n], n+1, mem[n+1], n+2, mem[n+2]))
        n += 3
    outFile.write("\nM[{:<2}] = {:<3}".format(48, mem[48]))

    outFile.write("\n=====================STATISTICS======================")
    outFile.write("\nDynamic Instruction count = {: <3}".format(DIC))
    outFile.write("\nProgram Count = {: <3}".format(line*4))
    outFile.write("\nMemory Count = {: <3}".format(MI) )
    outFile.write("\nBranch Count =  {: <3}".format(branch))
    outFile.close()

    print("=================REGISTER VALUE=================")
    n = 0
    while(n < 9):
        print("${: <2} = {: <3}         ${: <2} = {: <3}            ${: <2} = {: <3}".format(n, reg[n], n+1, reg[n+1], n+2, reg[n+2]))
        n += 3

    print("==================MEMORY VALUE===================")
    n= 0
    while(n < 48):
        print("M[{:<2}] = {:<3}         M[{:<2}] = {:<3}            M[{:<2}] = {:<3}".format(n, mem[n], n+1, mem[n+1], n+2, mem[n+2]))
        n += 3
    print("M[{:<2}] = {:<3}".format(48, mem[48]))

    print("===================STATISTICS====================")
    print("Instruction count = {}".format(DIC))
    print("Program Count = {}".format(line*4))
    print("Memory Count = {}".format(MI) )
    print("Branch Count =  {}".format(branch))
    

def disassemble(instructions, debugMode): 
    branch = 0                             # branch counter
    DIC = 0                                 #Dynamic Instructin Count
    MI = 0                                 #memory instruction counter
    line = 0                               #keeps track of what line of of instrcution from the txt file is being run

    finished = False                       #is the program finished?
    reg = [0]*15                           #declare register array all initialized to 0
    mem = [0]*49                           #declares mem array all initialized to 49
    fetch = instructions[line]             #for fetch in instructions:
    while(not finished):
        fetch = instructions[line]
        if(fetch[0:4] == "1111"):
            finished = True
            display(mem, reg, line, MI, branch, DIC)
        elif(fetch[0:4] == "0000"):     #SW
            Rx = reg[int(fetch[4:8],2)]
            mem[8+Rx] = reg[0] 
            line += 1
            MI += 1
            DIC +=1
            if(debugMode):
                print("IC = " + str(DIC).zfill(2) +":      sw $" + str(int(fetch[4:8],2)) + " =>  " + "mem[8+" + str(reg[int(fetch[4:8],2)]) + "]" +  " = $0")
        elif(fetch[0:4] == "0001"):     #LW
            reg[2] = mem[8+reg[int(fetch[4:8],2)]]
            line += 1
            MI +=1
            DIC +=1
            if(debugMode):
                print("IC = " + str(DIC).zfill(2) +":      lw $" + str(int(fetch[4:8],2)) + " =>  "+ "$2 = " +  "mem[8+" + str(reg[int(fetch[4:8],2)]) + "]")
        elif(fetch[0:4] == "0010"):     #addi
            Rx  = int(fetch[4:7],2)
            if(fetch[7:8] == "1"):
                imm = 1
            else:
                imm = 0
            reg[Rx] = reg[Rx] + imm
            line += 1
            DIC +=1
            if(debugMode):
                print("IC = " + str(DIC).zfill(2) +":      addi $"+ str(Rx) +", "+ str(imm) + " =>  "+"$"+ str(Rx) + " = $" + str(Rx) + " + " + str(imm))
        elif(fetch[0:2] == "10"):       #bne
            valx  = reg[int(fetch[2:4],2)]
            imm = int(fetch[4:8],2)
            if(reg[7] != valx):
                line += 1
                DIC +=1
                line  = line - imm
                if(debugMode):
                    print("IC = " + str(DIC).zfill(2) +":      bne $"+ str(int(fetch[2:4],2)) +", LOOP(-"+ str(imm) + ")" + " =>  ($7 != $"+ str(int(fetch[2:4],2)) + ") = " + "True")
            else:
                line += 1
                DIC +=1
                if(debugMode):
                    print("IC = " + str(DIC).zfill(2) +":      bne $"+ str(int(fetch[2:4],2)) +", LOOP(-"+ str(imm) + ")" + " =>  ($7 != $"+ str(int(fetch[2:4],2)) + ") = " + "False")
            branch += 1
        elif(fetch[0:4] == "1100"):     #add
            Rx  = reg[int(fetch[4:6],2)]
            Rx = (reg[6]<<8) + Rx
            Ry = reg[int(fetch[6:8],2)]
            tempAns = Rx + Ry
            reg[6] = int(tempAns>>8)
            reg[int(fetch[4:6],2)] = tempAns & 255
            line += 1
            DIC +=1
            if(debugMode):
                print("IC = " + str(DIC).zfill(2) +":      add $"+ str(int(fetch[4:6],2))+", " + str(int(fetch[6:8],2)) + "   =>  $" + str(int(fetch[4:6],2)) + " = $" + str(int(fetch[4:6],2)) +" + $" +str(int(fetch[6:8],2)) )
        elif(fetch[0:4] == "0101"):     #init
            line += 1
            DIC +=1
            if(fetch[4:8] == "0000"):
                reg[0]  = 251
                if(debugMode):
                    print("IC = " + str(DIC).zfill(2) +":      init  0"+ "  =>  " + "$0 = " + str(reg[0]))
            elif (fetch[4:8] == "0001"):
                reg[0] = 118
                if(debugMode):
                    print("IC = " + str(DIC).zfill(2) +":      init  1" + "  =>  " + "$0 = " + str(reg[0]))
            elif(fetch[4:8] == "0010"):
                reg[0]  = 79
                if(debugMode):
                    print("IC = " + str(DIC).zfill(2) +":      init  2" + "  =>  " + "$0 = " + str(reg[0]))
            elif (fetch[4:8] == "0011"):
                reg[0] = 5
                if(debugMode):
                    print("IC = " + str(DIC).zfill(2) +":      init  3" + "  =>  " + "$0 = " + str(reg[0]))
        elif(fetch[0:4] == "0110"):     #AOS - Average of sums
            line += 1
            DIC +=1
            if(reg[6] != 0):
                reg[0] = (reg[6]<<8) + reg[int(fetch[4:8],2)]
                reg[0] = reg[0] >> 4
                if(debugMode):
                    print("IC = " + str(DIC).zfill(2) +":      AOS  " + str(int(fetch[4:8],2)) + "   =>  " + "$6 != 0, " + "$0 = ($6<<8) + $"+str(int(fetch[4:8],2))+", $0 = "+ str(reg[0]))
            else:
                reg[0] = reg[int(fetch[4:8],2)]
                reg[0] = reg[0] >> 4
                if(debugMode):
                    print("IC = " + str(DIC).zfill(2) +":      AOS  " + str(int(fetch[4:8],2)) + "   =>  " + "$6 == 0, " + "$0 += $"+str(int(fetch[4:8],2))+", $0 = "+ str(reg[0]))
        elif(fetch[0:4] == "0100"):     #setR
            imm = int(fetch[7:8],2)
            reg[int(fetch[4:7],2)] = imm
            line += 1
            DIC +=1
            if(debugMode):
                print("IC = " + str(DIC).zfill(2) +":      setR  $" + str(int(fetch[4:7],2)) +", " + str(imm) + "   =>   $" + str(int(fetch[4:7],2))+ " = " + str(imm) )
        elif(fetch[0:4] == "0011"):   #MAD = multiplies two registers and concatenates the value so that Rx holds only the 4 MSB and $LSB of the result
            valx  = reg[int(fetch[4:6],2)]
            valy = reg[int(fetch[6:8],2)]
            temp= str(valx * valy)
            tempMSB= (valx * valy) >> 12
            tempLSB =(valx * valy) & 15
            reg[int(fetch[4:6],2)] =(tempMSB<<4) + tempLSB
            line += 1
            DIC +=1
            if(debugMode):
                print("IC = " + str(DIC).zfill(2) +":      MAD  $" + str(int(fetch[4:6],2)) +", $" + str(int(fetch[6:8],2)) + "   =>   $" + str(int(fetch[4:6],2))+ " = " + str(reg[int(fetch[4:6],2)]))
        elif(fetch[0:4] == "0111"):     #SLL -> shift logical left by 1
            reg[int(fetch[4:8],2)] = reg[3] <<1
            line += 1
            if(debugMode):
                print("IC = " + str(DIC).zfill(2) +":      sll  $" + str(int(fetch[4:8],2)) + "   =>  " + "$ "+ str(int(fetch[4:8],2)) + "+= $3 << 1")
        elif(fetch[0:4] == "1110"):     #cont - > counts the number of 1's
            Rx = reg[int(fetch[4:8],2)]
            temp=0
            temp  += Rx & 1
            temp  += (Rx & 2)>>1
            temp  += (Rx & 4)>>2
            temp  += (Rx & 8)>>3
            temp  += (Rx & 16)>>4
            temp  += (Rx & 32)>>5
            temp  += (Rx & 64)>>6
            temp  += (Rx & 128)>>7
            reg[int(fetch[4:8],2)] = temp
            line += 1
            DIC +=1
            if(debugMode):
                print("IC = " + str(DIC).zfill(2) +":      count  $" + str(int(fetch[4:8],2)) + "   =>   $" + str(int(fetch[4:8],2)) +" = # of 1's in $" + str(int(fetch[4:8],2))+ ",  $" + str(int(fetch[4:8],2)) + " = " + str(temp))
        else:
            print("This opcode is not valid: ", str(fetch[0:4]) )
            finished = True
            print("Done!!!!")


def main():
    inFile = open("Project3Hex.txt", "r")       #opens the file
    instructions = []                       #declares an array
    
    for line in inFile:
        if(line == "\n" or line[0] == '#'): 
            continue
        line = line.replace('\n', '')
        line = format(int(line, 16), "08b")    #formats the number as 32bits and uses 0 as filler
        instructions.append(line)   
    inFile.close()
    debugMode = int(input("1: Debug Mode \n0: Normal Mode : "))
    disassemble(instructions, debugMode)
main()
