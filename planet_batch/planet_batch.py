#! /usr/bin/env python

import argparse,logging,os,csv,subprocess
from activate import activate
from asset_downloader import downloader
from cli_space import space
from os.path import expanduser
from cli_aoi2json import aoijson
from cli_aoi2jsonb import aoijsonb
from idlist_footprint import id2footprint
from idlst import idl
import getpass
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def planet_key_entry():
    try:
        subprocess.call('planet init',shell=True)
    except Exception as e:
        print(e)
def planet_key_from_parser(args):
    planet_key_entry()
def planet_quota():
    try:
        subprocess.call('planet_quota.py',shell=True)
    except Exception as e:
        print(e)
def planet_quota_from_parser(args):
    planet_quota()
def aoijson_from_parser(args):
    aoijson(start=args.start,end=args.end,cloud=args.cloud,inputfile=args.inputfile,geo=args.geo,loc=args.loc)
def aoijsonb_from_parser(args):
    aoijsonb(indir=args.indir,
             infile=args.infile,
             start=args.start,
             end=args.end,
             cloud=args.cloud,
             outdir=args.outdir)
def idl_from_parser(args):
    item=args.item
    asset=args.asset
    num=int(args.number)
    if args.indir==None:
        idl(infile=args.aoi,item=args.item,asset=args.asset,num=int(args.number))
    elif args.aoi==None:
        l=[]
        for filename in os.listdir(args.indir):
            if filename.endswith('.json'):
                fpath=os.path.join(args.indir,filename)
                inputfile=fpath
                print('')
                print("Creating IDList for "+str(fpath))
                os.system('python idlst.py '+str(inputfile)+' '+str(item)+' '+str(asset)+' '+str(num))
                
                    #idl(infile=items,item=args.item,asset=args.asset,num=int(args.number))

def id2footprint_from_parser(args):
    if args.input==None:
        item=args.item
        asset=args.asset
        export=args.export
        id2footprint(indir=args.indir,inputfile=None,item=args.item,asset=args.asset,export=args.export)
    elif (args.indir==None and args.input==None):
        item=args.item
        asset=args.asset
        export=args.export
        id2footprint(indir=None,inputfile=None,item=args.item,asset=args.asset,export=args.export)
    else:
        inputfile=args.input
        item=args.item
        asset=args.asset
        export=args.export
        id2footprint(indir=None,inputfile=args.input,item=args.item,asset=args.asset,export=args.export)        
def activate_from_parser(args):
    if (args.indir==None and args.infile==None):
        asset_type=str(args.asset)
        subprocess.call("python download.py --idlist "+'"'+"idpl.txt"+'" '+"--activate "+asset_type,shell=True)
    else:
        activate(indir=args.indir,
             asset=args.asset,
             infile=args.infile)
def space_from_parser(args):
    space(indir=args.indir,
         asset=args.asset,
         infile=args.infile)
def downloader_from_parser(args):
    if (args.indir==None and args.infile==None):
        subprocess.call("python download.py --idlist "+'"'+"idpl.txt"+'" '+"--download "+args.outdir+" "+args.asset,shell=True)
    else:
        downloader(indir=args.indir,
                 outdir=args.outdir,
                 asset=args.asset,
                 infile=args.infile)
spacing="                               "
def main(args=None):
    parser = argparse.ArgumentParser(description='Planet Batch Downloader CLI')

    subparsers = parser.add_subparsers()

    parser_pp3 = subparsers.add_parser(' ', help='-------------------------------------------')
    parser_P2 = subparsers.add_parser(' ', help='-----Choose from Planet Batch Tools-----')
    parser_pp4 = subparsers.add_parser(' ', help='-------------------------------------------')

    parser_planet_key = subparsers.add_parser('apikey', help='Enter your planet API Key')
    parser_planet_key.set_defaults(func=planet_key_from_parser)

    parser_planet_quota = subparsers.add_parser('quota', help='Prints your Planet Quota Details')
    parser_planet_quota.set_defaults(func=planet_quota_from_parser)

    parser_idl=subparsers.add_parser('idlist',help='Creates an IDLIST that intersects AOI JSON')
    parser_idl.add_argument('--aoi', help='Choose aoi.json file created earlier',default=None)
    parser_idl.add_argument('--item', help='choose between Planet Item types PSOrthoTile|PSScene4Band|PSScene3Band|REOrthoTile')
    parser_idl.add_argument('--asset',help='Choose between Planet asset types analytic|analytic_dn|visual')
    parser_idl.add_argument('--number',help='Maximum number of assets for the idlist')
    optional_named = parser_idl.add_argument_group('Optional named arguments idlist saved in indir as filename.csv')
    optional_named.add_argument('--indir', help='Folder with CSV Files with IDList header is id')
    parser_idl.set_defaults(func=idl_from_parser)
    
    parser_id2footprint=subparsers.add_parser('id2footprint',help='Convert IDlist to Multi-footprint geojson')
    parser_id2footprint.add_argument('--item', help='Planet Item Type')
    parser_id2footprint.add_argument('--asset', help='Planet Asset Type')
    parser_id2footprint.add_argument('--export',help='Location to Export the Footprint geojson file use only if using input file')
    optional_named = parser_id2footprint.add_argument_group('Optional named arguments if not provided uses idlist')
    optional_named.add_argument('--indir', help='Folder with CSV Files with IDList header is id export geojson(s) in indir')
    optional_named.add_argument('--input', help='CSV File with IDList header is id do not use if using indir')
    parser_id2footprint.set_defaults(func=id2footprint_from_parser)
    
    parser_aoijson=subparsers.add_parser('aoijson',help='Tool to convert KML, Shapefile,WKT,GeoJSON or Landsat WRS PathRow file to AreaOfInterest.JSON file with structured query for use with Planet API')
    parser_aoijson.add_argument('--start', help='Start date in YYYY-MM-DD?')
    parser_aoijson.add_argument('--end', help='End date in YYYY-MM-DD?')
    parser_aoijson.add_argument('--cloud', help='Maximum Cloud Cover(0-1) representing 0-100')
    parser_aoijson.add_argument('--inputfile',help='Choose a kml/shapefile/geojson or WKT file for AOI(KML/SHP/GJSON/WKT) or WRS (6 digit RowPath Example: 023042)')
    parser_aoijson.add_argument('--geo', default='./map.geojson',help='map.geojson/aoi.kml/aoi.shp/aoi.wkt file')
    parser_aoijson.add_argument('--loc', help='Location where aoi.json file is to be stored')
    parser_aoijson.set_defaults(func=aoijson_from_parser)

    parser_aoijsonb=subparsers.add_parser('aoijsonb',help='Tool to batch convert KML, Shapefile,WKT,GeoJSON or Landsat WRS PathRow file to AreaOfInterest.JSON file with structured query for use with Planet API')
    parser_aoijsonb.add_argument('--indir', help='Input directory with geojson,kml,shp or wkt files',default=None)
    parser_aoijsonb.add_argument('--start', help='Start date in YYYY-MM-DD?')
    parser_aoijsonb.add_argument('--end', help='End date in YYYY-MM-DD?')
    parser_aoijsonb.add_argument('--cloud', help='Maximum Cloud Cover(0-1) representing 0-100')
    parser_aoijsonb.add_argument('--outdir', help='Output directory to save the formatted json files renamed filename_aoi.json',default=None)
    parser_aoijsonb.add_argument('--infile', help='Input list with geojson,kml,shp or wkt files',default=None)
    parser_aoijsonb.set_defaults(func=aoijsonb_from_parser)

    parser_activate = subparsers.add_parser('activate', help='Allows users to batch activate assets using a directory with json or list of json')
    parser_activate.add_argument('--asset', help='Choose from asset type for example:"PSOrthoTile analytic"|"REOrthoTile analytic"',default=None)
    optional_named = parser_activate.add_argument_group('Optional named arguments if not provided uses idlist')
    optional_named.add_argument('--indir', help='Input directory with structured json files',default=None)
    optional_named.add_argument('--infile', help='File list with headers pathways:path to json file|asset:asset type|',default=None)
    parser_activate.set_defaults(func=activate_from_parser)

    parser_space = subparsers.add_parser('space', help='Allows users to batch estimate asset sizes using a directory with json or list of json')
    parser_space.add_argument('--indir', help='Input directory with structured json files',default=None)
    parser_space.add_argument('--asset', help='Choose from asset type for example:"PSOrthoTile analytic"|"REOrthoTile analytic"',default=None)
    parser_space.add_argument('--infile', help='File list with headers pathways:path to json file|asset:asset type|',default=None)
    parser_space.set_defaults(func=space_from_parser)

    parser_downloader = subparsers.add_parser('downloader', help='Allows users to batch download assets using a directory with json or list of json(Sends updates on Slack if slack key added)')
    parser_downloader.add_argument('--asset', help='Choose from asset type for example:"PSOrthoTile analytic"|"REOrthoTile analytic"',default=None)
    parser_downloader.add_argument('--outdir', help='Output directory to save the assets',default=None)
    optional_named = parser_downloader.add_argument_group('Optional named arguments if not provided uses idlist')
    optional_named.add_argument('--indir', help='Input directory with structured json files',default=None)
    optional_named.add_argument('--infile', help='File list with headers pathways:path to json file|asset:asset type|',default=None)
    parser_downloader.set_defaults(func=downloader_from_parser)

    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__':
    main()

