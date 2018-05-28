#! /usr/bin/env python

import argparse,logging,os,csv,subprocess
from activate import activate
from asset_downloader import downloader
from cli_space import space
from os.path import expanduser
from cli_aoi2json import aoijson
from cli_aoi2jsonb import aoijsonb
import getpass
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def planet_key_entry():
    planethome=expanduser("~/.config/planet/")
    if not os.path.exists(planethome):
        os.mkdir(planethome)
    print("Enter your Planet API Key")
    password=getpass.getpass()
    os.chdir(planethome)
    with open("pkey.csv",'w') as completed:
        writer=csv.writer(completed,delimiter=',',lineterminator='\n')
        writer.writerow([password])
def planet_key_from_parser(args):
    planet_key_entry()
def aoijson_from_parser(args):
    aoijson(start=args.start,end=args.end,cloud=args.cloud,inputfile=args.inputfile,geo=args.geo,loc=args.loc)
def aoijsonb_from_parser(args):
    aoijsonb(indir=args.indir,
             infile=args.infile,
             start=args.start,
             end=args.end,
             cloud=args.cloud,
             outdir=args.outdir)

def activate_from_parser(args):
    activate(indir=args.indir,
             asset=args.asset,
             infile=args.infile)
def space_from_parser(args):
    space(indir=args.indir,
         asset=args.asset,
         infile=args.infile)
def downloader_from_parser(args):
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

    parser_planet_key = subparsers.add_parser('planetkey', help='Enter your planet API Key')
    parser_planet_key.set_defaults(func=planet_key_from_parser)

    parser_aoijson=subparsers.add_parser('aoijson',help='Tool to convert KML, Shapefile,WKT,GeoJSON or Landsat WRS PathRow file to AreaOfInterest.JSON file with structured query for use with Planet API 1.0')
    parser_aoijson.add_argument('--start', help='Start date in YYYY-MM-DD?')
    parser_aoijson.add_argument('--end', help='End date in YYYY-MM-DD?')
    parser_aoijson.add_argument('--cloud', help='Maximum Cloud Cover(0-1) representing 0-100')
    parser_aoijson.add_argument('--inputfile',help='Choose a kml/shapefile/geojson or WKT file for AOI(KML/SHP/GJSON/WKT) or WRS (6 digit RowPath Example: 023042)')
    parser_aoijson.add_argument('--geo', default='./map.geojson',help='map.geojson/aoi.kml/aoi.shp/aoi.wkt file')
    parser_aoijson.add_argument('--loc', help='Location where aoi.json file is to be stored')
    parser_aoijson.set_defaults(func=aoijson_from_parser)

    parser_aoijsonb=subparsers.add_parser('aoijsonb',help='Tool to batch convert KML, Shapefile,WKT,GeoJSON or Landsat WRS PathRow file to AreaOfInterest.JSON file with structured query for use with Planet API 1.0')
    parser_aoijsonb.add_argument('--indir', help='Input directory with geojson,kml,shp or wkt files',default=None)
    parser_aoijsonb.add_argument('--start', help='Start date in YYYY-MM-DD?')
    parser_aoijsonb.add_argument('--end', help='End date in YYYY-MM-DD?')
    parser_aoijsonb.add_argument('--cloud', help='Maximum Cloud Cover(0-1) representing 0-100')
    parser_aoijsonb.add_argument('--outdir', help='Output directory to save the formatted json files renamed filename_aoi.json',default=None)
    parser_aoijsonb.add_argument('--infile', help='Input list with geojson,kml,shp or wkt files',default=None)
    parser_aoijsonb.set_defaults(func=aoijsonb_from_parser)

    parser_activate = subparsers.add_parser('activate', help='Allows users to batch activate assets using a directory with json or list of json(Sends updates on Slack if slack key added)')
    parser_activate.add_argument('--indir', help='Input directory with structured json files',default=None)
    parser_activate.add_argument('--asset', help='Choose from asset type for example:"PSOrthoTile analytic"|"REOrthoTile analytic"',default=None)
    parser_activate.add_argument('--infile', help='File list with headers pathways:path to json file|asset:asset type|',default=None)
    parser_activate.set_defaults(func=activate_from_parser)

    parser_space = subparsers.add_parser('space', help='Allows users to batch estimate asset sizes using a directory with json or list of json(Sends updates on Slack if slack key added)')
    parser_space.add_argument('--indir', help='Input directory with structured json files',default=None)
    parser_space.add_argument('--asset', help='Choose from asset type for example:"PSOrthoTile analytic"|"REOrthoTile analytic"',default=None)
    parser_space.add_argument('--infile', help='File list with headers pathways:path to json file|asset:asset type|',default=None)
    parser_space.set_defaults(func=space_from_parser)

    parser_downloader = subparsers.add_parser('downloader', help='Allows users to batch download assets using a directory with json or list of json(Sends updates on Slack if slack key added)')
    parser_downloader.add_argument('--indir', help='Input directory with structured json files',default=None)
    parser_downloader.add_argument('--asset', help='Choose from asset type for example:"PSOrthoTile analytic"|"REOrthoTile analytic"',default=None)
    parser_downloader.add_argument('--outdir', help='Output directory to save the assets',default=None)
    parser_downloader.add_argument('--infile', help='File list with headers pathways:path to json file|directory:output directory|asset:asset type|',default=None)
    parser_downloader.set_defaults(func=downloader_from_parser)

    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__':
    main()

