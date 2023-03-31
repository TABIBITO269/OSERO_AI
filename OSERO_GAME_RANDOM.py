import tkinter as tk
import numpy as np
import re
import random
import time
import sys

board_before=None
board_after=None
mass=None
turn="WHITE"
part=-1
color=None
lis=[]

mass_list=np.zeros((8,8))
mass_list[3,3]=1
mass_list[3,4]=-1
mass_list[4,3]=-1
mass_list[4,4]=1

root=tk.Tk()
root.geometry("500x500")
root.resizable(0,0)
root.title("オセロ")

root.grid_rowconfigure(0,weight=1)
root.grid_columnconfigure(0,weight=1)

frame=tk.Frame(root)
frame.grid()

class osero():#初めにボタンを配置、その中のボタンのうち1、-1ならばいろをつけたラベルを配置
    def __init__(self):
        global frame
        #print(mass_list)
        osero.cancel(None)
        if turn==None:
            print("BLACK")#先行の駒を入力してください
        else:
            if turn=="BLACK":
                print("WHITE")
            else:
                print("BLACK")
        if not 0 in mass_list:
            for x in range(mass_list.shape[0]):
                for y in range(mass_list.shape[1]):
                    button=tk.Frame(frame,width=50,height=50,relief="sunken",bg="Green",bd=1)
                    button.grid(row=x,column=y)
                    button.bind("<1>",osero.pushed)
                    if mass_list[x,y]==1:
                        label=tk.Frame(button,width=48,height=48,relief="sunken",bg="WHite")
                        label.grid()
                    elif mass_list[x,y]==-1:
                        label=tk.Frame(button,width=48,height=48,relief="sunken",bg="Black",)
                        label.grid()
                    else:
                        pass
            osero.end(None)
            
        osero.pushed(None)

    def pushed(self):
        global turn
        global part
        global color
        global mass
        if mass=="":
            mass=1
        if turn=="BLACK":
            turn="WHITE"
            color=1
            ###################
            num=len(lis)
            a=random.randint(1,num)
            mass=lis[a-1]
            mass=mass+part*64
            ####################
            osero.change_mass_list(mass,color,part)
        elif turn=="WHITE":
            turn="BLACK"
            color=-1
            ####################
            num=len(lis)
            a=random.randint(1,num)
            mass=lis[a-1]
            mass=mass+part*64
            ####################
            osero.change_mass_list(mass,color,part)
            
        
    def change_mass_list(mass,color,part):
        global mass_list
        mass=int(mass)-(64*part)
        remainder=mass%8
        if remainder==0:
            column=(mass//8)-1
            row=(mass-column*8)-1
            mass_list[column,row]=color
            print(column,row)
            osero.rule(column,row)
            osero.judge(1)
        else:
            column=mass//8
            row=(mass-column*8)-1
            mass_list[column,row]=color
            print(column,row)
            osero.rule(column,row)
            osero.judge(1)


    def rule(column,row):
        global mass_list
        global color
        global board_before
        global board_after
        board_before=mass_list.copy()#値渡し(.copy()がないと参照渡しとなる)
        if row!=0:#左の駒と比較
        
            if (mass_list[column,row-1]==mass_list[column,row])or(mass_list[column,row-1]==0):
                pass
            else:
                for x in range(1,row+1):
                    if mass_list[column,row-x]==0:
                        break
                    elif mass_list[column,row-x]==mass_list[column,row]:
                        for b in range(x):
                                mass_list[column,row-b]=color
                        break



        if row!=7:#右の駒と比較
            if (mass_list[column,row+1]==mass_list[column,row])or(mass_list[column,row+1]==0):
                pass
            else:
                for x in range(1,8-row):
                    if mass_list[column,row+x]==0:
                        break
                    elif mass_list[column,row+x]==mass_list[column,row]:
                        for b in range(x):
                                mass_list[column,row+b]=color
                        break

        if column!=0:#上の駒と比較
            if (mass_list[column-1,row]==mass_list[column,row])or(mass_list[column-1,row]==0):
                pass
            else:
                for x in range(1,column+1):
                    if mass_list[column-x,row]==mass_list[column,row]:
                        for b in range(x):
                            mass_list[column-b,row]=color
                        break
                    elif mass_list[column-x,row]==0:
                        break

        if column!=7:#下の駒と比較
            if (mass_list[column+1,row]==mass_list[column,row])or(mass_list[column+1,row]==0):
                pass
            else:
                for x in range(1,8-column):
                    if mass_list[column+x,row]==mass_list[column,row]:
                        for b in range(x):
                            mass_list[column+b,row]=color
                        break
                    elif mass_list[column+x,row]==0:
                        break

        if (column!=0) and (row!=0):#左上の駒と比較
            if (mass_list[column-1,row-1]==mass_list[column,row])or(mass_list[column-1,row-1]==0):
                pass
            else:
                if column > row:
                    for x in range(1,row+1):
                        if mass_list[column-x,row-x]==mass_list[column,row]:
                            for b in range(x):
                                mass_list[column-b,row-b]=color
                            break
                        elif mass_list[column-x,row-x]==0:
                            break
                else:
                    for x in range(1,column+1):
                        if mass_list[column-x,row-x]==mass_list[column,row]:
                            for b in range(x):
                                mass_list[column-b,row-b]=color
                            break
                        elif mass_list[column-x,row-x]==0:
                            break

        if (column!=7) and (row!=7):#右下の駒と比較
            if (mass_list[column+1,row+1]==mass_list[column,row])or(mass_list[column+1,row+1]==0):
                pass
            else:
                if column > row:
                    for x in range(1,8-column):
                        if mass_list[column+x,row+x]==mass_list[column,row]:
                            for b in range(x):
                                mass_list[column+b,row+b]=color
                            break
                        elif mass_list[column+x,row+x]==0:
                            break
                else:
                    for x in range(1,8-row):
                        if mass_list[column+x,row+x]==mass_list[column,row]:
                            for b in range(x):
                                mass_list[column+b,row+b]=color
                            break
                        elif mass_list[column+x,row+x]==0:
                            break
                        
        if (row!=7) and (column!=0):#右上の駒と比較
            if (mass_list[column-1,row+1]==mass_list[column,row])or(mass_list[column-1,row+1]==0):
                pass
            else:
                if (column <= 3) and (row <= 3):
                    for x in range(1,column+1):
                        if mass_list[column-x,row+x]==mass_list[column,row]:
                            for b in range(x):
                                mass_list[column-b,row+b]=color
                            break
                        elif mass_list[column-x,row+x]==0:
                            break
                if (column > 3) and (row <= 3):
                    if (column+row)<=7:
                        for x in range(1,column+1):
                            if mass_list[column-x,row+x]==mass_list[column,row]:
                                for b in range(x):
                                    mass_list[column-b,row+b]=color
                                break
                            elif mass_list[column-x,row+x]==0:
                                break
                    elif (column+row)>7:
                        for x in range(1,8-row):
                            if mass_list[column-x,row+x]==mass_list[column,row]:
                                for b in range(x):
                                    mass_list[column-b,row+b]=color
                                break
                            elif mass_list[column-x,row+x]==0:
                                break
                if (column <= 3) and (row > 3):
                    if (column+row)<=7:
                        for x in range(1,column+1):
                            if mass_list[column-x,row+x]==mass_list[column,row]:
                                for b in range(x):
                                    mass_list[column-b,row+b]=color
                                break
                            elif mass_list[column-x,row+x]==0:
                                break
                    elif (column+row)>7:
                        for x in range(1,8-row):
                            if mass_list[column-x,row+x]==mass_list[column,row]:
                                for b in range(x):
                                    mass_list[column-b,row+b]=color
                                break
                            elif mass_list[column-x,row+x]==0:
                                break
                if (column > 3) and (row > 3):
                    for x in range(1,8-row):
                        if mass_list[column-x,row+x]==mass_list[column,row]:
                            for b in range(x):
                                mass_list[column-b,row+b]=color
                        elif mass_list[column-x,row+x]==0:
                            break
                        
        if (row!=0) and (column!=7):#左下の駒と比較
            if (mass_list[column+1,row-1]==mass_list[column,row])or(mass_list[column+1,row-1]==0):
                pass
            else:
                if (column <= 3) and (row <= 3):
                    for x in range(1,row+1):
                        if mass_list[column+x,row-x]==mass_list[column,row]:
                            for b in range(x):
                                mass_list[column+b,row-b]=color
                            break
                        elif mass_list[column+x,row-x]==0:
                            break
                if (column > 3) and (row <= 3):
                    if (column+row)<=7:
                        for x in range(1,row+1):
                            if mass_list[column+x,row-x]==mass_list[column,row]:
                                for b in range(x):
                                    mass_list[column+b,row-b]=color
                                break
                            elif mass_list[column+x,row-x]==0:
                                break
                    elif (column+row)>7:
                        for x in range(1,8-column):
                            if mass_list[column+x,row-x]==mass_list[column,row]:
                                for b in range(x):
                                    mass_list[column+b,row-b]=color
                                break
                            elif mass_list[column+x,row-x]==0:
                                break
                if (column <= 3) and (row > 3):
                    if (column+row)<=7:
                        for x in range(1,row+1):
                            if mass_list[column+x,row-x]==mass_list[column,row]:
                                for b in range(x):
                                    mass_list[column+b,row-b]=color
                                break
                            elif mass_list[column+x,row-x]==0:
                                break
                    elif (column+row)>7:
                        for x in range(1,8-column):
                            if mass_list[column+x,row-x]==mass_list[column,row]:
                                for b in range(x):
                                    mass_list[column+b,row-b]=color
                                break
                            elif mass_list[column+x,row-x]==0:
                                break
                if (column > 3) and (row > 3):
                    for x in range(1,8-column):
                        if mass_list[column+x,row-x]==mass_list[column,row]:
                            for b in range(x):
                                mass_list[column+b,row-b]=color
                            break
                        elif mass_list[column+x,row-x]==0:
                            break
        board_after=mass_list.copy()
        return board_before,board_after


    def judge(x):
            #print(mass_list)
            osero.compare(mass_list)
    
                      
            
    def compare(x):
        global board_after
        global board_before
        global color
        global turn
        global mass
        COMPARE_COLOR=color
        if part==-1:
            pass
        else:
            if  np.allclose(board_before,board_after):
                color=0
                mass=int(mass)-(64*part)
                remainder=mass%8
                if remainder==0:
                    column=(mass//8)-1
                    row=(mass-column*8)-1
                    mass_list[column,row]=color
                    if COMPARE_COLOR==-1:
                        turn="WHITE"
                    elif COMPARE_COLOR==1:
                        turn="BLACK"
                else:
                    column=mass//8
                    row=(mass-column*8)-1
                    mass_list[column,row]=color
                    if COMPARE_COLOR==-1:
                        turn="WHITE"
                    elif COMPARE_COLOR==1:
                        turn="BLACK"
            else:
                pass
        osero()

    def cancel(x):#駒がおけないときのパスを判定する
        global turn
        global color
        global mass_list
        global lis
        judgement=None
        lis=[]
        mass_list_before=mass_list.copy()
        while  (turn=="BLACK") and (judgement==None):
            color=1
            for x in range(mass_list.shape[0]):
                for y in range(mass_list.shape[1]):
                    if mass_list[x,y]!=0:
                        pass
                    else:
                        mass_list[x,y]=1
                        osero.rule(x,y)
                        mass_list=mass_list_before.copy()
                        if not np.allclose(board_before,board_after):
                            lis.append(x*8+y+1)
                            judgement="OK"
                            mass_list=mass_list_before.copy()
                            continue
            if judgement=="OK":
                turn="BLACK"
            else:
                turn="WHITE"
        while  (turn=="WHITE") and (judgement==None):
            color=-1
            for x in range(mass_list.shape[0]):
                for y in range(mass_list.shape[1]):
                    if mass_list[x,y]!=0:
                        pass
                    else:
                        mass_list[x,y]=-1
                        osero.rule(x,y)
                        mass_list=mass_list_before.copy()
                        if not np.allclose(board_before,board_after):
                            lis.append(x*8+y+1)
                            judgement="OK"
                            mass_list=mass_list_before.copy()
            if judgement=="OK":
                turn="WHITE"
            else:
                turn="BLACK"
            
        mass_list=mass_list_before

    def end(self):
        print("end")
        print(mass_list)
        fact=mass_list.flatten()
        print(type(fact))
        #z=np.bincount(fact)
        #print(z)

        sys.exit()
                
         
     
        
        
if __name__ == '__main__':
    osero()

        
