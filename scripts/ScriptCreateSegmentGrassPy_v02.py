import os
import numpy as np
import math
import grass.script as grass





class FuncGrass(object):
    #
    def __init__(self,tableInp,workspacefolder):
        self.workspacefolde=workspacefolder
        self.tableInp=tableInp
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
        self.spacemeters=50
        
    
    def ReadRable(self):
        os.chdir(workspacefolder)
        self.tabVar=np.genfromtxt(self.tableInp,names=True, delimiter=',', dtype=None)
        self.type_coluns_tables =self.tabVar.dtype
        self.type_coluns_tables_fields=self.type_coluns_tables.fields
    
    
    def WriteTxt(self):
        os.chdir(r'D:\_data\Funcao_Mov_rogerio\Grass\Files\temp')#trocar
        
        txt=open("mypoints.csv","w")
        txt.write(`self.corrd_X_unique1`+","+`self.corrd_Y_unique1`+"\n")
        txt.write(`self.corrd_X_unique2`+","+`self.corrd_Y_unique2`)
        txt.close()       

    def TxtExcluded(self):
        os.chdir(r'D:\_data\Funcao_Mov_rogerio\Grass\Files\temp')#trocar
        txt=open("mypoints.txt","w")
        txt.write(`self.corrd_X_unique1`+"|"+`self.corrd_Y_unique1`)
        txt.close()         
    def createFileSinglePoint(self):
        os.chdir(r'D:\_data\Funcao_Mov_rogerio\Grass\Files\temp')#trocar
        grass.run_command ('v.in.ascii',input='mypoints.txt',output=self.outputnameFilePointshp)
        
        
    def VlinesLinesToPoint(self):
        grass.run_command ('v.in.lines',input="mypoints.csv",out=self.outputnameFileLineshp,fs=",",overwrite = True,quiet=True)      
        grass.run_command ('v.to.points',input=self.outputnameFileLineshp,out=self.outputnameFilePointshp,dmax=self.spacemeters,overwrite = True,quiet=True)  
    
    def ExprtImpT(self,):
        os.chdir(r'D:\_data\Funcao_Mov_rogerio\Grass\Files\temp') #trocar
        grass.run_command ('v.out.ogr',input=self.outputnameFilePointshp,dsn=self.outputnameFilePointshp+'.shp',layer=2,type='point',quiet=True)
        grass.run_command ('v.in.ogr',dsn=self.outputnameFilePointshp+'.shp',out=self.outputnameFilePointshp,overwrite = True,quiet=True)
        grass.run_command ('v.build',map=self.outputnameFilePointshp)   
        
    def renameDropCol(self,maps):
        grass.run_command ('v.db.dropcol',map=maps,column="lcat",quiet=True)    
    
    def addcol(self,maps):
        grass.run_command ('v.db.addcol',map=maps,columns="prop double precision",quiet=True)
        grass.run_command ('v.db.addcol',map=maps,columns="P1 varchar(15)")
        grass.run_command ('v.db.addcol',map=maps,columns="P2 varchar(15)")
        grass.run_command ('v.db.addcol',map=maps,columns="Name varchar(15)")
      
    
    
    def CreateTable(self,maps):
        grass.run_command('v.db.addtable', map=maps)
        grass.run_command('v.db.connect',flags='p',map=maps)      
    
    def UpdateData(self,p1,p2,name):
        grass.run_command ('v.db.update',map=self.outputnameFilePointshp,col="P1",value=p1,quiet=True)
        grass.run_command ('v.db.update',map=self.outputnameFilePointshp,col="P2",value=p2,quiet=True)   
        grass.run_command ('v.db.update',map=self.outputnameFilePointshp,col="Name",value=name,quiet=True)
        
    def CreateSelectionDist(self):
        dist=list(self.tabVar['dist'])
    
        dist2=[]
        for i in dist:
            if i== "NA":
                dist2.append(i)
            else:
                dist2.append(float(i))
                
                
        burst=list(self.tabVar['burst'])
        fix=list(self.tabVar['fix'])
        self.xcordList=list(self.tabVar['x'])
        self.ycordList=list(self.tabVar['y'])
        
           
        
        
        
        for i in xrange(3):
            
            if dist[i]>=50:
                self.corrd_X_unique1= self.xcordList[i]
                self.corrd_Y_unique1= self.ycordList[i]   
                
                burstLine1=burst[i]
                
                try:
                    self.corrd_X_unique2= self.xcordList[i+1]
                    self.corrd_Y_unique2= self.ycordList[i+1] 
                    
                    burstLine2=burst[i+1]
                except:
                    self.corrd_X_unique2=-1
                if self.corrd_X_unique2==-1:
                    break
                else:
                    if burstLine1==burstLine2:
        
                        self.outputnameFileLineshp="Line_"+fix[i]+'_'+fix[i+1]
                        self.outputnameFilePointshp=fix[i]+'_'+fix[i+1]
                        FuncGrass.WriteTxt(self)
                        
                        FuncGrass.VlinesLinesToPoint(self)
                        FuncGrass.ExprtImpT(self)
                        
                        #FuncGrass.renameDropCol(self, self.outputnameFilePointshp)
                        FuncGrass.addcol(self, self.outputnameFilePointshp) 
                        FuncGrass.UpdateData(self, fix[i], fix[i+1],name=fix[i]+'_'+fix[i+1])
                    else:
                        pass
                


            if dist[i]<50 or dist[i]=="NA":
                self.corrd_X_unique1= self.xcordList[i]
                self.corrd_Y_unique1= self.ycordList[i]  
                self.outputnameFilePointshp=fix[i]
                FuncGrass.TxtExcluded(self)
                FuncGrass.ExprtImpT(self)
                FuncGrass.addcol(self, self.outputnameFilePointshp) 
                FuncGrass.UpdateData(self, fix[i],'NA',name=fix[i])
                
                
tableInp='ssf_lobos_exemplo_enumerate.txt'
workspacefolder=r'D:\_data\Funcao_Mov_rogerio\Funcao_Mov_rogeri2\Tables'

Insnt=FuncGrass(tableInp, workspacefolder)
Insnt.ReadRable()
Insnt.CreateSelectionDist()

        


