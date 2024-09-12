import json,re, os,sys

def read_long_json(fp):
    info_list,segmentID_list = {},[]
    with open(fp,'r',encoding='utf-8-sig') as fr:
        data = json.load(fr)
    try:
        OriginalFileName = data["Result"][0]["Body"]["OriginalFileName"]
        body = data["Result"][0]["Body"]
        segments = body['Segments']
    except Exception as e:
        print(e)
        raise "long json file is not right format"
    for item in segments:
        speaker = item["speaker"]
        start = item["Start"]
        end = item["End"]
        transcriptionContent = item["TranscriptionContent"].strip()
        segmentID = item['SegmentID']
        wave_name = os.path.splitext(os.path.basename(fp))[0] + '_' + segmentID + '.wav' #cs-CZ-2-2-RBLJTKbuEWI_008.wav
        # wave_name = OriginalFileName + '_' + segmentID + '.wav'
        segmentID_list.append(int(segmentID))
        if wave_name not in info_list.keys():
            info_list[wave_name] = transcriptionContent
        else:
            print('相同的segmented 音频名称',fp)
            sys.exit()
        # info_list.append([wave_name,transcriptionContent])
    #======================检查原始名称
    if OriginalFileName != os.path.splitext(os.path.basename(fp))[0]:
        print('输入文件的文件名和文件内写的名称不同：',OriginalFileName,os.path.splitext(os.path.basename(fp))[0])
    #======================检查segmentID
    if len(segmentID_list) != len(set(segmentID_list)):
        print('有重复的segment ID:',fp,segmentID_list)
    if sorted(segmentID_list) != segmentID_list:
        print('original transcription file: segment ID disorder: {}\n乱序{}\t保存顺序{}\n'.format(fp,segmentID_list,sorted(segmentID_list)))
    if diff_list(sorted(segmentID_list)):
        print('有缺省的segment ID')
    #======================检查trans
    if '\t' in transcriptionContent:
        print('trans包含tab:',fp)
    return info_list


def gen_num(input_string):
    if len(list(input_string)) < 3:
        input_string = gen_num(str(0)+str(input_string))
    else:
        return input_string

def read_tsv(inputpath):
    info_list = {}
    # print(inputpath)
    with open(inputpath,'r',encoding='UTF8') as f_trans:
        for i, line in enumerate(f_trans):
            # print(gen_num(str(i)))
            f_name = os.path.splitext(os.path.basename(inputpath))[0] +'_'+ "{:03d}".format(i+1)+'.wav' #line.split('\t')[0].strip().replace('\ufeff','')  #0YMW_ElQJxw_001

            # print(f_name)
            # sys.exit()
            f_p,s_p = line.split(']',1)
            s_time,e_time = f_p.replace('[', '').split(' ')
            sid = s_p.strip().split(' ',1)[0]
            
            # if len(re.sub('<.*?>',' ',s_p).strip().split(' ',1)) == 1:
            #     continue
            # trans = s_p.strip().split(' ',1)[1].replace('[',' ').replace(']',' ').strip()

            if len(re.sub('<.*?>',' ',s_p).strip().split(' ',1)) == 1:
                trans = ''
            else:
                trans = s_p.strip().split(' ',1)[1].replace('[',' ').replace(']',' ').strip()
                # trans = re.sub('\[.*?\]',' ',trans)


            # trans = '[{} {}] {}'.format(s_time,e_time,trans.strip())

            if f_name not in info_list.keys():
                info_list[f_name] = trans
            else:
                print('相同的segmented 音频名称',inputpath)
                sys.exit()
    return info_list


def check_lexicalAndDisplay_consistent(inputpath,outputpath):
    #获取lexical和display的info: {'lexical_format':{filename:[[filename_segID.wav,start,end,trans],[filename_segID.wav,start,end,trans]]},'display_format':{...}}
    trans_folder = {'lexical_format':{},'display_format':{}}  #lexical display的文件名  
    final_dict = {}

    data_info_json = {}
    data_info_txt = {}
    count_utts,count_num_json,count_num_txt = 0,0,0
    for root,der,files in os.walk(os.path.join(inputpath)):
        for file in files:
            #print(file)
            #if file.endswith('.tsv') and 'delivery-addpname' not in root.lower():# and 'lexical' in file.lower():
            if file.endswith('.tsv') and 'verify_lexical' in root.lower():
            # if file.endswith('.tsv') and 'ingest' in file.lower():
                # print(file)
                single_info = read_tsv(os.path.join(root,file))
                count_num_json = len(data_info_json)
                data_info_json.update(single_info)
                if count_num_json+len(single_info) != len(data_info_json):
                    print('update字典后，值不同 NonPName',count_num_json,len(single_info),len(data_info_json))
                    sys.exit()
            #elif file.endswith('.tsv') and 'delivery-addpname' in root.lower():# and 'display' in file.lower():
            elif file.endswith('.txt') and 'verify_display' in root.lower():
            # elif file.endswith('.tsv') and 'other' in file.lower():
                # print(root)
                single_txt_info = read_tsv(os.path.join(root,file))
                count_num_txt = len(data_info_txt)
                data_info_txt.update(single_txt_info)
                if count_num_txt+len(single_txt_info) != len(data_info_txt):
                    print('update字典后，值不同 PName\n',os.path.join(root,file))
                    print(count_num_txt,len(single_txt_info),len(data_info_txt))
                    sys.exit()
        
    print("utts数目",len(data_info_json),len(data_info_txt))
    print(set(data_info_json)-set(data_info_txt))
    # print(data_info_json)
    # print(data_info_json["HQCLbfRE7Jc_058.wav"],'\n',data_info_txt["HQCLbfRE7Jc_058.wav"])
    # sys.exit()

    select_num,select_num_2,select_num_3 = {},{},{}
    select_num_list = {}
    need_check_num_list = []
    count_skip = 0
    # flag_lexical_info = trans_folder['lexical_format']  #
    for i,(key_lex,value_lex) in enumerate(data_info_json.items()): #trans_folder = {'lexical_format':{foldername:{[full_name,start,end,trans],[full_name2,start,end,trans]}},'display_format':{foldername:{[full_name,start,end,trans]}} 
        if key_lex in data_info_txt.keys():    #foldername 相同
            #==============================compare lexical and display trans=============================================
            merge_info = compare_diff(key_lex,value_lex,data_info_txt[key_lex],outputpath)  #{48: ['osmdesát', '80'], 49: ['procent', '%']}
            if len(merge_info) > 0:
                # print('mergr_info:',merge_info)
                
                differ_return=[]#,select_num_list = [],[]   #两个返回值，数字和非数字区分开
                merge_info_key = [int(x) for x in merge_info.keys()]

                # record_line,lex_line,dis_line = '','',''
                # for ind_sav,(sav_key,sav_value) in enumerate(merge_info.items()):
                #     if ind_sav == 0:
                #         record_line = sav_key
                #         lex_line = sav_value[0]
                #         dis_line = sav_value[1]
                #     elif ind_sav < len(merge_info):
                #         if abs(merge_info_key[ind_sav-1]-int(sav_key)) == 1:
                #             record_line = '{} {}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
                #             lex_line = '{} {}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
                #             dis_line = '{} {}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 
                #         else:
                #             record_line = '{}\t{}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
                #             lex_line = '{}\t{}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
                #             dis_line = '{}\t{}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 
##########################################################################
                # record_line,lex_line,dis_line = '','',''
                # correspond_char = {"@":"at",  "&":"and"}
                # for ind_sav,(sav_key,sav_value) in enumerate(merge_info.items()):
                #     if (sav_value[1] in correspond_char) and (sav_value[0] == correspond_char[sav_value[1]]):
                #         # print(sav_key,sav_value)
                #         continue
                #     if ind_sav == 0:
                #         record_line = sav_key
                #         lex_line = sav_value[0]
                #         dis_line = sav_value[1]
                #     elif ind_sav < len(merge_info):
                #         if abs(merge_info_key[ind_sav-1]-int(sav_key)) == 1:
                #             record_line = '{} {}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
                #             lex_line = '{} {}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
                #             dis_line = '{} {}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 
                #         else:
                #             record_line = '{}\t{}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
                #             lex_line = '{}\t{}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
                #             dis_line = '{}\t{}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 

                # if not lex_line.strip() and not dis_line.strip():
                #     continue

                record_line,lex_line,dis_line = '','',''
                # correspond_char = {"@":"at",  "&":"and"}    #base


                # correspond_char = {"@":"at",  "&":"and","iii":"the third","v":"five"}    #en-GB
                # correspond_char = {"xx": "twentieth", "xxi": "twenty first", "xix": "nineteenth", "&":"and"}    #en-IN
                # correspond_char = {"+":"plus", "&":"and", "/":'slash', "@":"at", "#":"hashtag"} #en-US
                # correspond_char = {'xxi':"veintiuno","xx":"veinte", "six": "seis", "xiv": "catorce", "xv": "quince", "xviii": "dieciocho", "xix": "diecinueve","xiii": "trece",
                                    # "xi": "once", "vii":"siete", "xvi":"dieciséis", "xvii": "diecisiete","x": :"equis"}   #es-ES
                # correspond_char = {"+":"más",'xxi':"veintiuno"} #es-MX
                # correspond_char = {"&": "et", "#": "hashtag", "€":"euros", "xxie": "vingt et unième", "xixe": "dix neuvième", "xiv": "quatorze",  "m/s":"mètres par seconde",  "km/h":"kilomètres par heure", "km": "kilomètres"}   #fr-FR
                # correspond_char = {} #hi-IN
                # correspond_char = {"xiv": "quattordicesimo", "xiii": "tredici","xv": "quindici", "&":"and", "+":"più","xix": "diciannovesimo", "xx": "ventesimo", "ii": "due"} #it-IT
                # correspond_char = {} #ja-JP
                correspond_char = {"+": "加", "-": "减", ":": "冒 号"} #zh-CN


                for ind_sav,(sav_key,sav_value) in enumerate(merge_info.items()):
                    # if (sav_value[1] in correspond_char) and (sav_value[0] == correspond_char[sav_value[1]]):
                    #     # print(sav_key,sav_value)
                    #     continue
                    flag_r = False
                    for single_check_char,single_check_word in correspond_char.items():
                        if single_check_char in sav_value[1] and single_check_word in sav_value[0]:
                            if re.sub(r'\s+',' ', sav_value[1].replace(single_check_char,' ')) == re.sub(r'\s+',' ', sav_value[0].replace(single_check_word,' ')):
                                print(single_check_char,single_check_word)
                                flag_r = True

                    if flag_r:
                        continue

                    if ind_sav == 0:
                        record_line = sav_key
                        lex_line = sav_value[0]
                        dis_line = sav_value[1]
                    elif ind_sav < len(merge_info):
                        if abs(merge_info_key[ind_sav-1]-int(sav_key)) == 1:
                            record_line = '{} {}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
                            lex_line = '{} {}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
                            dis_line = '{} {}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 
                        else:
                            record_line = '{}\t{}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
                            lex_line = '{}\t{}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
                            dis_line = '{}\t{}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 

                if not lex_line.strip() and not dis_line.strip():
                    continue


                flag_r = False
                for single_check_char,single_check_word in correspond_char.items():
                    if single_check_char in dis_line and single_check_word in lex_line:
                        if re.sub(r'\s+',' ', dis_line.replace(single_check_char,' ')).strip() == re.sub(r'\s+',' ', lex_line.replace(single_check_word,' ')).strip():
                            print(dis_line, lex_line)
                            flag_r = True
                if flag_r:
                    continue

                lex_line = lex_line.strip()
                dis_line = dis_line.strip()
                
                file_name_final = '_'.join(key_lex.split('_')[:-1])
                file_name_final = file_name_final + ' 第{}行'.format(str(int(os.path.splitext(key_lex.split('_')[-1])[0])))

                if "'" in lex_line or "'" in dis_line:
                    # con_conb.append('{}\n{}\n{}\n{}\n\n'.format('Filename: '+ file_name_final,'record_index: '+str(record_line),'lexical_word: '+lex_line,'display_word: ' +dis_line))
                    con_conb.append('{}\n{}\n{}\n\n'.format('Filename: '+ file_name_final,'lexical_word: '+lex_line,'display_word: ' +dis_line))
                elif re.findall('\d',dis_line):
                    # select_num_list.append('{}\n{}\n{}\n{}\n\n'.format('Filename: '+ file_name_final,'record_index: '+str(record_line),'lexical_word: '+lex_line,'display_word: ' +dis_line))
                    if str(dis_line) not in select_num_list.keys():
                        # print(dis_line)
                        select_num_list[str(dis_line)] = [[lex_line],[file_name_final]]
                    else:
                        select_num_list[str(dis_line)][0].append(lex_line)
                        select_num_list[str(dis_line)][1].append(file_name_final)
                else:
                    with open(os.path.join(outputpath,'differ_between_NonPName_and_PName.txt'),'a+',encoding="UTF8") as sav:
                        # sav.write('{}\n{}\n{}\n{}\n\n'.format('Filename: '+ file_name_final,'record_index: '+str(record_line),'lexical_word: '+lex_line,'display_word: ' +dis_line))
                        sav.write('{}\n{}\n{}\n\n'.format('Filename: '+ file_name_final,'lexical_word: '+lex_line,'display_word: ' +dis_line))

        else:
            print(key_lex,'不存在于第二个输入中')
            sys.exit()

    for con_cob in con_conb:
        with open(os.path.join(outputpath,'differ_between_NonPName_and_PName.txt'),'a+',encoding="UTF8") as sav:
            sav.write(con_cob)
    if len(select_num_list) != 0:
        # print(type(select_num_list))
        with open(os.path.join(outputpath,'differ_between_NonPName_and_PName.txt'),'a+',encoding="UTF8") as sav:
            sav.write(json.dumps(select_num_list))    


 
    #         merge_info = compare_diff(key_lex,value_lex,data_info_txt[key_lex],outputpath)  #{48: ['osmdesát', '80'], 49: ['procent', '%']}
    #         if len(merge_info) > 0:
    #             # print('mergr_info:',merge_info)
                
    #             differ_return=[]#,select_num_list = [],[]   #两个返回值，数字和非数字区分开
    #             merge_info_key = [int(x) for x in merge_info.keys()]

    #             record_line,lex_line,dis_line = '','',''
    #             for ind_sav,(sav_key,sav_value) in enumerate(merge_info.items()):
    #                 if ind_sav == 0:
    #                     record_line = sav_key
    #                     lex_line = sav_value[0]
    #                     dis_line = sav_value[1]
    #                 elif ind_sav < len(merge_info):
    #                     if abs(merge_info_key[ind_sav-1]-int(sav_key)) == 1:
    #                         record_line = '{} {}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
    #                         lex_line = '{} {}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
    #                         dis_line = '{} {}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 
    #                     else:
    #                         record_line = '{}\t{}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
    #                         lex_line = '{}\t{}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
    #                         dis_line = '{}\t{}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 

    #             # print('record_line',record_line)
    #             # print('lex_line',lex_line)
    #             # print('dis_line',dis_line)
    #             file_name_final = '_'.join(key_lex.split('_')[:-1])
    #             file_name_final = file_name_final + ' 第{}行'.format(str(int(os.path.splitext(key_lex.split('_')[-1])[0])))

    #             if "'" in lex_line or "'" in dis_line:
    #                 # con_conb.append('{}\n{}\n{}\n{}\n\n'.format('Filename: '+ file_name_final,'record_index: '+str(record_line),'lexical_word: '+lex_line,'display_word: ' +dis_line))
    #                 con_conb.append('{}\n{}\n{}\n\n'.format('Filename: '+ file_name_final,'lexical_word: '+lex_line,'display_word: ' +dis_line))
    #             elif re.findall('\d',dis_line):
    #                 recode_contain_num = ['','']
    #                 recode_Notcontain_num = ['','']
    #                 if len(dis_line.strip().split('\t')) == len(lex_line.strip().split('\t')):

    #                     for order_dis,dis_word_per in enumerate(dis_line.strip().split('\t')):
    #                         if re.findall('\d',dis_word_per):
    #                             recode_contain_num[1] = '{} {}'.format(recode_contain_num[1],dis_word_per)
    #                             recode_contain_num[0] = '{} {}'.format(recode_contain_num[0],lex_line.strip().split('\t')[order_dis])
    #                         else:
    #                             recode_Notcontain_num[1] = '{} {}'.format(recode_Notcontain_num[1],dis_word_per)
    #                             recode_Notcontain_num[0] = '{} {}'.format(recode_Notcontain_num[0],lex_line.strip().split('\t')[order_dis])

    #                     if str(recode_contain_num[1]) not in select_num_list.keys():
    #                         # print(dis_line)
    #                         select_num_list[str(recode_contain_num[1])] = [[recode_contain_num[0]],[file_name_final]]
    #                     else:
    #                         select_num_list[str(recode_contain_num[1])][0].append(recode_contain_num[0])
    #                         select_num_list[str(recode_contain_num[1])][1].append(file_name_final)

    #                     if recode_Notcontain_num[0].strip() != '' or recode_Notcontain_num[1].strip() != '':
    #                         with open(os.path.join(outputpath,'differ_between_NonPName_and_PName.txt'),'a+',encoding="UTF8") as sav:
    #                             sav.write('{}\n{}\n{}\n\n'.format('Filename: '+ file_name_final,'lexical_word: '+recode_Notcontain_num[0],'display_word: ' +recode_Notcontain_num[1]))
    #                 else:
    #                     print('格式整顿后lexical 和display数目不匹配')
    #                     print('lexical:',lex_line.strip().split('\t'))
    #                     print('display:',dis_line.strip().split('\t'))
    #                     # sys.exit()
    #                     if str(dis_line) not in select_num_list.keys():
    #                         # print(dis_line)
    #                         select_num_list[str(dis_line)] = [[lex_line],[file_name_final]]
    #                     else:
    #                         select_num_list[str(dis_line)][0].append(lex_line)
    #                         select_num_list[str(dis_line)][1].append(file_name_final)


    #             else:
    #                 with open(os.path.join(outputpath,'differ_between_NonPName_and_PName.txt'),'a+',encoding="UTF8") as sav:
    #                     sav.write('{}\n{}\n{}\n\n'.format('Filename: '+ file_name_final,'lexical_word: '+lex_line,'display_word: ' +dis_line))

    #     else:
    #         print(key_lex,'不存在于第二个输入中')
    #         sys.exit()

    # for con_cob in con_conb:
    #     with open(os.path.join(outputpath,'differ_between_NonPName_and_PName.txt'),'a+',encoding="UTF8") as sav:
    #         sav.write(con_cob)
    # if len(select_num_list) != 0:
    #     # print(type(select_num_list))
    #     with open(os.path.join(outputpath,'differ_between_NonPName_and_PName.txt'),'a+',encoding="UTF8") as sav:
    #         sav.write(json.dumps(select_num_list))    


    # for num_L_W in select_num_list:

    #     with open(os.path.join(outputpath,'differ_between_lexical_and_display.txt'),'a+',encoding="UTF8") as sav:
    #         sav.write(num_L_W)


            # for ind,single_value_lex in enumerate(value_lex):   #single_value_lex: [full_name,start,end,trans]
            #     if single_value_lex[0] in [x[0] for x in trans_folder['display_format'][key_lex]]:
            #         #在filename 能对上的情况下，比较时间戳信息
            #         for single_dis_info_list in trans_folder['display_format'][key_lex]:
            #             if single_value_lex[0] == single_dis_info_list[0]:
            #                 final_dict[single_value_lex[0]] = [single_value_lex[1],single_value_lex[2],single_value_lex[3],single_dis_info_list[3]]
                            #==============================compare lexical and display trans=============================================
                            # merge_info = compare_diff(single_value_lex[0],single_value_lex[3],single_dis_info_list[3],outputpath)  #{48: ['osmdesát', '80'], 49: ['procent', '%']}
                            # if not os.path.exists(outputpath):
                            #     os.mkdir(outputpath)

                            # if len(merge_info) > 0:
                            #     print('mergr_info:',merge_info)
                                
                            #     merge_info_key = [int(x) for x in merge_info.keys()]
                            #     with open(os.path.join(outputpath,'lexical_display_differ_all.txt'),'a+',encoding='UTF8') as sav:
                            #         record_line,lex_line,dis_line = '','',''
                            #         for ind_sav,(sav_key,sav_value) in enumerate(merge_info.items()):
                            #             if ind_sav == 0:
                            #                 record_line = sav_key
                            #                 lex_line = sav_value[0]
                            #                 dis_line = sav_value[1]
                            #             elif ind_sav < len(merge_info):
                            #                 if abs(merge_info_key[ind_sav-1]-int(sav_key)) == 1:
                            #                     record_line = '{} {: <{}}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
                            #                     lex_line = '{} {: <{}}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
                            #                     dis_line = '{} {: <{}}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 
                            #                 else:
                            #                     record_line = '{}\t{: <{}}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
                            #                     lex_line = '{}\t{: <{}}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
                            #                     dis_line = '{}\t{: <{}}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 

                            #         print('record_line',record_line)
                            #         print('lex_line',lex_line)
                            #         print('dis_line',dis_line)
                            #         if re.findall('\d',dis_line):
                            #             select_num_list.append('Filename:{}\nlexical_word:{}\ndisplay_word:{}\n\n'.format(single_value_lex[0],lex_line,dis_line))
                            #         else:
                            #             sav.write('Filename:{}\nlexical_word:{}\ndisplay_word:{}\n\n'.format(single_value_lex[0],lex_line,dis_line))

                            #     left_lenth = len([sav_value[0] for ind_sav,(sav_key,sav_value) in enumerate(merge_info.items()) if sav_value[0].strip() != ''])
                            #     right_lenth = len([sav_value[1] for ind_sav,(sav_key,sav_value) in enumerate(merge_info.items()) if sav_value[1].strip() != ''])
                            #     record_del = []
                            #     # record_num_line,lex_num_line,dis_num_line = [],[],[]
                            #     for ind_sav,(sav_key,sav_value) in enumerate(merge_info.items()):
                            #         # if sav_value[1].isdigit() and sav_value[0].strip() != '' and left_lenth== right_lenth and len(merge_info.items()) == 1:
                            #         #     count_skip+=1
                            #         #     if sav_value[1] not in select_num.keys():
                            #         #         select_num[sav_value[1]] = [sav_value[0]] #[sav_value[0],[single_value_lex[0]]]
                            #         #     elif sav_value[0] not in select_num[sav_value[1]]:
                            #         #         select_num[sav_value[1]].append(sav_value[0])
                            #         #     record_del.append(sav_key)
                            #         # elif sav_value[1].isdigit() and sav_value[0].strip() != '' and left_lenth== right_lenth:
                            #         #     if sav_value[1] not in select_num_2.keys():
                            #         #         select_num_2[sav_value[1]] = [sav_value[0]] #[sav_value[0],[single_value_lex[0]]]
                            #         #     elif sav_value[0] not in select_num_2[sav_value[1]]:
                            #         #         select_num_2[sav_value[1]].append(sav_value[0])
                            #         if sav_value[1].isdigit() and sav_value[0].strip() != '' and left_lenth== right_lenth and len(merge_info.items()) == 1:
                            #             count_skip+=1
                            #             if sav_value[1] not in select_num.keys():
                            #                 select_num[sav_value[1]] = [[sav_value[0]],[single_value_lex[0]]] #[sav_value[0],[single_value_lex[0]]]
                            #             elif sav_value[0] not in select_num[sav_value[1]][0]:
                            #                 select_num[sav_value[1]][0].append(sav_value[0])
                            #                 select_num[sav_value[1]][1].append(single_value_lex[0])
                            #             record_del.append(sav_key)

                            #         elif sav_value[1].isdigit() and sav_value[0].strip() != '' and left_lenth== right_lenth: #or [x for k_c,v_c in merge_info.items() ]:
                            #             if sav_value[1] not in select_num_2.keys():
                            #                 select_num_2[sav_value[1]] = [[sav_value[0]],[single_value_lex[0]]] #[sav_value[0],[single_value_lex[0]]]
                            #             elif sav_value[0] not in select_num_2[sav_value[1]][0]:    #{key:[[],[]]}
                            #                 select_num_2[sav_value[1]][0].append(sav_value[0])
                            #                 select_num_2[sav_value[1]][1].append(single_value_lex[0])
                            #             record_del.append(sav_key)
                                    
                            #         elif sav_value[1].isdigit():
                            #             if sav_value[1] not in select_num_3.keys():
                            #                 select_num_3[sav_value[1]] = [[sav_value[0]],[single_value_lex[0]]] #[sav_value[0],[single_value_lex[0]]]
                            #             elif sav_value[0] not in select_num_3[sav_value[1]][0]:    #{key:[[],[]]}
                            #                 select_num_3[sav_value[1]][0].append(sav_value[0])
                            #                 select_num_3[sav_value[1]][1].append(single_value_lex[0])
                            #             record_del.append(sav_key)

                                    
                            #         # else:
                            #         #     need_check_num_list
                            #         #     record_line = '{}\t{: <{}}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
                            #         #     lex_line = '{}\t{: <{}}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
                            #         #     dis_line = '{}\t{: <{}}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 

                            # print(len(merge_info))
                            # print('High accuracy pair:',[[key_num,value_num[0]] for key_num,value_num in select_num.items()])
                            # print('High accuracy filename:',[[key_num,value_num[1]] for key_num,value_num in select_num.items()])
                            # print('low accuracy pair:',[[key_num,value_num[0]] for key_num,value_num in select_num_2.items()])
                            # print('low accuracy filename:',[[key_num,value_num[1]] for key_num,value_num in select_num_2.items()])
                            # print('other pair:',[[key_num,value_num[0]] for key_num,value_num in select_num_3.items()])
                            # print('other filename:',[[key_num,value_num[1]] for key_num,value_num in select_num_3.items()])
                                # print('select_num----------',select_num,count_skip)
                                # print('select num 2----------------',select_num_2,record_del)
    


                            #============================================================================================================
    #                         if single_value_lex[1] == single_dis_info_list[1] and single_value_lex[2] == single_dis_info_list[2]:
    #                             trans_folder['display_format'][key_lex].remove(single_dis_info_list)
    #                             # flag_lexical_info[key_lex].remove(single_value_lex)
    #                         else:
    #                             #只print, 数据还是写入
    #                             print('{}的时间戳对不上{} {}'.format(single_value_lex[0],single_value_lex[1]+' '+single_value_lex[2],single_dis_info_list[1]+' '+single_dis_info_list[2]))
    #                     break

    # disTransAfterDel = [x for x in trans_folder['display_format'].values() if x != []]
    # if disTransAfterDel != []:
    #     print('时间戳(或code逻辑错误)对不上的utts:',disTransAfterDel)

    # if len(select_num_list):
    #     for i,single_error in enumerate(select_num_list):
    #         with open(os.path.join(outputpath,'lexical_display_differ_all.txt'),'a+',encoding='UTF8') as sav:
    #             if i == 0:
    #                 sav.write('-----------------------------------contain num-------------------------------\n')
    #             else:
    #                 sav.write(single_error)
    # num_info_write(os.path.join(outputpath,'only_num_info.txt'),[[key_num,value_num[0]] for key_num,value_num in select_num.items()],"High accuracy pair")
    # num_info_write(os.path.join(outputpath,'only_num_info.txt'),[[key_num,value_num[1]] for key_num,value_num in select_num.items()],"High accuracy filename")
    # num_info_write(os.path.join(outputpath,'only_num_info.txt'),[[key_num,value_num[0]] for key_num,value_num in select_num_2.items()],"low accuracy pair")
    # num_info_write(os.path.join(outputpath,'only_num_info.txt'),[[key_num,value_num[1]] for key_num,value_num in select_num_2.items()],"low accuracy filename")
    # num_info_write(os.path.join(outputpath,'only_num_info.txt'),[[key_num,value_num[0]] for key_num,value_num in select_num_3.items()],"other pair")
    # num_info_write(os.path.join(outputpath,'only_num_info.txt'),[[key_num,value_num[1]] for key_num,value_num in select_num_3.items()],"other filename")
    
                            # print('High accuracy pair:',[[key_num,value_num[0]] for key_num,value_num in select_num.items()])
                            # print('High accuracy filename:',[[key_num,value_num[1]] for key_num,value_num in select_num.items()])
                            # print('low accuracy pair:',[[key_num,value_num[0]] for key_num,value_num in select_num_2.items()])
                            # print('low accuracy filename:',[[key_num,value_num[1]] for key_num,value_num in select_num_2.items()])
    #===============save carbon file===================================================================
    # for final_key,final_value in final_dict.items():
    #     if not os.path.exists(os.path.join(inputpath,'audio_piece',os.path.splitext(final_key)[0].rsplit('_',1)[0],final_key)):
    #         print('音频不存在：',os.path.join(inputpath,'audio_piece',os.path.splitext(final_key)[0].rsplit('_',1)[0],final_key))
    #     else:

    # #         #carbon save
    # #         wav_path = os.path.join(inputpath,'audio_piece',os.path.splitext(final_key)[0].rsplit('_',1)[0],final_key)
    # #         if not os.path.exists(os.path.join('\\'.join(outputpath.split('\\')[:-1]),'carbon')):
    # #             os.mkdir(os.path.join('\\'.join(outputpath.split('\\')[:-1]),'carbon'))
           
    # #         with open(os.path.join('\\'.join(outputpath.split('\\')[:-1]),'carbon','carbon_lexical_input.txt'),'a+',encoding='UTF8') as sav_carbon_lex:
    # #             sav_carbon_lex.write('{}\t{}\n'.format(wav_path,final_value[2]))
    # #         with open(os.path.join('\\'.join(outputpath.split('\\')[:-1]),'carbon','carbon_display_input.txt'),'a+',encoding='UTF8') as sav_carbon_dis:
    # #             sav_carbon_dis.write('{}\t{}\n'.format(wav_path,final_value[3]))
    # #         with open(os.path.join('\\'.join(outputpath.split('\\')[:-1]),'carbon','all_trans.txt'),'a+',encoding='UTF8') as sav_all_trans:
    # #             sav_all_trans.write('{}\t{}\t{}\n'.format(wav_path,final_value[2],final_value[3]))

    # #====================================================================================================
    #         # verify save
    #         # 文件给的时间戳仅是为了满足格式给的假的
    #         if not os.path.exists(os.path.join(outputpath,'verify')):
    #             os.mkdir(os.path.join(outputpath,'verify'))
    #         if not os.path.exists(os.path.join(outputpath,'verify','verify_lexical')):
    #             os.mkdir(os.path.join(outputpath,'verify','verify_lexical'))
    #         if not os.path.exists(os.path.join(outputpath,'verify','verify_display')):
    #             os.mkdir(os.path.join(outputpath,'verify','verify_display'))

    #         # print(os.path.join(outputpath,'verify_tsv'))
    #         with open(os.path.join(outputpath,'verify','verify_lexical',final_key.replace('.wav','.tsv')),'a+',encoding='UTF8') as sav_verify_lex:
    #             sav_verify_lex.write('[{} {}] {} {}\n'.format('0','1','s1',final_value[2]))
    #         with open(os.path.join(outputpath,'verify','verify_display',final_key.replace('.wav','.tsv')),'a+',encoding='UTF8') as sav_verify_dis:
    #             sav_verify_dis.write('[{} {}] {} {}\n'.format('0','1','s1',final_value[3]))
    
    # # #copy wave
    # # import shutil
    # # shutil.copytree(os.path.join(inputpath,'audio_piece'))

    # # print(trans_folder['display_format'])
    # print(flag_lexical_info)

                    # print(single_value_lex[1] , trans_folder['display_format'][key_lex])#[single_value_lex[0]])
                    # if single_value_lex[1] == trans_folder['display_format'][key_lex][single_value_lex[0]][1]:
                    #     print(single_value_lex[1] , trans_folder['display_format'][key_lex][single_value_lex[0]][1])

        # for j,(key_dis,value_dis) in enumerate(trans_folder['display_format'].items()):
            
    # print(trans_folder['display_format'])      
        # if sorted(v_ind) != [x for x in v_ind.keys()]:
        #     print('original transcription file: segment ID disorder: {} {}\n乱序{}\t保存顺序{}\n'.format(test_type,key_ind,[x for x in v_ind.keys()],sorted(v_ind)))
        # if diff_list(sorted(v_ind)):
        #     print('有缺省的segment ID')
        # for ind_k in sorted(v_ind):
        #     sav_single_trans = '{} {}'.format(sav_single_trans,v_ind[ind_k])
        # all_trans.append('{}{}\t{}'.format(key_ind,'.wav',sav_single_trans)) 
def num_info_write(sav_p,info_list,desc):
    with open(sav_p,'a+',encoding='UTF8') as sav:
        sav.write('-'*10+desc+'\n')
        for i,single_error in enumerate(info_list):
            sav.write('{}\t{}\n'.format(single_error[0],single_error[1]))
    

def check_tag_info(trans,pattern):
    #########################check tag pair##################################################
    real_pair = 0
    error_pair = []

    tags_pair = re.compile("<{}>.*?</{}>".format(pattern,pattern)).findall(trans)
    # print(tags_pair)
    tags_pair_cap_low = re.compile("<{}>.*?</{}>".format(pattern,pattern)).findall(trans,re.IGNORECASE)#re.findall('<disfluency>.*?</disfluency>', trans,re.IGNORECASE)
    if len(tags_pair) != len(tags_pair_cap_low):
        print('tag大小写问题！！！！！')

    tag_left = re.compile("<{}>".format(pattern)).findall(trans)
    tag_right = re.compile("</{}>".format(pattern)).findall(trans)
    if len(tags_pair) == len(tag_left) and len(tags_pair) == len(tag_right):
        real_pair = len(tags_pair)
    else:
        real_pair = min(len(tags_pair),len(tag_left),len(tag_right))
        error_pair = [len(tags_pair),len(tag_left),len(tag_right)]
        print('tag 不成对：',error_pair)
    # print('存在tag对数：',real_pair)

    ###################split trans and tag with space#############################
    tag_split_content = list_trans(trans)
    # print('修改过trans文本和tag间隔为空格:',tag_split_content)
    return real_pair,tag_split_content


def list_trans(filename,trans):
    trans_pro = list(trans.replace(',',' ').replace('?',' ').replace('!',' ').replace(';',' ').replace('،',' ').replace('؟',' ').replace('-',' ').replace('¿',' ').replace('।',' ').replace('。', ' ').replace('、',' ').replace('，',' '))   #.replace('.',' ')
    #Ar --.replace('،',' ').replace('؟',' ')


    if not ((trans.count('<') == trans.count('>')) and (trans.count('>') == len(re.findall('<.*?>',trans)))):
        print(filename,'tag 括号不完整',trans)
    if len([x for x in re.findall('<.*?>',trans) if len(x)>10]) != 0:
        print('有错误风险的标签：',[x for x in re.findall('<.*?>',trans) if len(x)>10])
    for i,letter in enumerate(trans_pro):
        if i > 0 and i < len(trans_pro) - 1:
            if '<' == letter and trans_pro[i-1] != ' ':
                trans_pro.insert(i,' ')
            if '>' == letter and trans_pro[i+1] != ' ':
                trans_pro.insert(i+1,' ')

    #必须要确保tag的标注完全正确
    # trans_pro = [x for x in re.sub('<.*?>',' ',''.join(trans_pro)).split(' ') if x.strip()] #非空word list

    trans_pro = re.sub(r'\s+',' ', re.sub('<.*?>',' ',''.join(trans_pro))) #.replace('  ',' ').replace('  ',' ')
    trans_pro = [x for x in re.sub(r'\s+',' ', re.sub('<.*?>',' ',''.join(trans_pro))).split(' ') if x.strip()]
    # .split(' ') if x.strip()] #非空word list

    trans_pro = list(reversed(trans_pro))
    for order_l, single_char in enumerate(trans_pro):
        if single_char == '.':
            if order_l < len(trans_pro) - 1:
                if '.' not in trans_pro[order_l + 1]:
                    trans_pro[order_l + 1] = trans_pro[order_l + 1] + '.'
            trans_pro[order_l] = ''
        # elif single_char == "'s":
        #     if "'s" not in trans_pro[order_l + 1]:
        #             trans_pro[order_l + 1] = trans_pro[order_l + 1] + '.'
        #     trans_pro[order_l] = ''
            
 
    trans_pro = [x for x in list(reversed(trans_pro)) if x.strip()]
    print(trans_pro)
    
    #把类似 x. n. f. --> xnf
    #得到连接的index_list : [[2,3],[7,8,9]]
    # index_list,single_list = [],[]
    # for i,word in enumerate(trans_pro):
    #     if len(list(word.strip())) == 2 and list(word)[-1] == '.' and list(word)[0].isalpha():
    #         if not single_list:
    #             single_list.append(i)
    #         elif abs(i-single_list[-1]) == 1:
    #             single_list.append(i)
    #         elif len(single_list) > 1:
    #             index_list.append(single_list)
    #             single_list = [i]
    index_list,single_list = [],[]
    for i,word in enumerate(trans_pro):
        if len(list(word.strip())) == 2 and list(word)[-1] == '.' and list(word)[0].isalpha():
            if not single_list:
                single_list.append(i)
            elif abs(i-single_list[-1]) == 1:
                single_list.append(i)
            elif len(single_list) > 1:
                index_list.append(single_list)
                single_list = [i]
            else:
                single_list = [i]

    if len(single_list)>1:
        index_list.append(single_list)
    if len(index_list):
        for order in index_list[::-1]:  #倒着连接，不影响index的正确性
            ind_string = ''
            flag_ind = ''
            for ind in order:
                ind_string += trans_pro[ind].replace('.','')
            for ind in order[::-1]:
                trans_pro.pop(ind)
                flag_ind = ind
            trans_pro.insert(flag_ind,ind_string)
    
    print('111-----------',trans_pro)

    if "'s" in trans_pro or "s" in trans_pro:
        trans_pro = list(reversed(trans_pro))

        for ord_l, single_word in enumerate(trans_pro):
            if single_word == "'s" and ord_l < len(trans_pro) -1:
                if "'s" not in trans_pro[ord_l + 1]:
                    trans_pro[ord_l + 1] = trans_pro[ord_l + 1] + "'s"
                trans_pro[ord_l] = ''
            elif single_word == 's' and ord_l < len(trans_pro) -1:
                if "s" != trans_pro[ord_l + 1][-1]:
                    trans_pro[ord_l + 1] = trans_pro[ord_l + 1] + "s"
                trans_pro[ord_l] = ''

        # 
        # sys.exit()

        trans_pro = [x for x in list(reversed(trans_pro)) if x.strip()]
    # sys.exit()

    return ' '.join(trans_pro).replace('.','').replace('．','').split(' ')   #网址不能识别

def re_format_trans(trans):
    # combine_letter_dot
    print(trans)
    letter_dot_dict = {}
    trans_list = list(trans)
    for i,letter in enumerate(trans_list):
        if i > 0 and i < len(trans_list) - 1:
            if letter.isalpha() and trans_list[i-1].strip() == '' and find_dot(i,trans_list):
                # print(i,letter,trans_list)
                letter_dot_dict = {i:trans_list[i]}
    save_recode = ''
    # for i,(key_letter,value_letter) in enumerate(letter_dot_dict):
    #     if key_letter

    # return trans
def compute_diff(recode_dict):
    save_recode = []
    flag_continue = False
    for i,num in enumerate(recode_dict.items()):
        if abs(num - num_list[i+1]) <5:
            save_recode.append([])

def find_dot(index,trans_list):
    for i,letter in enumerate(trans_list):
        if i >  index:
            if trans_list[i].strip() == '':
                continue
            elif trans_list[i].strip() == '.':
                return True
            else:
                return False


def compare_diff(filename,lexical_trans,display_trans,outputpath):
    #去tag,合缩写词
    lex_remove_tag_list = [x for x in list_trans(filename,lexical_trans.lower()) if x.strip() != '']
    dis_remove_tag_list = [x for x in list_trans(filename,display_trans.lower()) if x.strip() != '']

    print(lex_remove_tag_list)
    print(dis_remove_tag_list)
    # sys.exit()


    ########compare char
    lex_part,dis_part = [],[]
    for ord_list,x in enumerate(lex_remove_tag_list):
        # flag = if 
        lex_part.extend([p for p in list(x) if p.strip()])
    for ord_list,x in enumerate(dis_remove_tag_list):
        dis_part.extend([p for p in list(x) if p.strip()])

    lex_remove_tag_list,dis_remove_tag_list = lex_part, dis_part

    # print(len(lex_remove_tag_list),len(dis_remove_tag_list))

    flag_locate = 0
    compare_ind = [[],[]]
    lex_dict,dis_dict = {},{}

    for i,lex_word in enumerate(lex_remove_tag_list):
        lex_dict[i] = [1,lex_word]  # 1作为比较word的flag
    for i,dis_word in enumerate(dis_remove_tag_list):
        dis_dict[i] = [1,dis_word]


    for i,(lex_key,lex_value) in enumerate(lex_dict.items()): #{order:[flag,word]，order:[flag,word]}
        for j,(dis_key,dis_value) in enumerate(dis_dict.items()):
            if dis_value[0] != 0:
                if abs(dis_key - lex_key) < max(5,abs(len(lex_value)-len(dis_value))) and j>i-5: #认为错词在5个以内(造成误差)，
                    if lex_value[1] == dis_value[1]:
                        lex_dict[lex_key][0] = 0
                        dis_dict[dis_key][0] = 0 
                        # print(lex_key,dis_key,dis_value[1])
                        break
    # print(filename)
    lex_only,dis_only,ind_info = {},{},[]
    for i,(lex_key,lex_value) in enumerate(lex_dict.items()):
        if lex_value[0] != 0:
            lex_only[lex_key] = lex_value[1]
            if lex_key not in ind_info:
                ind_info.append(lex_key)
    for j,(dis_key,dis_value) in enumerate(dis_dict.items()):
        if dis_value[0] != 0:
            dis_only[dis_key] = dis_value[1]
            if dis_key not in ind_info:
                 ind_info.append(dis_key)

    print('------------',ind_info)
    print('lex_omly--',lex_only)
    print('dis_only---------',dis_only)
    print(ind_info)

    # for common_key in list(set(lex_only.keys()) & set(dis_only.keys()) ):
    #     print(common_key,lex_only[common_key],dis_only[common_key])
    #     if '-' in lex_only[common_key] or '_' in dis_only[common_key]:
    #         print(re.sub(r'\s+',' ', lex_only[common_key].replace('-',' ')),  re.sub(r'\s+',' ', dis_only[common_key].replace('-',' ')))
    #         # sys.exit()
    #         import time
    #         time.sleep(5)
    #     if re.sub(r'\s+',' ', lex_only[common_key].replace('-',' ')) == re.sub(r'\s+',' ', dis_only[common_key].replace('-',' ')):
    #         lex_only.pop(l_s_order)
    #         dis_only.pop(l_s_order)
    #         sys.exit()
        # if '-' in lex_only[common_key] or '_' in dis_only[common_key]:
        #     sys.exit()

                #     l_s_list = lex_line.strip().split('\t')[::-1]
                # d_s_list = dis_line.strip().split('\t')[::-1]
                # copy_l_s_list,copy_d_s_list = l_s_list[:], d_s_list[:]
                # for l_s_order,l_s_word in enumerate(l_s_list):
                #     if re.sub(r'\s+',' ',l_s_word.replace('-',' ')) == re.sub(r'\s+',' ', d_s_list[l_s_order].replace('-',' ')):
                #         copy_l_s_list.pop(l_s_order)
                #         copy_d_s_list.pop(l_s_order)
                
                # if len(copy_l_s_list) != len(l_s_list):
                #     lex_line = '\t'.join(copy_l_s_list)
                #     dis_line = '\t'.join(copy_d_s_list)


    merge_recode = {}

    if len(lex_only) or len(dis_only):
        for i,ind_num in enumerate(sorted(ind_info)):  #[[3, 'dva'], [4, 'tisíce'], [5, 'dvacet']]
            
             merge_recode[ind_num] = [lex_only[ind_num] if ind_num in lex_only.keys() else '',dis_only[ind_num] if ind_num in dis_only.keys() else '']
        # print(merge_recode)   ##{48: ['osmdesát', '80'], 49: ['procent', '%']}
    # format_savediffer(filename,merge_recode,outputpath)
    
    return merge_recode
    # if not os.path.exists(outputpath):
    #     os.mkdir(outputpath)

con_conb = []
# select_num_list = []
def format_savediffer(filename,merge_info,outputpath):
    if len(merge_info) > 0:
        print('mergr_info:',merge_info)
         
        differ_return,select_num_list = [],[]   #两个返回值，数字和非数字区分开
        merge_info_key = [int(x) for x in merge_info.keys()]

        record_line,lex_line,dis_line = '','',''
        for ind_sav,(sav_key,sav_value) in enumerate(merge_info.items()):
            if ind_sav == 0:
                record_line = sav_key
                lex_line = sav_value[0]
                dis_line = sav_value[1]
            elif ind_sav < len(merge_info):
                # if abs(merge_info_key[ind_sav-1]-int(sav_key)) == 1:
                #     record_line = '{} {: <{}}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
                #     lex_line = '{} {: <{}}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
                #     dis_line = '{} {: <{}}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 
                # else:
                #     record_line = '{}\t{: <{}}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
                #     lex_line = '{}\t{: <{}}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
                #     dis_line = '{}\t{: <{}}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 
                if abs(merge_info_key[ind_sav-1]-int(sav_key)) == 1:
                    record_line = '{} {}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
                    lex_line = '{} {}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
                    dis_line = '{} {}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 
                else:
                    record_line = '{}\t{}'.format(record_line,sav_key,max(len(sav_value[0]),len(sav_value[1])))
                    lex_line = '{}\t{}'.format(lex_line,sav_value[0],max(len(sav_value[0]),len(sav_value[1])))
                    dis_line = '{}\t{}'.format(dis_line,sav_value[1],max(len(sav_value[0]),len(sav_value[1]))) 

        print('record_line',record_line)
        print('lex_line',lex_line)
        print('dis_line',dis_line)
        if re.findall('\d',dis_line):
            select_num_list.append('Filename:{}\nlexical_word:{}\ndisplay_word:{}\n\n'.format(filename,lex_line,dis_line))
        # else:
        #     differ_return.append('Filename:{}\nlexical_word:{}\ndisplay_word:{}\n\n'.format(filename,lex_line,dis_line))
        # if "'" in lex_line or "'" in dis_line:
        #     con_conb.append('{}\n{}\n{}\n{}\n\n'.format('Filename: '+filename,'record_index: '+str(record_line),'display_word: '+lex_line,'displayEntity_word: ' +dis_line))
        else:
            with open(os.path.join(outputpath,'differ_between_twofiles.txt'),'a+',encoding="UTF8") as sav:
                sav.write('{}\n{}\n{}\n{}\n\n'.format('Filename: '+filename,'record_index: '+str(record_line),'lexical_word:: '+lex_line,'display_word: ' +dis_line))
    return select_num_list
# print(select_num_list)
    # print(differ_return)

        # left_lenth = len([sav_value[0] for ind_sav,(sav_key,sav_value) in enumerate(merge_info.items()) if sav_value[0].strip() != ''])
        # right_lenth = len([sav_value[1] for ind_sav,(sav_key,sav_value) in enumerate(merge_info.items()) if sav_value[1].strip() != ''])
        # record_del = []
        # for ind_sav,(sav_key,sav_value) in enumerate(merge_info.items()):
        #     if sav_value[1].isdigit() and sav_value[0].strip() != '' and left_lenth== right_lenth and len(merge_info.items()) == 1:
        #         count_skip+=1
        #         if sav_value[1] not in select_num.keys():
        #             select_num[sav_value[1]] = [[sav_value[0]],[filename]] #[sav_value[0],[single_value_lex[0]]]
        #         elif sav_value[0] not in select_num[sav_value[1]][0]:
        #             select_num[sav_value[1]][0].append(sav_value[0])
        #             select_num[sav_value[1]][1].append(filename)
        #         record_del.append(sav_key)

        #     elif sav_value[1].isdigit() and sav_value[0].strip() != '' and left_lenth== right_lenth: #or [x for k_c,v_c in merge_info.items() ]:
        #         if sav_value[1] not in select_num_2.keys():
        #             select_num_2[sav_value[1]] = [[sav_value[0]],[filename]] #[sav_value[0],[single_value_lex[0]]]
        #         elif sav_value[0] not in select_num_2[sav_value[1]][0]:    #{key:[[],[]]}
        #             select_num_2[sav_value[1]][0].append(sav_value[0])
        #             select_num_2[sav_value[1]][1].append(filename)
        #         record_del.append(sav_key)
            
        #     elif sav_value[1].isdigit():
        #         if sav_value[1] not in select_num_3.keys():
        #             select_num_3[sav_value[1]] = [[sav_value[0]],[filename]] #[sav_value[0],[single_value_lex[0]]]
        #         elif sav_value[0] not in select_num_3[sav_value[1]][0]:    #{key:[[],[]]}
        #             select_num_3[sav_value[1]][0].append(sav_value[0])
        #             select_num_3[sav_value[1]][1].append(filename)
        #         record_del.append(sav_key)

    # print(len(merge_info))
    # return merge_recode #{48: ['osmdesát', '80'], 49: ['procent', '%']}
                






        # print(list(lex_value[1].strip()))

    # lex_only = [[lex_key,lex_value[1]] for i,lex_value in enumerate(lex_only) if  len(lex_value[1])!= 0]
    # dis_only = [[dis_key,dis_value[1]] for j,dis_value in enumerate(dis_only) if dis_value[0] != 0]



    # if lex_only and dis_only:
    #     for i,lex_list in enumerate(lex_only):





    # print(lex_dict)
    # flag_lexical = lex_remove_tag_list
    # flag_display = dis_remove_tag_list
    # for i,lex_word in enumerate(lex_remove_tag_list):
    #     for j,dis_word in enumerate(dis_remove_tag_list):
    #         if j - i < 5:
    #             if lex_word == dis_word:
    #                 flag = j - i
    #                 compare_ind[0],compare_ind[1] = i,j
    #                 del flag_lexical[i]
    #                 del flag_display[j]

    #                 break
    #     # if flag_locate <= 1:
    # print(flag_lexical,flag_display)

    
    # import time
    # time.sleep(1000)


    
def correspond_carbonresult_to_speechinsight(inputpath1,inputpath2,outputpath):
    carbon_info = {}
    with open(inputpath1,'r',encoding='UTF8') as f:
        for i,line in enumerate(f):
            if i== 0 and line.strip().startswith('Audio'):
                continue
            Audio,Transcription,Lexical,Display,TrafficType_SessionID = line.strip().split('\t')
            carbon_info[Audio.strip()] = [Transcription,Lexical,Display]
    
    with open(inputpath2,'r',encoding='UTF8') as f1:
        for i,line in enumerate(f1):
            Audio_name,display_input = line.strip().split('\t')
            if Audio_name.strip() in carbon_info.keys():
                with open(outputpath,'a+',encoding='UTF8') as sav:
                    sav.write('{}\t{}\t{}\t{}\t{}\n'.format(Audio_name.strip(),carbon_info[Audio_name.strip()][0],display_input,carbon_info[Audio_name.strip()][1],carbon_info[Audio_name.strip()][2]))
                del(carbon_info[Audio_name.strip()])
            else:
                print('{}不存在于carbon输出文件'.format(Audio_name))
    if len(carbon_info) != 0:
        print('carbon中未匹配display的条',carbon_info)



def diff_list(input_list):
    for order,con in enumerate(input_list):
        if order < len(input_list) - 1:
            if abs(int(con)-int(input_list[order+1])) != 1:
                return True
    return False

def generate_carbonInput_And_transTSV(inputpath,outputpath):
    print(2)


input = sys.argv[1]
output = sys.argv[2]
# flag = sys.argv[3]


# input = r"E:\v-yuhangxing\data\Dictation_Data_Collection-FY23-iSoftstone\24\0618\verify\test"
# output = r"E:\v-yuhangxing\data\Dictation_Data_Collection-FY23-iSoftstone\24\0618\Compare"
flag = str(1)


if flag == '1':
    check_lexicalAndDisplay_consistent(input,output)
# elif flag == '2':
#     generate_carbonInput_And_transTSV(input,output)
