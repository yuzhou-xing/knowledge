#=================================================1127=======================================
#lower format---------------------------------------------------------
# import os,sys,re,json


# def gain_pname(filepath,summery,sav_ph_path):
#     tsv_file = 0
#     for root,der,files in os.walk(filepath):
#         for file in files:
#             if file.endswith('tsv'):
#                 tsv_file += 1
#                 phrases_part = []
#                 single_tsv_info = {}
#                 single_tsv_pname_pair = 0
#                 with open(os.path.join(root,file),'r',encoding='UTF8') as f:
#                     for i,line in enumerate(f):
#                         line = line.replace('\ufeff','')
#                         wav_name,trans = line.strip().split('\t')

#                         if re.findall('<pname>.*?</pname>',trans.lower()):
#                             for single_pattern in re.findall('<pname>.*?</pname>',trans.lower()):
#                                 _,s_c = single_pattern.split('<pname>')
#                                 single_phrases,_ = s_c.split('</pname>')
#                                 phrases_part.append(single_phrases.strip())
#                                 if wav_name not in single_tsv_info.keys():
#                                     single_tsv_info[wav_name] = 1
#                                 else:
#                                     single_tsv_info[wav_name] += 1
#                         if wav_name not in single_tsv_info.keys():
#                             single_tsv_info[wav_name] = 0
#                         single_tsv_pname_pair += single_tsv_info[wav_name]
#                     if single_tsv_pname_pair == 0:
#                         print(file,' PName 数目为0\n')
#                         sys.exit()
#                     # print(single_tsv_pname_pair)
#                     # print(len(phrases_part))
#                     # print(len(set(phrases_part)))
#                     # print(set(phrases_part))
#                     # print(sorted(set(phrases_part)))
#                     # sys.exit()
#                     with open(os.path.join(sav_ph_path,file.replace('_0_DatasetMeta.tsv','_Phrases.txt')),'a+',encoding='UTF8') as sav_ph:
#                         for single_ph_word in sorted(set(phrases_part)):
#                             sav_ph.write(single_ph_word+'\n')
#                     with open(summery,'a+',encoding='UTF8') as sav_summery:
#                         sav_summery.write(json.dumps({file.replace('_0_DatasetMeta.tsv',''):{'Pname pair count':single_tsv_pname_pair,'details':single_tsv_info}})+'\n')

#     print('检查{}个tsv'.format(tsv_file))

# gain_pname(sys.argv[1],sys.argv[2],sys.argv[3])

#-----------------former format----------------------------------------------------------------------
import os,sys,re,json


def gain_pname(filepath,summery,sav_ph_path):
    tsv_file = 0
    empty_content_file = set()
    for root,der,files in os.walk(filepath):
        for file in files:
            if file.endswith('tsv'):
                tsv_file += 1
                phrases_part = []
                single_tsv_info = {}
                single_tsv_pname_pair = 0
                with open(os.path.join(root,file),'r',encoding='UTF8') as f:
                    for i,line in enumerate(f):
                        line = line.replace('\ufeff','')
                        #if 'ja-JP-piv8bj4dcak-9' in line:
                        #    continue
                        wav_name,trans = line.strip().split('\t')

                        if re.findall('<PName>.*?</PName>',trans):
                            print(wav_name)
                            for single_pattern in re.findall('<PName>.*?</PName>',trans):
                                print(wav_name,single_pattern)
                                try:
                                    _,s_c = single_pattern.split('<PName>')
                                except:
                                    continue
                                #_,s_c = single_pattern.split('<PName>')
                                single_phrases,_ = s_c.split('</PName>')
                                phrases_part.append(single_phrases.strip())
                                if not single_phrases.strip():
                                    empty_content_file.add(wav_name)
                                if wav_name not in single_tsv_info.keys():
                                    single_tsv_info[wav_name] = 1
                                else:
                                    single_tsv_info[wav_name] += 1
                        if wav_name not in single_tsv_info.keys():
                            single_tsv_info[wav_name] = 0
                        single_tsv_pname_pair += single_tsv_info[wav_name]
                    if single_tsv_pname_pair == 0:
                        print(file,' PName 数目为0\n')
                        sys.exit()
                    # print(single_tsv_pname_pair)
                    # print(len(phrases_part))
                    # print(len(set(phrases_part)))
                    # print(set(phrases_part))
                    # print(sorted(set(phrases_part)))
                    # sys.exit()
                    with open(os.path.join(sav_ph_path,file.replace('_0_DatasetMeta.tsv','_Phrases.txt')),'a+',encoding='UTF8') as sav_ph:
                        for single_ph_word in sorted(set(phrases_part)):
                            sav_ph.write(single_ph_word+'\n')
                    with open(summery,'a+',encoding='UTF8') as sav_summery:
                        sav_summery.write(json.dumps({file.replace('_0_DatasetMeta.tsv',''):{'Pname pair count':single_tsv_pname_pair,'details':single_tsv_info}})+'\n')

    print('检查{}个tsv'.format(tsv_file))
    print('empty content file:',empty_content_file)

gain_pname(sys.argv[1],sys.argv[2],sys.argv[3])

