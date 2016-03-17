import os
import json
import time
import sys
import time
import numpy as np;
import copy;
import pylab as pl;
import matplotlib.pyplot as plt;
import urllib2
from pandas.io.json import json_normalize
import pandas as pd;
from django.shortcuts import render
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login

def print_statistics(dataframe, column_name):
    myStatistics = '\n';
    myStatistics = myStatistics + ' ' + ' Mean: ' + str(dataframe[column_name].mean()) + '\n';
    myStatistics = myStatistics + ' '  + ' Max: ' + str(dataframe[column_name].max()) + '\n';
    myStatistics = myStatistics + ' '  + ' Min: ' + str(dataframe[column_name].min()) + '\n';
    myStatistics = myStatistics + ' ' + ' Median: ' + str(dataframe[column_name].median()) + '\n';
    myStatistics = myStatistics + ' '  + ' Std. Dev: ' + str(dataframe[column_name].std()) + '\n';
    myStatistics+= ' '  + ' Frequent values: ';
    if(len(dataframe[column_name].mode().tolist())==0):
        myStatistics+=' <<Empty>>';
    else:
        for i in list(dataframe[column_name].mode().tolist()):
            myStatistics+=' ' + str(i);
            myStatistics+=' ';
            myStatistics+='\n';
    return myStatistics;

def print_statistics_complete(df, myFrame, emailAddress):
    myFrame2 = myFrame.groupby('email').groups;
    print(myFrame2);
    f = emailAddress in myFrame2.keys();
    if(f==False):
        return 'E-Mail Address Wrong!  Check and try again!';
    ids = myFrame2[emailAddress];
    if(len(ids)==0):
        return 'User Mail ID does not exist';

    '''Get Print Data(DeadPercent, LivePercent and Elasticity) and Graph'''
    df_print = df["print_data"];
    df_print_user = pd.DataFrame.from_records(df_print);
    df_print_user = df_print_user[ids[0]:ids[len(ids)-1]];
    pd.options.display.mpl_style = 'default';
    df_print_user.boxplot();
    fig = plt.gcf();
    fig.savefig("print_data.png");
    all_statistics = '\n';
    all_statistics += '\n \t DeadPercent \t \n';
    all_statistics += print_statistics(df_print_user, "deadPercent");
    all_statistics += '\n';
    all_statistics += '\n \t LivePercent \t \n';
    all_statistics += print_statistics(df_print_user, "livePercent");
    all_statistics += '\n';
    all_statistics += '\n \t Elasticity \t \n';
    all_statistics += print_statistics(df_print_user, "elasticity");
    all_statistics += '\n';
    
    '''Get Print Info Pressure(Extruder 1, 2) values and Graph'''
    df_print_info = df["print_info"];
    df_print_info_user = pd.DataFrame.from_records(df_print_info);
    print(df_print_info_user.columns);
    pressure_frame = df_print_info_user["pressure"];
    pressure_frame = pd.DataFrame.from_records(pressure_frame)
    pressure_frame = pressure_frame[ids[0]:ids[len(ids)-1]];
    pd.options.display.mpl_style = 'default';
    pressure_frame.boxplot();
    fig = plt.gcf();
    fig.savefig("pressure_data.png");
    all_statistics += '\n \t Extruder1 Pressure \t \n';
    all_statistics += print_statistics(pressure_frame, "extruder1");
    all_statistics += '\n';
    all_statistics += '\n \t Extruder2 Pressure \t \n';
    all_statistics+=print_statistics(pressure_frame, "extruder2");
    all_statistics += '\n';
    
    '''Get Print Info Crosslinking(Enabled, Intensity, Duration) values and Graph'''
    crosslinking_frame = df_print_info_user["crosslinking"];
    crosslinking_frame = pd.DataFrame.from_records(crosslinking_frame);
    crosslinking_frame = crosslinking_frame[ids[0]:ids[len(ids)-1]];
    pd.options.display.mpl_style = 'default';
    enabledFrame = crosslinking_frame['cl_enabled'];
    all_statistics += '\n \t Enabled % \t \n';
    enabled_normalized = enabledFrame.value_counts(normalize=True);
    enabled_normalized_string = str(enabled_normalized);
    enabled_normalized_string = enabled_normalized_string[:-16];
    all_statistics = all_statistics + " " + enabled_normalized_string + "\n";
    durationIntensityFrame = crosslinking_frame[['cl_duration', 'cl_intensity']];
    durationIntensityFrame = pd.DataFrame.from_records(durationIntensityFrame);
    pd.options.display.mpl_style = 'default';
    durationIntensityFrame.boxplot();
    fig = plt.gcf();
    fig.savefig("crosslinking_data.png");
    all_statistics += '\n';
    all_statistics += '\n \t Duration \t \n';
    all_statistics+=print_statistics(durationIntensityFrame, "cl_duration");
    all_statistics+='\n';
    print 'Intensity '
    all_statistics += '\n \t Intensity \t \n';
    all_statistics+=print_statistics(durationIntensityFrame, "cl_intensity");
    all_statistics+='\n';

    '''Get Print Info Resolution(layerNum, layerHeight) values and Graph'''
    resolution_frame = df_print_info_user["resolution"];
    resolution_frame = pd.DataFrame.from_records(resolution_frame);
    resolution_frame = resolution_frame[ids[0]:ids[len(ids)-1]];
    pd.options.display.mpl_style = 'default';
    resolution_frame_new = copy.deepcopy(resolution_frame);
    resolution_frame_new.boxplot(column='layerNum');  #A different version of box plot specifying column name
    fig = plt.gcf();
    fig.savefig("layerNum.png");
    resolution_frame.boxplot(by='layerHeight');
    fig = plt.gcf();
    fig.savefig("layerHeight.png");
    all_statistics += '\n \t Number of Layers \t \n';
    all_statistics+=print_statistics(resolution_frame, "layerNum");
    all_statistics+='\n';
    all_statistics += '\n \t Layer Height \t \n';
    all_statistics+=print_statistics(resolution_frame, "layerHeight");
    all_statistics+='\n';
    
    '''Get Print Info - frequently occuring WellPlate Info'''
    all_statistics += '\n \t WellPlate Info \t \n';
    wellplate_frame = df_print_info_user["wellplate"];
    wellplate_frame = wellplate_frame[ids[0]:ids[len(ids)-1]];
    all_statistics+=' '  + ' Frequently Occuring WellPlate Type: ';
    for i in list(wellplate_frame.mode().tolist()):
        all_statistics+=str(i);
        all_statistics+='\t';
    all_statistics+='\n\n\n';
    return all_statistics;

def index(request):
    return HttpResponse("Hello");


'''Functions to redirect and display the appropriate generated boxplot for each field'''

def view_print_result(request):
    if request.POST:
        print_path = os.getcwd() + '/print_data.png';
        image_data =  open(print_path,"rb").read();
        return HttpResponse(image_data, content_type="image/png");

def view_pressure_result(request):
    if request.POST:
        pressure_path = os.getcwd() + '/pressure_data.png';
        image_data =  open(pressure_path, "rb").read();
        return HttpResponse(image_data, content_type="image/png");

def view_crosslinking_result(request):
    if request.POST:
        crosslinking_path = os.getcwd() + '/crosslinking_data.png';
        image_data =  open(crosslinking_path, "rb").read();
        return HttpResponse(image_data, content_type="image/png");

def view_layernum_result(request):
    if request.POST: 
        layernum_path = os.getcwd() + '/layerNum.png';
        image_data =  open(layernum_path, "rb").read();
        return HttpResponse(image_data, content_type="image/png");

def view_layerheight_result(request):
    if request.POST:       
        layerheight_path = os.getcwd() + '/layerHeight.png';
        image_data = open(layerheight_path, "rb").read();
        return HttpResponse(image_data, content_type="image/png");


def login_user(request):
    state = "Please log in below..."
    usermail = ''
    if request.POST:
        usermail = request.POST.get('usermail')
        #Pass Json file right away here -
        df = pd.read_json("https://raw.githubusercontent.com/biobotsdev/biobots-coding-challenge-2015/master/bioprint-data.json");
        df2 = df["user_info"];
        myFrame = pd.DataFrame.from_records(df2);
        state = print_statistics_complete(df,myFrame, usermail)
        return render_to_response('dispData.html', {'state':state, 'usermail': usermail}, context_instance=RequestContext(request));
    else:
        return render_to_response('auth.html',{'state':state, 'usermail': usermail}, context_instance=RequestContext(request))
