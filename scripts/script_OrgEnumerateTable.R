rm(list = ls())
setwd("D:\\_data\\Funcao_Mov_rogerio")

tab<-read.table("ssf_lobos_exemplo.csv",sep=',',header=T) # lendo a tabela
tab$fix<-NA # criando a tabela fix
tabApoio<-NULL
for (i in 1:nrow(tab))
  {
    line1<-as.character(tab$burst[i])
    line2<-as.character(tab$burst[i+1])
    if(! is.na(line2))
      {
        if (line1==line2)
          {
              tab$fix[i]<-paste(tab$burst[i],count,sep = "_")
              count<-count+1
          }
        else
          {
              tab$fix[i]<-paste(tab$burst[i],count,sep = "_")
              count<-1
          
          }

      }
    else{tab$fix[i]<-paste(tab$burst[i],count,sep = "_")}
  }

x<-paste("x","y",sep="_")
