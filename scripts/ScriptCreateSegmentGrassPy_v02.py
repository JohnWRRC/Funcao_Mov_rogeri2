# -*- coding: utf-8 -*-
"""
Editos: Bernardo Pacas, John Ribeiro


"""

import os
import numpy as np
import math
import grass.script as grass





class FuncGrass(object):
    #
    def __init__(self,tableInp,workspacefolder,SpacePointDistance,Mindistance):
        self.Mindistance=Mindistance
        self.SpacePointDistance=SpacePointDistance #spacing of separate points
        self.workspacefolde=workspacefolder # input table way
        self.tableInp=tableInp #input table name
        self.tabVar='' # table load 
        self.type_coluns_tables='' 
        self.type_coluns_tables_fields=''
        self.xcordList=''
        self.ycordList=''
        self.corrd_X_unique1=''
        self.corrd_X_unique2=''
        self.corrd_Y_unique1=''
        self.corrd_Y_unique2=''
        
        self.outputnameFileLineshp=''
        self.outputnameFilePointshp=''
        
        self.burst='' # Colouna extracted ta table
        self.dist=''  # Colouna extracted ta table
        self.dist2='' # Colouna extracted ta table
        self.fix=''   # Colouna extracted ta table 
        
    
    def ReadRable(self):
        """
        
        Function To read data table
        self.tabVar contains the entire table , elf.type_coluns_tables contains column types and names , 
        self.type_coluns_tables_fields contains the column names . It to be possible to make the table subsets
        """
        os.chdir(workspacefolder)
        self.tabVar=np.genfromtxt(self.tableInp,names=True, delimiter=',', dtype=None)
        self.type_coluns_tables =self.tabVar.dtype
        self.type_coluns_tables_fields=self.type_coluns_tables.fields
    
    
    def WriteTxt(self):
        """
        Function to create the input txt to create the lines,
        the function of grass requires vc create a txt with the
        coordinate of the points to which you want to connect , and this has exactly this format
        """
        os.chdir(r'D:\_data\Funcao_Mov_rogerio\Grass\Files\temp')#trocar
        
        txt=open("mypoints.csv","w")
        txt.write(`self.corrd_X_unique1`+","+`self.corrd_Y_unique1`+"\n")
        txt.write(`self.corrd_X_unique2`+","+`self.corrd_Y_unique2`)
        txt.close()       

    def TxtExcluded(self):
        """
        This function is similar to another,
        also create a txt but now is to make the plot point that not atigiu
        the minimum distance and also to the row that contains NAs
        """
        
        os.chdir(r'D:\_data\Funcao_Mov_rogerio\Grass\Files\temp')#trocar
        txt=open("mypoints.txt","w")
        txt.write(`self.corrd_X_unique1`+"|"+`self.corrd_Y_unique1`)
        txt.close()         
    def createFileSinglePoint(self):
        """
        
        Function that creates the point file into the grass
        """
        
        os.chdir(r'D:\_data\Funcao_Mov_rogerio\Grass\Files\temp')#trocar
        grass.run_command ('v.in.ascii',input='mypoints.txt',output=self.outputnameFilePointshp)
        
        
    def VlinesLinesToPoint(self):
             
        """Function that creates the online file into the gras"""
        
        grass.run_command ('v.in.lines',input="mypoints.csv",out=self.outputnameFileLineshp,fs=",",overwrite = True,quiet=True)      
        grass.run_command ('v.to.points',input=self.outputnameFileLineshp,out=self.outputnameFilePointshp,dmax=self.SpacePointDistance,overwrite = True,quiet=True)  
    
    def ExprtImpT(self,):
        """
        The grass has some limitacos with vector files , the main reason
        you have created this function is that the grass when you create
        a file as the split points instance it creates two tables of attributes
        , and all the information we need this in the second layer , and
        this second layer is sort of protected . However I export the point file
        to a folder temp using layer 2 and already care again, so we will
        have a single table associated with the second.
        """
        
        os.chdir(r'D:\_data\Funcao_Mov_rogerio\Grass\Files\temp') #trocar
        grass.run_command ('v.out.ogr',input=self.outputnameFilePointshp,dsn=self.outputnameFilePointshp+'.shp',layer=2,type='point',quiet=True)
        grass.run_command ('v.in.ogr',dsn=self.outputnameFilePointshp+'.shp',out=self.outputnameFilePointshp,overwrite = True,quiet=True)
        #grass.run_command ('v.build',map=self.outputnameFilePointshp)   
        
    def renameDropCol(self,maps):
        
        """
        When the point file is created, it creates a boring
        column and bobona called " LCAT " that not even fucking
        go out , not this function is working a lot.
        """        
        grass.run_command ('v.db.dropcol',map=maps,column="lcat",quiet=True)    
    
    def addcol(self,maps):
        
        """
        function to add columns
        
        """
        grass.run_command ('v.db.addcol',map=maps,columns="prop double precision",quiet=True)
        grass.run_command ('v.db.addcol',map=maps,columns="P1 varchar(15)")
        grass.run_command ('v.db.addcol',map=maps,columns="P2 varchar(15)")
        grass.run_command ('v.db.addcol',map=maps,columns="NameF varchar(15)")
        grass.run_command ('v.db.addcol',map=maps,columns="P1 varchar(15)")
      
    
    
    def CreateTable(self,maps):
        """
        Create of the table to files in grass and conect 
        """
        grass.run_command('v.db.addtable', map=maps)
        grass.run_command('v.db.connect',flags='p',map=maps)      
    
    def UpdateData(self,p1,p2,name):
        """
        Does the update data
        """
        grass.run_command ('v.db.update',map=self.outputnameFilePointshp,col="P1",value=p1,quiet=True)
        grass.run_command ('v.db.update',map=self.outputnameFilePointshp,col="P2",value=p2,quiet=True)   
        grass.run_command ('v.db.update',map=self.outputnameFilePointshp,col="NameF",value=name,quiet=True)
     
    
    def CreateSubsetList(self):
        """
        
        This function creates the subset lists the original table
        """
        #----------------------------------------
        self.dist=list(self.tabVar['dist'])
        self.dist2=[]
        for i in dist:
            if i== "NA":
                self.dist2.append(i)
            else:
                self.dist2.append(float(i))     
         #----------------------------------------
         
        self.burst=list(self.tabVar['burst'])
        self.fix=list(self.tabVar['fix'])
        self.xcordList=list(self.tabVar['x']) # 
        self.ycordList=list(self.tabVar['y'])        
       
    def CreateSelectionDist(self):  
        
        """
        Main function , that function all the other functions are called
        """
        FuncGrass.ReadRable(self)
        FuncGrass.CreateSubsetList(self) 

        for i in xrange(3):
            
            if self.dist2[i]>=self.Mindistance:
                self.corrd_X_unique1= self.xcordList[i]
                self.corrd_Y_unique1= self.ycordList[i]    
                self.burstLine1=self.burst[i]
                
                try:
                    self.corrd_X_unique2= self.xcordList[i+1]
                    self.corrd_Y_unique2= self.ycordList[i+1] 
                    
                    self.burstLine2=self.burst[i+1]
                except:
                    self.corrd_X_unique2=-1
                if self.corrd_X_unique2==-1:
                    break
                else:
                    if self.burstLine1==self.burstLine2:
                        self.outputnameFileLineshp="Line_"+self.fix[i]+'_'+self.fix[i+1]
                        self.outputnameFilePointshp=self.fix[i]+'_'+self.fix[i+1]
                        FuncGrass.WriteTxt(self)
                        FuncGrass.VlinesLinesToPoint(self)
                        FuncGrass.ExprtImpT(self)
                        #FuncGrass.renameDropCol(self, self.outputnameFilePointshp)
                        FuncGrass.addcol(self, self.outputnameFilePointshp) 
                        FuncGrass.UpdateData(self, self.fix[i], self.fix[i+1],name=self.fix[i]+'_'+self.fix[i+1])
                    else:
                        pass
                


            if dist2[i]<self.Mindistance or dist2[i]=="NA":
                self.corrd_X_unique1= self.xcordList[i]
                self.corrd_Y_unique1= self.ycordList[i]  
                self.outputnameFilePointshp=fix[i]
                FuncGrass.TxtExcluded(self)
                FuncGrass.ExprtImpT(self)
                FuncGrass.addcol(self, self.outputnameFilePointshp) 
                FuncGrass.UpdateData(self, self.fix[i],'NA',name=self.fix[i])
                
 
#-------------------------------------------------------------------------------------------#            
#---------------------------------define parameters-----------------------------------------#
tableInp='ssf_lobos_exemplo_enumerate.txt' 
workspacefolder=r'D:\_data\Funcao_Mov_rogerio\Funcao_Mov_rogeri2\Tables'
SpacePointDistance=50
Mindistance=50
#-------------------------------------------------------------------------------------------#   

Insnt=FuncGrass(tableInp, workspacefolder, SpacePointDistance, Mindistance) # instance class
Insnt.CreateSelectionDist() # run main function

        


