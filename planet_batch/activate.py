import subprocess
import time
import progressbar,os,csv
os.chdir(os.path.dirname(os.path.realpath(__file__)))
def activate(indir=None,asset=None,infile=None):
    if infile==None:
        aoicount=[]
        for filename in os.listdir(indir):
            if filename.endswith('.json'):
                aoi=os.path.join(indir,filename)
                print('')
                print("Using Directory sort & processing "+str(filename)+' Asset type '+str(asset))
                try:
                    activate= subprocess.check_output("python download.py --query "+'"'+aoi+'" '+"--activate "+asset,shell=True)
                    item=int((str(activate).split('...')[1].split(' available')[0]))
                    comb=str(os.path.basename(aoi))+':'+str(asset)+': '+str(item)+' '
                    aoicount.append(str(comb))
                except Exception as e:
                    print(e)
                finally:
                    print("Activation Requested for " +str(item)+' '+str(asset)+' using '+str(os.path.basename(aoi)))
    else:
        with open(infile) as csvFile:
            reader = csv.DictReader(csvFile)
            aoicount=[]
            itmcount=[]
            join1=[]
            for row in reader:
                aoi=str(row["pathways"])
                asset=str(row["asset"])
                print('')
                print("Using CSV file & processing "+str(os.path.basename(aoi))+' Asset type '+str(asset))
                try:
                    activate= subprocess.check_output("python download.py --query "+'"'+aoi+'" '+"--activate "+asset+'"',shell=True)
                    item=int((str(activate).split('...')[1].split(' available')[0]))
                    comb=str(os.path.basename(aoi))+':'+str(asset)+': *'+str(item)+'* '
                    aoicount.append(str(comb))
                except Exception as e:
                    print(e)
                finally:
                    print("Activation Requested for " +str(item)+' '+str(asset)+' using '+str(os.path.basename(aoi)))
