import sys,os,re,json
import copy

#=============================extract information from ingested file=========================================

#============================注册文件格式会修改，code应该还要修改，也许还要关于TranscriptionSource的判断
#test data: E:\v-yuhangxing\tool\simple_tool\summary_way_to_process_data\test_file\extract_information_from_ingested_file\1b822e0b-fff7-4075-90be-70032f3eddf2\1b822e0b-fff7-4075-90be-70032f3eddf2_0_DatasetMeta.json
def extract_information_from_ingested_file_1(fp,output):
    info_list = {}
    CompareKey_set = []
    read_trans = None
    data_info_all = {}
    single_per_all_count = 0
    respond_key = {}
    with open(fp,'r',encoding='utf-8-sig') as fr:
        data = json.load(fr)
    # try:
        
        # DatasetID = data["DatasetId"]
        body = data["ListOfUtterances"]
        for con in body:
            data_info = {}
            CompareKey = con["CompareKey"]
            lex_trans = con["Transcription"]
            lexi_trans = False
            # print(lex_trans)
            lex_pattern =  {
                        "ResultType": "Transcription",
                        "ResultSubtype": 'Lexical',
                        "TranscriptionSystem": "Official",
                        "NewTranscriptionSystem": "Official",
                        "Transcription": lex_trans,
                        }
        
            for single_pair in con["AdditionalTranscription"]:
                if single_pair["TranscriptionSource"] == "OfflineIngestion" or single_pair["TranscriptionSource"] == "ISS_PublicData_VFY23Q1_20240401":
                    lexi_trans = single_pair["Transcription"]

            wav,display_trans = False,False
            for single_pair in con['MetaData']:

                if single_pair['Key'] == 'CompareKey':
                    wav = single_pair['Value']
                    break
            # for single_pair in con['MetaData']:
            #     if single_pair['Key'] == 'DisplayTranscription':
            #         display_trans = single_pair['Value']
            #         break
            # if wav and display_trans:
            #if not os.path.exists(os.path.join(output,'ori')):
            #    os.mkdir(os.path.join(output,'ori'))
            #if not os.path.exists(os.path.join(output,'updated')):
            #    os.mkdir(os.path.join(output,'updated'))    

            if wav and lexi_trans:
                single_per_all_count += 1
                with open(os.path.join(output,os.path.splitext(os.path.basename(fp))[0]+'.tsv'),'a+',encoding= 'UTF8') as sav:
                    # sav.write(wav+'.wav'+'\t'+lexi_trans+'\t'+lex_trans+'\n')
                    sav.write(wav+'.wav'+'\t'+lexi_trans+'\n')
                # with open(os.path.join(output,'display_transcription.tsv'),'a+',encoding= 'UTF8') as sav:
                #     sav.write(wav+'.wav'+'\t'+display_trans+'\n')
                    
            # if wav and lex_trans:
            #     with open(os.path.join(output,'lexical',os.path.splitext(os.path.basename(fp))[0]+'.tsv'),'a+',encoding= 'UTF8') as sav:
            #         sav.write(wav+'\t'+lex_trans+'\n') 
            # if lexi_trans:
            #     with open(os.path.join(output,'ori',os.path.splitext(os.path.basename(fp))[0]+'.tsv'),'a+',encoding= 'UTF8') as sav:
            #         sav.write(wav+'.wav'+'\t'+lexi_trans+'\n') 

    # print(respond_key)
    print('总共保存{}个comparekey'.format(single_per_all_count))
    if single_per_all_count == 0:
        print(fp)
    return respond_key

def extract_information_from_ingested_file(fp):
    info_list = {}
    CompareKey_set = []
    read_trans = None
    data_info_all = {}
    single_per_all_count = 0
    respond_key = {}
    with open(fp,'r',encoding='utf-8-sig') as fr:
        data = json.load(fr)
    # try:
        
        # DatasetID = data["DatasetId"]
        body = data["ListOfUtterances"]
        for con in body:
            data_info = {}
            CompareKey = con["CompareKey"]
            lex_trans = con["Transcription"]
            lex_pattern =  {
                        "ResultType": "Transcription",
                        "ResultSubtype": 'Lexical',
                        "TranscriptionSystem": "Official",
                        "NewTranscriptionSystem": "Official",
                        "Transcription": lex_trans,
                        }
            lex_system_pattern =  {
                        "ResultType": "Transcription",
                        "ResultSubtype": 'Lexical',
                        "TranscriptionSystem": "OfflineIngestion",
                        "NewTranscriptionSystem": "PT_PD_VFY24Q2_20240605",
                        "Transcription": lex_trans,
                        }
            for single_pair in con['MetaData']:
                if single_pair['Key'] == 'SessionId':#'CompareKey':# 'SessionId':#'CompareKey':
                    wav = single_pair['Value']
                # if single_pair['Key'] == 'UtteranceId':
                #     wav = single_pair['Value']
                    respond_key[wav] = {CompareKey:[lex_system_pattern,lex_pattern]}  #{CompareKey:{}}
                    break
    # print(respond_key)
    print('总共保存{}个comparekey'.format(len(respond_key.keys())))
    return respond_key

replace_tag = [[],[]]
def multiple_replace(text, myDict):
    for key, val in myDict.items():
        if re.search(key, text):
            text = re.sub(key, val, text)
            replace_tag[0].append(key)
            replace_tag[1].append(val)
    return text

MAGIC_TAGS = {
    r'<lang:English>' : "",
    r'</lang:English>' : "",
    r'<lang:Foreign>' : "",
    r'</lang:Foreign>' : "",
    r'<lang:Russian>' : "",
    r'</lang:Russian>' : "",
    r'<initial>' : "",
    r'</initial>' : "",
    r'\[no-speech\]' : "",
    r'\[overlap\]' : " ",
    r'#aa' : "<SN/>",
    r'#ee' : "<SN/>",
    r'#mm' : "<SN/>",
    r'#uu' : "<SN/>",
    r'\[lipsmack\]' : "<SN/>",
    r'\[noise\]' : "<SN/>",
    r'\[laugh\]' : "<SN/>",
    r'\[breath\]' : "<SN/>",
    r'\[cough\]': "<SN/>",
    r'\[applause\]' : "<SN/>",
    r'\(\(\)\)' : "<UNKNOWN/>",
    r'\[PCI\]' : "",
    r'#Uh' : "<FILL/>",
    r'#hm' : "<FILL/>",
    r'#uh' : "<FILL/>",
    r'#ah' : "<FILL/>",
    r'#um' : "<FILL/>",
    r"<SN>" : "<SN/>",
    r'<OVERLAP/>': "</OL>",
    r'<OVERLAP>': "<OL>",
    r'\[ASIDE\]': "",
    r'\[UNK\]': "<UNKNOWN/>",
    r"\[OVERLAP\]": "<OL>",
    r"\[OVERLAP/\]": "</OL>",
    r"\[MUSIC_P1\]": "",
    r"\[\*\]": "<UNKNOWN/>",
    r"\[TTSF\]": "",
    r"\[TTSM\]": "",
    r"\[LAUGH\]": "<SN/>",
    r"\[SONANT\]": "<SN/>",
    r"\[ENS\]": "<SN/>",
    r"\[MUSIC\]": "<SN/>",
    r"\[music]": "<SN/>",
    r"\[PI\]": "<PII/>",
    "<osp/>": "",
    r'<dt df\=.*?>': "",
    r'<ddt df\=.*?>': "",
    r'<dtdt df\=.*?>': "",
    r'</?dt/?>': "",
    # r"<(nsp)>(.*?)<\1/>": r"\2",
    '<nsp>': '',
    '<nsp/>': '',
}

def update_ingest_info(input_dict,update_dict,outputpath):    
    # pattern = {
    #     "CompareKey": CompareKey,
    #     "InputMediaReference": "",
    #     "EnrichmentResultNodes": 
    #     [
    #         {
    #             "ResultType": "Transcription",
    #             "ResultSubtype": ResultSubtype,
    #             "TranscriptionSystem": TranscriptionSystem,
    #             "NewTranscriptionSystem": NewTranscriptionSystem,
    #             "Transcription": Transcription
    #         }
    #     ]
    # }
    #input_dict: {'en-US-18-D1JTUI2AHFY': comparekey}   #{'386db319-4ea1-44eb-b58c-19fae5a3e312': {}},...}
    #update_dict: {'readability':{{wav:trans}},'disfluency':{}}
    copy_compare_dict = input_dict
    copy_update_dict = update_dict
    ingest_info = []
    read_pattern, disf_pattern = None,None
    flag_pattern = [0,0,0,0]
    
    flag_wav = [x for x in input_dict.keys()]
    flag_find = False

    flag_disf = [x for x in update_dict['disfluency'].keys()]
    flag_find_disf = False


    for wav_name,comparekey_v_info in input_dict.items():
        for comparekey_v,pattern_lex_v in comparekey_v_info.items():

            if 'readability' in update_dict.keys():
                for (update_k,update_v) in update_dict['readability'].items():
                    if wav_name == update_k:
                        read_pattern =  {
                                    "ResultType": "Transcription",
                                    "ResultSubtype": 'DisplayReadability',
                                    "TranscriptionSystem": "Official",
                                    "NewTranscriptionSystem": "Official",
                                    "Transcription": update_v,
                                    }
                        flag_find = True
                        break
            if 'disfluency' in update_dict.keys():
                for (update_k1,update_v1) in update_dict['disfluency'].items():
                        # print(update_v.keys())
                    if wav_name == update_k1:
                        disf_pattern =  {
                                    "ResultType": "Transcription",
                                    "ResultSubtype": 'DisplayVerbatim',
                                    "TranscriptionSystem": "Official",
                                    "NewTranscriptionSystem": "Official",
                                    "Transcription": update_v1,
                                    }
                        flag_find = True
                        flag_find_disf = update_k1
                        break

            if flag_find:
                flag_wav.remove(wav_name)
                flag_find = False

            if flag_find_disf:
                flag_disf.remove(flag_find_disf)
                flag_find_disf = False

            dis_m = copy.deepcopy(disf_pattern)
            dis_m["NewTranscriptionSystem"] = "PT_PD_VFY23Q3_20240827"
            dis_f = copy.deepcopy(read_pattern)
            dis_f["NewTranscriptionSystem"] = "PT_PD_VFY23Q3_20240827"
            if disf_pattern and read_pattern:
                flag_pattern[2] += 1
                ingest_info.append({
                                    "CompareKey": comparekey_v,
                                    "InputMediaReference": "",
                                    "EnrichmentResultNodes": 
                                    [
                                        # pattern_lex_v[1],
                                        # #pattern_lex_v,
                                        # pattern_lex_v[0],
                                        # disf_pattern,
                                        # read_pattern
                                        dis_m,
                                        disf_pattern,
                                        dis_f,
                                        read_pattern
                                    ]
                                })
                read_pattern = None
                disf_pattern = None
                continue
            if read_pattern:
                flag_pattern[0] += 1
                ingest_info.append( {
                                    "CompareKey": comparekey_v,
                                    "InputMediaReference": "",
                                    "EnrichmentResultNodes": 
                                    [   
                                        pattern_lex_v,
                                        read_pattern
                                    ]
                                })
                read_pattern = None
                disf_pattern = None
                continue
            if disf_pattern:
                flag_pattern[1] += 1
                ingest_info.append({
                                    "CompareKey": comparekey_v,
                                    "InputMediaReference": "",
                                    "EnrichmentResultNodes": 
                                    [
                                        pattern_lex_v,
                                        disf_pattern
                                    ]
                                })
                read_pattern = None
                disf_pattern = None
                continue

    if len(flag_wav) >0:
        print('注册文件中未匹配到的音频：',len(flag_wav),str(flag_wav))

    if len(flag_disf) >0:
        print('disf文件中未匹配到的音频：',len(flag_disf),str(flag_disf))
  
    for single_update_info in ingest_info:
        with open(outputpath,'a+',encoding='UTF8') as sav:
            sav.write(json.dumps(single_update_info)+'\n')
    print('更新trans有不同类型',flag_pattern)

    # # print(ingest_info)
    #                     json_save = json.dumps(single_nodes)#,ensure_ascii=False)
    #         sav_update.write(json_save+'\n')
        
        

            # if update
            # if wav_name in update_v.keys():
            #     print(wav_name)
            #     sys.exit()


    # comparekey_change,all_node = 0,0
    # change_source = {
    #     "Official":"ISS_PD_VFY24Q3",
    #     "ISS_PD_VFY24Q3_DT": "Official"
    # }
    # save_pattern = {}
    # for index,(CompareKey,index_v) in enumerate(info_dict.items()):    #compareKey,
    #     single_nodes = {
    #         "CompareKey": CompareKey,
    #         "InputMediaReference": "",
    #         "EnrichmentResultNodes": []
    #         }

    #     for ResultSubtype,single_info in index_v.items():  #trans_type, [[source,trans],[]]
    #         if ResultSubtype == 'DisplayVerbatim':
    #             for single_part_info in single_info:
    #                 if single_part_info[0] in change_source:

    #                     node_info = {
    #                                 "ResultType": "Transcription",
    #                                 "ResultSubtype": ResultSubtype,
    #                                 "TranscriptionSystem": single_part_info[0],
    #                                 "NewTranscriptionSystem": change_source[single_part_info[0]],
    #                                 "Transcription": single_part_info[1]
    #                             }
    #                     single_nodes["EnrichmentResultNodes"].append(node_info)
    #                     all_node += 1
                        

    #     with open(outputpath,'a+',encoding='UTF8') as sav_update:
    #         json_save = json.dumps(single_nodes)#,ensure_ascii=False)
    #         sav_update.write(json_save+'\n')
    #         comparekey_change += 1
    # print('总共保存{}个comparekey,{}个node'.format(comparekey_change,all_node))

def read_update_info(inputpath1):
    info_dict = {'readability':{},'disfluency':{}}
    for root,der,files in os.walk(inputpath1):
        for ord,file in enumerate(files):
            if ord >=3:
                print('输入文件个数过多')
                sys.exit()
            if 'read' in file.lower():
                with open(os.path.join(root,file),'r',encoding='UTF8') as f:
                    for i,line in enumerate(f):
                        filename,trans = line.strip().split('\t')
                        if filename.endswith('wav'):
                            filename = os.path.splitext(filename)[0]
                        # print(filename)
                        trans = multiple_replace(trans, myDict=MAGIC_TAGS)
                        info_dict["readability"][filename] = trans
            elif 'disf'  in file.lower():
                with open(os.path.join(root,file),'r',encoding='UTF8') as f1:
                    for i1,line1 in enumerate(f1):
                        filename,trans = line1.strip().split('\t')
                        if filename.endswith('.wav'):
                            filename = os.path.splitext(filename)[0]
                        trans = multiple_replace(trans, myDict=MAGIC_TAGS)
                        info_dict["disfluency"][filename] = trans
    
    if len(set(replace_tag[0])) or len(set(replace_tag[1])):
        print('replaced tag:',set(replace_tag[0]),set(replace_tag[1]))

    if info_dict['readability'] != {} and info_dict['disfluency'] != {}:
        if set([x for x in info_dict['readability'].keys()]) - set([x for x in info_dict['disfluency'].keys()]) or set([x for x in info_dict['disfluency'].keys()]) - set([x for x in info_dict['readability'].keys()]):
            print('更新不同种类的trans不完全成对：','\n',set([x for x in info_dict['readability'].keys()]) - set([x for x in info_dict['disfluency'].keys()]),'\n',set([x for x in info_dict['disfluency'].keys()]) - set([x for x in info_dict['readability'].keys()]))
            sys.exit()
    # print(info_dict['readability'].keys(),info_dict['disfluency'].keys())
    return info_dict





# for root,der,files in os.walk(sys.argv[1]):
#     for file in files:
#         extract_information_from_ingested_file_1(os.path.join(root,file),sys.argv[2])

inputpath = sys.argv[1]#r"E:\v-yuhangxing\data\FY24Q2-IS-Flexible-Data-Collection-TX\disfluency\240129\ori_ingest_file\d4578736-5332-4bff-96ab-1fe1eed1f8d6\d4578736-5332-4bff-96ab-1fe1eed1f8d6_0_DatasetMeta.json"
inputpath1 = sys.argv[2]##r"E:\v-yuhangxing\data\FY24Q2-IS-Flexible-Data-Collection-TX\disfluency\240129\update_file\en-US_BTEST_Conversation"
outputpath = sys.argv[3]##r"E:\v-yuhangxing\data\FY24Q2-IS-Flexible-Data-Collection-TX\disfluency\240129\update_file\Ingest_info\en-US_BTEST_Conversation.tsv"

info_dict = extract_information_from_ingested_file(inputpath)
# print(info_dict)
update_file_info = read_update_info(inputpath1)    
update_ingest_info(info_dict,update_file_info,outputpath)



###############save_ingest_info|保存注册文件的参数信息#######################################
# #############总结的字段没有写出来，想的是用字典统计
# for index,(index_k,index_v) in enumerate(info_dict.items()):    #compareKey,data_info
#     for trans_type,single_info in index_v.items():  #{type:{source:trans}}
#         # print('{}包含{}个source'.format(trans_type,len(single_info)))
#         for single_part_info_k,single_part_info_v in single_info.items():    #{source:trans}
                
#             with open(outputpath,'a+',encoding='UTF8') as sav:
#                 sav.write('{}\t{}\t{}\t{}\n'.format(index_k,trans_type,single_part_info_k,single_part_info_v))
###############========只生成原始格式的lexical 的字段############################################
# info_dict = extract_information_from_ingested_file(inputpath)
# for index,(index_k,index_v) in enumerate(info_dict.items()):
#     for (compareKey_single,pattern_lex_v) in index_v.items():
#         single_ingest_info = {
#                         "CompareKey": compareKey_single,
#                         "InputMediaReference": "",
#                         "EnrichmentResultNodes": 
#                         [
#                             pattern_lex_v
#                         ]
#                     }

#         with open(outputpath,'a+',encoding='UTF8') as sav:
#             sav.write(json.dumps(single_ingest_info)+'\n')

# sav.write(json.dumps(single_update_info)+'\n')
###############compare ingest | before-after================================================
# inputpath_after = r"E:\v-yuhangxing\data\FY24Q2-IS-Flexible-Data-Collection-TX\en-US_PPE_Ingest\2_step_test_update\959316ca-7769-4777-8d87-0ea3aae23eb4_prod_test_4_re_1\959316ca-7769-4777-8d87-0ea3aae23eb4_0_DatasetMeta_modify_test.json"
# info_dict_after = extract_information_from_ingested_file(inputpath_after)


# modify_info = {'TranscriptionSystem':[],'Transcription':[],'All_modify':[]}
# update_info = {}
# info_dict_ori = info_dict
# for index,(index_k,index_v) in enumerate(info_dict.items()):    #compareKey,data_info
#     for trans_type,single_info in index_v.items():  #{type:{source:trans}}
#         for single_part_info_k,single_part_info_v in single_info.items():    #{source:trans}
#             if single_part_info_k in info_dict_after[index_k][trans_type].keys():
#                 #未修改的字段
#                 if single_part_info_v.strip() == info_dict_after[index_k][trans_type][single_part_info_k].strip():
#                     # pass
#                     # info_dict_ori[index_k][trans_type].pop(single_part_info_k)
#                     info_dict_after[index_k][trans_type].pop(single_part_info_k)
#                     if info_dict_after[index_k][trans_type] == {}:
#                         info_dict_after[index_k].pop(trans_type)
#                     if info_dict_after[index_k] == {}:
#                         info_dict_after.pop(index_k)

#                 else:
#                     modify_info["Transcription"].append([index_k,trans_type,single_part_info_k])
#                     info_dict_after[index_k][trans_type].pop(single_part_info_k)


#             elif single_part_info_v in info_dict_after[index_k][trans_type].values():
#                 modify_info["TranscriptionSystem"].append([index_k,trans_type,single_part_info_k])
#                 del info_dict_after[index_k][trans_type][single_part_info_v]

#             else:
#                 modify_info["All_modify"].append([index_k,trans_type,single_part_info_k])



# print(info_dict_after)
# print(modify_info)


                # sys.exit()



                # print(single_part_info_k)
                # sys.exit()



# print(info_dict_after.keys())
# print(info_dict_after["b6c5cca8-d9ee-365b-aa6e-2d962bbdb242"]['Lexical'])