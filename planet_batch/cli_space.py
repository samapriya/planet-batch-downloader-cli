import subprocess,os,csv,time
os.chdir(os.path.dirname(os.path.realpath(__file__)))
now=time.strftime("%c")
tm="Last estimated at %s" % now

def space(indir=None,asset=None,infile=None):
    if infile==None:
        for filename in os.listdir(indir):
            if filename.endswith('.json'):
                aoi=os.path.join(indir,filename)
                local=indir
                inlet='"'+local+'"'+" "+asset
                print('')
                print("Using Directory sort & processing "+str(filename)+' Asset type '+str(asset))
                try:
                    sz=subprocess.check_output('python download.py --query '+'"'+aoi+'"'+' --size '+inlet,shell=True)
                    asstsize=(sz.split("Size in GB', '")[1].split("'")[0])
                    #print(sz.split("Space in GB', '")[1].split("'")[0])
                    comb=str(os.path.basename(aoi))+':'+str(asset)+': *'+str(asstsize)+'* GB'
                    print('Using '+str(os.path.basename(aoi))+' estimated download size for activated assets of type '+str(asset)+' is '+asstsize+" GB ")
                except Exception:
                    print(' ')
    else:
        with open(infile) as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                aoi=str(row["pathways"])
                asset=str(row["asset"])
                outdir=str(row["directory"])
                [head,tail]=os.path.split(aoi)
                local=head
                inlet='"'+local+'"'+" "+asset
                print('')
                print("Using filelist & processing "+str(os.path.basename(aoi))+' Asset type '+str(asset))
                try:
                    sz=subprocess.check_output('python download.py --query '+'"'+aoi+'"'+' --size '+inlet,shell=True)
                    asstsize=(sz.split("Size in GB', '")[1].split("'")[0])
                    comb=str(os.path.basename(aoi))+':'+str(asset)+': *'+str(asstsize)+'* GB'
                    print('Using '+str(os.path.basename(aoi))+' estimated download size for activated assets of type '+str(asset)+' is '+asstsize+" GB ")
                except Exception:
                    print(' ')
