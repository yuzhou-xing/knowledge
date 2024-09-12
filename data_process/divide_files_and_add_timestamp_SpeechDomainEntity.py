########################################################
#generate transcription to tsv to verify
#python D:\v-yuhangxing\tool\first_week\BasicVerification\pre_precess\divide_files_and_add_timestamp_SpeechDomainEntity.py "D:\v-yuhangxing\data\SpeechDomainEntity_Testset_FY23\it-IT\Trans_0721_refinement\Medical\EntityTagging\BTest\transcript.txt" D:\v-yuhangxing\data\SpeechDomainEntity_Testset_FY23\it-IT\Trans_0721_refinement\Medical\lexical\BTest

import sys,os,json,re

data_type_flag = sys.argv[3]
prefix_end = sys.argv[4]
transcription_all = []


print('command:',sys.argv)
for trans_root,trans_der,trans_files in os.walk(sys.argv[1]):
    for trans_file in trans_files:
        if trans_file == 'transcript.txt' and data_type_flag.lower() in trans_root.split('\\')[-2].lower():
            # print(os.path.join(trans_root,trans_file))
            with open(os.path.join(trans_root,trans_file),'r',encoding='UTF8') as f_trans:
                for i, line in enumerate(f_trans):
                    f_name = os.path.splitext(line.split('\t')[0])[0]  #0YMW_ElQJxw_001
                    # s_name = re.sub('_\d{3}','',f_name).strip().replace('\ufeff','')
                    s_name = f_name.strip().replace('\ufeff','')[:-4]
                    # segmentid = re.findall('\d{3}',f_name)[-1].strip()
                    segmentid = f_name.strip().replace('\ufeff','')[-3:]
                    trans = line.split('\t')[1].strip()

                    # print(f_name,s_name,segmentid)

                    transcription_all.append([s_name,segmentid,trans])
print('trans utts:',len(transcription_all))  #as: [['Zir77AqgbI4', '044', 'أنا معك وهيدي كلمة كثير حلوة دكتور أكيد.'],[...]]
segments_num = 0
save_file,save_name = [],[]
for root,der,files in os.walk(sys.argv[1]):
    for file in files:
        if file.endswith('.json') and data_type_flag.lower() in root.split('\\')[-2].lower():
            # print(os.path.join(root,file))
            trans_list = []
            with open(os.path.join(root,file),'r',encoding='utf-8-sig') as fr:
                data = json.load(fr)
                try:
                    body = data["Result"][0]["Body"]
                    segments = body['Segments']
                except Exception as e:
                    print(e)
                    raise "long json file is not right format"
                segments_num += len(segments)
                for item in segments:
                    segment_id = item["SegmentID"]
                    speaker = item["speaker"]
                    start = item["Start"]
                    end = item["End"]
                    flag = len(transcription_all)
                    for i,single in enumerate(transcription_all):
                        if os.path.splitext(file)[0] == transcription_all[i][0] and segment_id == transcription_all[i][1]:
                            transcription_all[i][1] = '[{} {}] {}'.format(start,end,speaker)
                            save_file.append(transcription_all[i])
                            del transcription_all[i]
                            break
                    # if flag == len(transcription_all):
                    #     print('unfound utt:',item)

print('json utts:',segments_num)
if len(transcription_all):
    print('not found trans utts:',len(transcription_all))
    for i in transcription_all:
        print('not not found utts in',str(i)+'\n')
    #     locale = ''.join(re.findall('[a-z]{2}-[A-Z]{2}',sys.argv[1]))
    #     category = sys.argv[1].split('\\')[-4]
    #     B_or_D = sys.argv[1].split('\\')[-2]
    #     with open(r'E:\v-yuhangxing\data\FY23Q4_Speech_Domain_Entity_test_set\1205\{}_{}_{}.tsv'.format(locale,category,B_or_D),'a+',encoding='UTF8') as not_found:
    #         not_found.write(str(i)+'\n')
    # print('see not found utts in:',r'E:\v-yuhangxing\data\FY23Q4_Speech_Domain_Entity_test_set\1205\{}_{}_{}.tsv'.format(locale,category,B_or_D))

# print('s',len(save_file))
if not os.path.exists(sys.argv[2]):
    os.mkdir(sys.argv[2])
for i,s_line in enumerate(save_file):
    save_name.append(os.path.join(sys.argv[2],s_line[0]+'.'+prefix_end))
    with open(os.path.join(sys.argv[2],s_line[0]+'.'+prefix_end),'a+',encoding='utf8') as save:
        save.write(' '.join(s_line[1:])+'\n')



# print('tsv file:{}\nsaved_all_utts:{}\ntsv num:{}'.format(set(save_name),len(save_name),len(set(save_name))))
print('saved_all_utts:{}\ntsv num:{}'.format(len(save_name),len(set(save_name))))

# #mix version------gen trans.txt-->tsv
# python D:\v-yuhangxing\tool\first_week\BasicVerification\pre_precess\divide_files_and_add_timestamp_SpeechDomainEntity.py D:\v-yuhangxing\data\FY23Q4_Speech_Domain_Entity\de-DE\Trans_0818_refinement\Trans_0818_refinement\entity_verify D:\v-yuhangxing\data\FY23Q4_Speech_Domain_Entity\de-DE\Trans_0818_refinement\Trans_0818_refinement\all_Mixed_Domain\Btest Btest
# import sys,os,json,re
# transcription_all = {}
# for root,der,files in os.walk(sys.argv[1]):
#     for file in files:
#         if file.endswith('txt') and 'display' in root:# and root.split('\\')[-1].lower() == sys.argv[3].lower():
#             flag_type = root.split('\\')[-1].lower()
#             with open(os.path.join(root,file),'r',encoding='UTF8') as f_trans:
#                 for i, line in enumerate(f_trans):
#                     f_name = os.path.splitext(line.split('\t')[0])[0]  #0YMW_ElQJxw_001
#                     # s_name = re.sub('_\d{3}','',f_name).strip().replace('\ufeff','')
#                     s_name ='_'.join( f_name.split('_')[:-1]).strip().replace('\ufeff','')
#                     segmentid = re.findall('\d{3}',f_name)[-1].strip()
#                     trans = line.split('\t')[1].strip()

                    
#                     if flag_type not in transcription_all.keys():
#                         transcription_all[flag_type] = []
#                     transcription_all[flag_type].append([s_name,segmentid,trans])
# for i in transcription_all.keys():
#     print('{} trans utts {}'.format(i,len(transcription_all[i])))  #as: [['Zir77AqgbI4', '044', 'أنا معك وهيدي كلمة كثير حلوة دكتور أكيد.'],[...]]


# timestamp_diff_select = []
# segments_num = 0
# save_file,save_name = {},[]
# for root,der,files in os.walk(sys.argv[1]):
#     for file in files:
#         if file.endswith('.json') and 'display' in root:# and root.split('\\')[-1].lower() == sys.argv[3].lower():
#             trans_list = []
#             flag_diff_stamp = None
#             # print(os.path.join(root,file))
#             with open(os.path.join(root,file),'r',encoding='utf-8-sig') as fr:
#                 print(fr)
#                 data = json.load(fr)
#                 try:
#                     body = data["Result"][0]["Body"]
#                     segments = body['Segments']
#                 except Exception as e:
#                     print(e)
#                     raise "long json file is not right format"
#                 segments_num += len(segments)
#                 for item in segments:
#                     segment_id = item["SegmentID"].replace('\ufeff','')
#                     speaker = item["speaker"]
#                     start = item["Start"]
#                     end = item["End"]
#                     for i,(key_ind,single) in enumerate(transcription_all.items()):
#                         for index_del,single_per in enumerate(single):
#                             if os.path.splitext(file)[0] == single_per[0] and segment_id == single_per[1]:
#                                 single_per[1] = '[{} {}] {}'.format(start,end,speaker)
#                                 if key_ind not in save_file.keys():
#                                     save_file[key_ind] = []
#                                 save_file[key_ind].append(single_per)
#                                 del single[index_del]
#                                 break
#                         # break
#                     if not flag_diff_stamp:
#                         flag_diff_stamp = end
#                     else:
#                         if abs(float(start) - float(flag_diff_stamp)) > 10:
#                             # print('time stamp:',os.path.join(root,file),start,flag_diff_stamp,float(start) - float(flag_diff_stamp))
#                             timestamp_diff_select.append(float(start) - float(flag_diff_stamp))
#                         flag_diff_stamp = end

# print('json utts:',segments_num)
# if len(transcription_all.values()):
#     for i in transcription_all.values():
#         locale = re.findall('[a-z]{2}-[A-Z]{2}',sys.argv[1])[0]
#         with open(r'E:\v-yuhangxing\data\FY23Q4_Speech_Domain_Entity_test_set\2024\0312\en-US\{}_utts_notfound.tsv'.format(locale),'a+',encoding='UTF8') as not_found:
#             not_found.write(str(i)+'\n')
#     print('see not found utts in:',r'E:\v-yuhangxing\data\FY23Q4_Speech_Domain_Entity_test_set\2024\0312\en-US\{}_utts_notfound.tsv'.format(locale))
# # print('not found trans utts:',len(transcription_all.values()))

# print('s',save_file.keys())
# for i,(i_line,s_line) in enumerate(save_file.items()):
#     for value in s_line:
#         save_name.append(os.path.join(sys.argv[2],value[0]+'.tsv'))
#         if not os.path.exists(os.path.join(sys.argv[2],i_line)):
#             os.makedirs(os.path.join(sys.argv[2],i_line))
#         with open(os.path.join(sys.argv[2],i_line,value[0]+'.tsv'),'a+',encoding='utf8') as save:
#             save.write(' '.join(value[1:]) +'\n')

# # print('tsv file:{}\nsaved_all_utts:{}\ntsv num:{}'.format(set(save_name),len(save_name),len(set(save_name))))
# print('tsv file:{}\nsaved_all_utts:{}\ntsv num:{}'.format(len(set(save_name)),len(save_name),len(set(save_name))))
# print('time stamp grap >5:',len(timestamp_diff_select))
###################################################################################################################
#entity transcription.txt to carbon input
# import re,os,sys

# single_trans,transcription_line_count,wav_count,save_wav_count,catalog_type = [],0,[],[],{}
# for root,dir,files in os.walk(sys.argv[1]):
#     for file in files:
#         if file == 'transcript.txt':
#             count = 0
#             test_type = root.split('\\')[-1]
#             wav_path_part = os.path.join('\\'.join(root.split('\\')[:-2]),'lexical',test_type)
#             single_dict = {}
#             with open(os.path.join(root,file),'r',encoding='UTF8') as f_trans:
#                 for i,line in enumerate(f_trans):
#                     file_wav_name = '_'.join(os.path.splitext(line.split('\t')[0].strip())[0].split('_')[:-1]).replace('\ufeff','')

#                     # print(file_wav_name)
#                     if file_wav_name not in single_dict.keys():
#                         single_dict[file_wav_name] = line.split('\t')[1].strip()
#                     else:
#                         single_dict[file_wav_name] = '{} {}'.format(single_dict[file_wav_name],line.split('\t')[1].strip())

#                     if test_type not in catalog_type.keys():
#                         catalog_type[test_type] = []
#                     catalog_type[test_type].append(file_wav_name)


#                     count = i
#             for j,(key_ind,v_ind) in enumerate(single_dict.items()):
#                 if not os.path.exists(sys.argv[2]):
#                     os.mkdir(sys.argv[2])
#                 with open(os.path.join(sys.argv[2],'carbon_input_{}.txt'.format(test_type)),'a+',encoding='UTF8') as sav:
#                     sav.write('{}\t{}\n'.format(os.path.join(wav_path_part,key_ind+'.wav'),v_ind))
#                 with open(os.path.join(sys.argv[2],'carbon_input.txt'),'a+',encoding='UTF8') as sav:
#                     sav.write('{}\t{}\n'.format(os.path.join(wav_path_part,key_ind+'.wav'),v_ind))

#             save_wav_count.extend(single_dict.keys())

#         elif file.endswith('wav'):
#             wav_count.append(os.path.splitext(file)[0])


# print('浏览得到wav个数{}，保存wav个数{},浏览-保存={}，保存-浏览={}'.format(len(wav_count),len(save_wav_count),set(wav_count) - set(save_wav_count),set(save_wav_count) - set(wav_count)))
# print('Btest保存了:{}文件，{}行,Dtest保存了:{}文件，{}行'.format(len(set(catalog_type['BTest'])),len(catalog_type['BTest']),len(set(catalog_type['DTest'])),len(catalog_type['DTest'])))



######################################## new modify data ========================================
#entity transcription.txt to carbon input
# import re,os,sys

# def entity_trans_to_carbon_input(inputpath,outputpath):
#     single_trans,transcription_line_count,wav_count,save_wav_count,catalog_type = [],0,[],[],{}
#     for root,dir,files in os.walk(inputpath):
#         for file in files:
#             if file == 'transcript.txt':
#                 count = 0
#                 test_type = root.split('\\')[-1]
#                 wav_path_part = os.path.join('\\'.join(root.split('\\')[:-2]),'lexical',test_type)
#                 single_dict = {}
#                 # print(os.path.join(root,file))
#                 with open(os.path.join(root,file),'r',encoding='UTF8') as f_trans:
#                     for i,line in enumerate(f_trans):
#                         file_wav_name = '_'.join(os.path.splitext(line.split('\t')[0].strip())[0].split('_')[:-1]).replace('\ufeff','')
#                         seg_ID = os.path.splitext(line.split('\t')[0].strip())[0].split('_')[-1]

#                         # print(file_wav_name)
#                         # print(seg_ID)
#                         if file_wav_name not in single_dict.keys():
#                             single_dict[file_wav_name] = {int(seg_ID):line.split('\t')[1].strip()} #line.split('\t')[1].strip()
#                         elif int(seg_ID) not in single_dict[file_wav_name].keys():
#                             single_dict[file_wav_name][int(seg_ID)] = line.split('\t')[1].strip()
#                         else:
#                             print('segmentID 重复')

#                             # single_dict[file_wav_name] = '{} {}'.format(single_dict[file_wav_name],line.split('\t')[1].strip())
#                         # print(single_dict)

#                         if test_type not in catalog_type.keys():
#                             catalog_type[test_type] = []
#                         catalog_type[test_type].append(file_wav_name)

#                         count = i
#                 for j,(key_ind,v_ind) in enumerate(single_dict.items()):
#                     sav_single_trans = ''
#                     if not os.path.exists(outputpath):
#                         os.mkdir(outputpath)
                    
#                     # print(sorted(v_ind) ,'\n',[x for x in v_ind.keys()])
#                     if sorted(v_ind) != [x for x in v_ind.keys()]:
#                         print('original transcription file: segment ID disorder: {} {}\n乱序{}\t保存顺序{}\n'.format(test_type,key_ind,[x for x in v_ind.keys()],sorted(v_ind)))
#                     if diff_list(sorted(v_ind)):
#                         print('{}有缺省的segment ID'.format(os.path.join(root,key_ind)))
#                     for ind_k in sorted(v_ind):
#                         sav_single_trans = '{} {}'.format(sav_single_trans,v_ind[ind_k])

#                     if not os.path.exists(outputpath):
#                         os.mkdir(outputpath)

#                     with open(os.path.join(outputpath,'carbon_input_{}.txt'.format(test_type)),'a+',encoding='UTF8') as sav:
#                         sav.write('{}\t{}\n'.format(os.path.join(wav_path_part,key_ind+'.wav'),sav_single_trans.strip()))
#                     with open(os.path.join(outputpath,'carbon_input.txt'),'a+',encoding='UTF8') as sav:
#                         sav.write('{}\t{}\n'.format(os.path.join(wav_path_part,key_ind+'.wav'),sav_single_trans))

#                 save_wav_count.extend(single_dict.keys())

#             elif file.endswith('wav'):
#                 wav_count.append(os.path.splitext(file)[0])


#     print('浏览得到wav个数{}，保存wav个数{},浏览-保存={}，保存-浏览={}'.format(len(wav_count),len(save_wav_count),set(wav_count) - set(save_wav_count),set(save_wav_count) - set(wav_count)))
#     print('Btest保存了:{}文件，{}行,Dtest保存了:{}文件，{}行'.format(len(set(catalog_type['BTEST'])),len(catalog_type['BTEST']),len(set(catalog_type['DTEST'])),len(catalog_type['DTEST'])))

# def segID_sort():

#     return 
# def diff_list(input_list):
#     for order,con in enumerate(input_list):
#         if order < len(input_list) - 1:
#             if abs(int(con)-int(input_list[order+1])) != 1:
#                 print('ID',int(con),int(input_list[order+1]))
#                 return True
#     return False

# # def check_first_alpha_isupper_and_isLegelDot(filepath,line):
# #     EndFlag = ['.','?','!']
# #     content_list = line.split(' ')
# #     for i,word in enumerate(content_list):
# #         if i < len(content_list) - 1:
# #             for j,letter in enumerate(list(word)):
# #                 if len(set(EndFlag) - set(list(word))) != 3:
# #                     if len(set(EndFlag)-(set(EndFlag) - set(list(word)))) == 1 and word[-1] == set(EndFlag)-(set(EndFlag) - set(list(word))):   #need check type
                        
    

# entity_trans_to_carbon_input(sys.argv[1],sys.argv[2])



#=================================================================================================
#entity format pre
# import re,sys,os
# def read_trans_1011(p):
#     deal_l = ''
#     time_stamp = [0,0]
#     try:
#         with open (p,encoding="UTF-8-sig") as f:
#             lines = f.readlines()
#             # print(lines)
#     except Exception as e:
#         print("reading tsv file is bad",e) 
#     finally:
#         for l in lines:
#             s_time = 0
#             e_time = 0
#             sid = 0
#             trans_info = ''
#             s = l.strip()
#             if not s:
#                 continue
#             try:
#                 f_p,s_p = s.split(']',1)
#                 s_time,e_time = f_p.replace('[', '').split(' ')
#                 sid = s_p.strip().split(' ',1)[0]
#                 trans_info = s_p.strip().split(' ',1)[1]
#             except Exception as e:
#                 print("reading tsv file is bad",e) 
#                 print(os.path.basename(p),l)
#                 raise "reading tsv file is bad"
#             deal_l = '{} {}'.format(deal_l,trans_info)
#             if time_stamp != [0,0]:
#                 if s_time >= time_stamp[0] and e_time >= time_stamp[1]:
#                     time_stamp = [s_time,e_time]
#                 else:
#                     print('时间戳错误：',p, time_stamp,s_time,e_time)
#     return deal_l

# for root,der,files in os.walk(sys.argv[1]):
#     for file in files:
#         if file.endswith('tsv'):
#             trans = read_trans_1011(os.path.join(root,file))
#             if '\n' in trans:
#                 print(file)
#             if os.path.exists(os.path.join('\\'.join(root.split('\\')[:-1]),'wav',os.path.splitext(file)[0]+'.wav')):
#                 with open(sys.argv[2],'a+',encoding='UTF8') as sav:
#                     sav.write('{}\t{}\n'.format(os.path.join('\\'.join(root.split('\\')[:-1]),'wav',os.path.splitext(file)[0]+'.wav'),trans))
#             else:
#                 print('路径不存在：',os.path.join('\\'.join(root.split('\\')[:-1]),'wav',os.path.splitext(file)[0]+'.wav'))
# if __name__ == '__main__':
#     while(1):
#         print('select what you want to do in entity data verify:\n{}\n{}\n'.format('enter 1 to complete: entity transcription.txt to carbon input',
#                                                                                    'enter 2 to complete: mix version---generate trans.txt-->verify tsv'))
#         enter_in = input()
#         if int(enter_in) == 1:
#             entity_trans_to_carbon_input(inputpath,outputpath)
#             break
#         elif int(enter_in) == 2:
#             entity_generate_verify_tsv(inputpath,outputpath)
#             break
#         elif int(enter_in) == 0:
#             break

#=======================================new format| tsv _ wav=====================================================

# def read_trans_1011(p):
#     deal_l = []
#     trans_all = ''
#     try:
#         with open (p,encoding="UTF-8-sig") as f:
#             lines = f.readlines()
#             # print(lines)
#     except Exception as e:
#         print("reading tsv file is bad",e) 
#     finally:
#         for l in lines:
#             s_time = 0
#             e_time = 0
#             sid = 0
#             trans_info = ''
#             s = l.strip()
#             if not s:
#                 continue
#             try:
#                 f_p,s_p = s.split(']',1)
#                 s_time,e_time = f_p.replace('[', '').split(' ')
#                 sid = s_p.strip().split(' ',1)[0]
#                 trans_info = s_p.strip().split(' ',1)[1]
#             except Exception as e:
#                 print("reading tsv file is bad",e) 
#                 print(os.path.basename(p),l)
#                 raise "reading tsv file is bad"
#             if '\t' in trans_info:
#                 print('trans中包含tab:',p)
#             if '=' in trans_info:
#                 print('trans中包含=:',p)
#             trans_all = '{} {}'.format(trans_all,'[' + s_time +' '+ e_time + ']'+' '+trans_info)
#             # deal_l.append(f'{sid}\t{s_time}\t{e_time}\t{trans_info}')
#     # print(deal_l)
#     return trans_all

# def generate_carbon_input(inputpath,outputpath):
#     wav_list = []
#     tsv_info_list = {}

#     if not os.path.exists(os.path.dirname(outputpath)):
#         os.mkdir(os.path.dirname(outputpath))
#     for root,der,files in os.walk(inputpath):
#         for file in files:
#             if file.endswith('.tsv'):
#                 if os.path.splitext(file)[0].strip() not in tsv_info_list.keys():
#                     tsv_info_list[os.path.splitext(file)[0].strip()] = read_trans_1011(os.path.join(root,file))
#                 else:
#                     print('输入文件夹有相同名称的文件：',file)
#             if file.endswith('.wav'):
#                 wav_list.append(os.path.join(root,file))

#     if len(set(wav_list)) != len(wav_list):
#         print('输入文件夹有相同名称的文件wav：',len(set(wav_list)) , len(wav_list))
#     for i,wav_single in enumerate(wav_list):
#         if os.path.splitext(os.path.basename(wav_single))[0] in tsv_info_list.keys():
#             with open(outputpath,'a+',encoding='UTF8') as sav:
#                 sav.write('{}\t{}\n'.format(wav_single.strip(),tsv_info_list[os.path.splitext(os.path.basename(wav_single))[0]]))
#             del tsv_info_list[os.path.splitext(os.path.basename(wav_single))[0]]
#         else:
#             print('音频没有对应的tsv文件：',wav_single)
    
#     if len(tsv_info_list) != 0:
#         print('为找到对应音频的tsv:',tsv_info_list.keys())

# import sys,os 
# generate_carbon_input(sys.argv[1],sys.argv[2])



# ######################################## display data ========================================
# #entity transcription.txt to carbon input
# import re,os,sys

# def entity_display_trans_to_carbon_input(inputpath,outputpath):
#     single_trans,transcription_line_count,wav_count,save_wav_count,catalog_type = [],0,[],[],{}

#     for root,dir,files in os.walk(inputpath):
#         for file in files:
#             if file == 'transcript.txt':
#                 count = 0
#                 test_type = root.split('\\')[-1]
#                 if 'lexical' in root.lower():
#                     wav_path_part = os.path.join('\\'.join(root.split('\\')[:-2]),'lexical',test_type)
#                 elif 'display' in root.lower():
#                     wav_path_part = os.path.join('\\'.join(root.split('\\')[:-2]),'display',test_type)
#                 else:
#                     print('错误的规则')
#                     sys.exit()
#                 single_dict = {}
#                 # print(os.path.join(root,file))
#                 with open(os.path.join(root,file),'r',encoding='UTF8') as f_trans:
#                     for i,line in enumerate(f_trans):
#                         file_wav_name = '_'.join(os.path.splitext(line.split('\t')[0].strip())[0].split('_')[:-1]).replace('\ufeff','')
#                         seg_ID = os.path.splitext(line.split('\t')[0].strip())[0].split('_')[-1]
#                         # print(seg_ID,root)

#                         # print(file_wav_name)
#                         # print(seg_ID)
#                         if file_wav_name not in single_dict.keys():
#                             single_dict[file_wav_name] = {int(seg_ID):line.split('\t')[1].strip()} #line.split('\t')[1].strip()
#                         elif int(seg_ID) not in single_dict[file_wav_name].keys():
#                             single_dict[file_wav_name][int(seg_ID)] = line.split('\t')[1].strip()
#                         else:
#                             print('segmentID 重复')

#                             # single_dict[file_wav_name] = '{} {}'.format(single_dict[file_wav_name],line.split('\t')[1].strip())
#                         # print(single_dict)

#                         if test_type not in catalog_type.keys():
#                             catalog_type[test_type] = []
#                         catalog_type[test_type].append(file_wav_name)

#                         count = i
#                 for j,(key_ind,v_ind) in enumerate(single_dict.items()):
#                     sav_single_trans = ''
#                     if not os.path.exists(outputpath):
#                         os.mkdir(outputpath)
                    
#                     # print(sorted(v_ind) ,'\n',[x for x in v_ind.keys()])
#                     if sorted(v_ind) != [x for x in v_ind.keys()]:
#                         print('original transcription file: segment ID disorder: {} {}\n乱序{}\t保存顺序{}\n'.format(test_type,key_ind,[x for x in v_ind.keys()],sorted(v_ind)))
#                     if diff_list(sorted(v_ind)):
#                         print('{}有缺省的segment ID'.format(os.path.join(root,key_ind)))
#                     for ind_k in sorted(v_ind):
#                         sav_single_trans = '{} {}'.format(sav_single_trans,v_ind[ind_k])

#                     # if not os.path.exists(os.path.join(outputpath,'refine_input')):
#                     #     os.mkdir(os.path.join(outputpath,'refine_input'))


#                     with open(os.path.join(outputpath,'carbon_input_{}.txt'.format(test_type)),'a+',encoding='UTF8') as sav:
#                         sav.write('{}\t{}\n'.format(os.path.join(wav_path_part,key_ind+'.wav'),sav_single_trans.strip()))
#                     with open(os.path.join(outputpath,'carbon_input.txt'),'a+',encoding='UTF8') as sav:
#                         sav.write('{}\t{}\n'.format(os.path.join(wav_path_part,key_ind+'.wav'),sav_single_trans))

#                 save_wav_count.extend(single_dict.keys())

#             elif file.endswith('wav'):
#                 wav_count.append(os.path.splitext(file)[0])


#     print('浏览得到wav个数{}，保存wav个数{},浏览-保存={}，保存-浏览={}'.format(len(wav_count),len(save_wav_count),set(wav_count) - set(save_wav_count),set(save_wav_count) - set(wav_count)))
#     print('Btest保存了:{}文件，{}行,Dtest保存了:{}文件，{}行'.format(len(set(catalog_type['BTest'])),len(catalog_type['BTest']),len(set(catalog_type['DTest'])),len(catalog_type['DTest'])))

# def segID_sort():

#     return 
# def diff_list(input_list):
#     for order,con in enumerate(input_list):
#         if order < len(input_list) - 1:
#             if abs(int(con)-int(input_list[order+1])) != 1:
#                 print('ID',int(con),int(input_list[order+1]))
#                 return True
#     return False

# # def check_first_alpha_isupper_and_isLegelDot(filepath,line):
# #     EndFlag = ['.','?','!']
# #     content_list = line.split(' ')
# #     for i,word in enumerate(content_list):
# #         if i < len(content_list) - 1:
# #             for j,letter in enumerate(list(word)):
# #                 if len(set(EndFlag) - set(list(word))) != 3:
# #                     if len(set(EndFlag)-(set(EndFlag) - set(list(word)))) == 1 and word[-1] == set(EndFlag)-(set(EndFlag) - set(list(word))):   #need check type
                        
    

# entity_display_trans_to_carbon_input(sys.argv[1],sys.argv[2])



# #mix version------gen trans.txt-->tsv
# python D:\v-yuhangxing\tool\first_week\BasicVerification\pre_precess\divide_files_and_add_timestamp_SpeechDomainEntity.py D:\v-yuhangxing\data\FY23Q4_Speech_Domain_Entity\de-DE\Trans_0818_refinement\Trans_0818_refinement\entity_verify D:\v-yuhangxing\data\FY23Q4_Speech_Domain_Entity\de-DE\Trans_0818_refinement\Trans_0818_refinement\all_Mixed_Domain\Btest Btest
# import sys,os,json,re
# transcription_all = {}
# for root,der,files in os.walk(sys.argv[1]):
#     for file in files:
#         if file.endswith('txt'):# and root.split('\\')[-1].lower() == sys.argv[3].lower():
#             flag_type = root.split('\\')[-1].lower()
#             with open(os.path.join(root,file),'r',encoding='UTF8') as f_trans:
#                 for i, line in enumerate(f_trans):
#                     f_name = os.path.splitext(line.split('\t')[0])[0]  #0YMW_ElQJxw_001
#                     # s_name = re.sub('_\d{3}','',f_name).strip().replace('\ufeff','')
#                     s_name ='_'.join( f_name.split('_')[:-1]).strip().replace('\ufeff','')
#                     segmentid = re.findall('\d{3}',f_name)[-1].strip()
#                     trans = line.split('\t')[1].strip()

                    
#                     if flag_type not in transcription_all.keys():
#                         transcription_all[flag_type] = []
#                     transcription_all[flag_type].append([s_name,segmentid,trans])
# for i in transcription_all.keys():
#     print('{} trans utts {}'.format(i,len(transcription_all[i])))  #as: [['Zir77AqgbI4', '044', 'أنا معك وهيدي كلمة كثير حلوة دكتور أكيد.'],[...]]


# timestamp_diff_select = []
# segments_num = 0
# save_file,save_name = {},[]
# for root,der,files in os.walk(sys.argv[1]):
#     for file in files:
#         if file.endswith('.json'):# and root.split('\\')[-1].lower() == sys.argv[3].lower():
#             trans_list = []
#             flag_diff_stamp = None
#             # print(os.path.join(root,file))
#             with open(os.path.join(root,file),'r',encoding='utf-8-sig') as fr:
#                 data = json.load(fr)
#                 try:
#                     body = data["Result"][0]["Body"]
#                     segments = body['Segments']
#                 except Exception as e:
#                     print(e)
#                     raise "long json file is not right format"
#                 segments_num += len(segments)
#                 for item in segments:
#                     segment_id = item["SegmentID"].replace('\ufeff','')
#                     speaker = item["speaker"]
#                     start = item["Start"]
#                     end = item["End"]
#                     for i,(key_ind,single) in enumerate(transcription_all.items()):
#                         for index_del,single_per in enumerate(single):
#                             if os.path.splitext(file)[0] == single_per[0] and segment_id == single_per[1]:
#                                 single_per[1] = '[{} {}] {}'.format(start,end,speaker)
#                                 if key_ind not in save_file.keys():
#                                     save_file[key_ind] = []
#                                 save_file[key_ind].append(single_per)
#                                 del single[index_del]
#                                 break
#                         # break
#                     if not flag_diff_stamp:
#                         flag_diff_stamp = end
#                     else:
#                         if abs(float(start) - float(flag_diff_stamp)) > 10:
#                             # print('time stamp:',os.path.join(root,file),start,flag_diff_stamp,float(start) - float(flag_diff_stamp))
#                             timestamp_diff_select.append(float(start) - float(flag_diff_stamp))
#                         flag_diff_stamp = end

# print('json utts:',segments_num)
# if len(transcription_all.values()):
#     for i in transcription_all.values():
#         locale = re.findall('[a-z]{2}-[A-Z]{2}',sys.argv[1])[0]
#         with open(r'E:\v-yuhangxing\data\FY23Q4_Speech_Domain_Entity_test_set\2024\0206\{}_utts_notfound.tsv'.format(locale),'a+',encoding='UTF8') as not_found:
#             not_found.write(str(i)+'\n')
#     print('see not found utts in:',r'E:\v-yuhangxing\data\FY23Q4_Speech_Domain_Entity_test_set\2024\0206\{}_utts_notfound.tsv'.format(locale))
# # print('not found trans utts:',len(transcription_all.values()))

# print('s',save_file.keys())
# for i,(i_line,s_line) in enumerate(save_file.items()):
#     for value in s_line:
#         save_name.append(os.path.join(sys.argv[2],value[0]+'.tsv'))
#         if not os.path.exists(os.path.join(sys.argv[2],i_line)):
#             os.makedirs(os.path.join(sys.argv[2],i_line))
#         with open(os.path.join(sys.argv[2],i_line,value[0]+'.tsv'),'a+',encoding='utf8') as save:
#             save.write(' '.join(value[1:]) +'\n')

# # print('tsv file:{}\nsaved_all_utts:{}\ntsv num:{}'.format(set(save_name),len(save_name),len(set(save_name))))
# print('tsv file:{}\nsaved_all_utts:{}\ntsv num:{}'.format(len(set(save_name)),len(save_name),len(set(save_name))))
# print('time stamp grap >5:',len(timestamp_diff_select))