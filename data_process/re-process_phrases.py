#=================================================1127=======================================

import os,sys,re,json

def re_process_phrases(inputpath,outputpath,change_list,cjk_locale):
    tsv_file = 0
    char_set,left_letter_set,right_letter_set = [[],[]],[[],[]],[[],[]]
    replaced_tag = []
    cjk_file = []
    modify_dict = {}
    modify_data_set_id = []
    if os.path.exists(change_list):
        with open(change_list,'r',encoding='UTF8') as f_r:
            for order,line_c in enumerate(f_r):
                datasetID_single,former,after = line_c.strip().split('\t')
                modify_dict[former] = after
                modify_data_set_id.append(datasetID_single)


    for root,der,files in os.walk(inputpath):
        for file in files:
            if file.endswith('tsv'):
                tsv_file += 1
                phrases_part = []
                single_tsv_info = {}
                single_tsv_pname_pair = 0
                single_save_content = []
                with open(os.path.join(root,file),'r',encoding='UTF8') as f:
                    for i,line in enumerate(f):
                        trans_combine = ''
                        ori_trans = trans = line.strip().replace('？',' ').replace(',',' ').replace('،',' ').replace('?',' ')
                        content_list = trans.split(' ')

                        #？,-ΔΘ،
                        #？:42d5ef30-a647-44e8-b739-e110a1617096
                        #,:05c63639-557e-4a7a-8bb8-c65469364272, 101fe7f9-1f70-47fc-b203-65064b7c3bca, 50ee835a-1a7c-4634-8b8b-6b1c9ddd2ea2, 6b2d1081-42aa-4f55-8101-ccdd1db5e4ca, 6f90cea3-a45d-44dc-9edc-ccf4f0b891f0, cbafb0b1-76e1-43e7-a814-36fc5d2af2ab, ccaecc8a-40e2-40ed-8350-46debc256252, d23b04ab-90bd-4449-9195-da2d47a1be96, dd5c8572-20da-43e2-aef0-7589c84a4e12, e184cf4c-87e9-472b-89b1-f7192cd5a160, ee2cd81a-dd6f-48aa-a6f7-8ea5abfc051a, eefefb71-fd04-4316-b8fe-e64537a70d18, 
                        #-: pass
                        #Δ:pass
                        #Θ:pass
                        #،:c0437ea6-3f79-4a7d-9e6a-63c471dc9b38
                            #d21e7ad6-1842-45fa-9837-2fbbc5c35ff8

                        # if '،' in trans:
                        #     print(file)

                        #cjk 数据, 这个也许还要改
                        #英文字母范围
                        pattern = re.compile("["
                            u"\U00000000-\U0000007F"  # ascii
                            u"\U000000A3"             # £
                            #u"\U00002010-\U00002027"  # 常用标点（破折号，一般标点符号，引号和撇号）
                                                "]+", flags=re.UNICODE)
                        
                        if os.path.splitext(file.replace('_Phrases.txt',''))[0] in cjk_locale and (not pattern.match(trans)):
                            trans = trans.replace(' ','')
                            content_list = [trans]
                            # print(file)
                            # sys.exit()
                        
                        #extract char
                        # print('line:',line,file)
                        for letter in list(line.strip()):
                            char_set[0].append(letter)
                        #print('1--------------------',line.strip(),file)
                        left_letter_set[0].append(line.strip()[0])
                        right_letter_set[0].append(line.strip()[-1])

                        # print('content_before_after: ',content_list)
                        #去掉文本中夹杂的tag: 根据是否cjk分离
                        for p_T_order,part_content in enumerate(content_list):
                            # print(part_content)
                            if re.findall('<.*?>',part_content):
                                for single_tag in re.findall('<.*?>',part_content):
                                    replaced_tag.append(single_tag)
                                if os.path.splitext(file.replace('_Phrases.txt',''))[0] in cjk_locale:
                                    content_list[p_T_order] = re.sub('<.*?>','',content_list[p_T_order])
                                    cjk_file.append(os.path.splitext(file.replace('_Phrases.txt',''))[0])
                                else:
                                    content_list[p_T_order] = re.sub('<.*?>',' ',content_list[p_T_order])
                        # print('content_split_after: ',content_list)

                        trans_combine = [x.strip() for x in content_list if x.strip()]
                        trans_combine = ' '.join(trans_combine)
                        # if trans != trans_combine:
                        #     print(trans,'\t',trans_combine,'\t',file)

                        #change A. B. C. -->ABC   N.B.An  --> NBA
                        # trans_list = [l_x for l_x in list(trans_combine) if l_x.strip()]
                        # print('trans_list:',trans_list)


                        if trans_combine.count('.')>1:
                            #上边refine过,最多点和字母间存在一个空格

                            trans_list = list(trans_combine)
                            # print('2.1',trans_list)


                            for j,letter in enumerate(trans_list):
                                if letter == '.' and trans_list[j-1].strip() != '':
                                    trans_list[j-1] = trans_list[j-1]+letter
                                    trans_list[j] = 'del_letter_*'
                                elif letter == '.' and trans_list[j-1].strip() == '':
                                    trans_list[j-2] = trans_list[j-2]+letter
                                    trans_list[j] = 'del_letter_*'
                                    trans_list[j-1] = 'del_letter_*'

                            trans_list = [x.strip() for x in trans_list if x.strip() != 'del_letter_*']

                            # print('3',trans_list)

                            #去掉 A. B. 中间的空格
                            # flag_part = []
                            # for j,letter in enumerate(trans_list):
                            #     if len(letter) > 1:
                            #         flag_part.append(j)
                            #     if letter == ''


                            trans_list_copy = trans_list
                            flag_combine = []
                            flag_content = ''

                            for j,letter in enumerate(trans_list):
                        
                                if len(letter) >1:
                                    if len(flag_combine) == 0 or abs(flag_combine[-1]-j) == 1:
                                        flag_combine.append(j)
                                    else:
                                        if len(flag_combine) > 1:
                                            for flag_index in flag_combine:
                                                flag_content ='{}{}'.format(flag_content,trans_list[flag_index][0].strip())
                                                trans_list[flag_index] = 'del_letter_*'
                                                # print('flag_content:',flag_content)
                                                # print(trans_list[flag_index][0],trans_list[flag_index])
                                                # sys.exit()
                                            trans_list[flag_combine[0]] = flag_content
                                            sys.exit()
                                        flag_combine = [j]
                                        flag_content = ''
                                if letter == '' and len(flag_combine) != 0 and abs(flag_combine[-1]-j) == 1:
                                    flag_combine.append(j)
                   
                                elif letter =='':
                                    trans_list[j] = ' '
                            # print('11',flag_combine,flag_content,trans_list)

                            if len(flag_combine) > 1:
                                if trans_list[flag_combine[-1]].strip() == '':
                                    trans_list[flag_combine[-1]] = ' '
                                    flag_combine = flag_combine[:-1]
                                    

                            if len(flag_combine) > 1:
                                for flag_index in flag_combine:
                                    if trans_list[flag_index].strip() != '':
                                        flag_content ='{}{}'.format(flag_content,trans_list[flag_index][0].strip())
                            
                                    # print('111111111',flag_content,trans_list[flag_index][0].strip())
                                    # print(trans_list[flag_index][0],trans_list[flag_index])
                                    # sys.exit()
                                    trans_list[flag_index] = 'del_letter_*'
                                trans_list[flag_combine[0]] = flag_content
                            # print(trans_list)

                            trans_list = [x for x in trans_list if x.strip() != 'del_letter_*']
                            trans_combine = ''.join(trans_list)
                            # print('5',trans_combine)

                        if trans_combine.strip():
                            if trans_combine.strip()[-1] == '.':
                                trans_combine = trans_combine[:-1]
                            if trans_combine.strip()[-1] == '-':
                                trans_combine = trans_combine[:-1]
                            if trans_combine.strip()[-1] == "'":
                                trans_combine = trans_combine[:-1]
                            
                            if '-' in trans_combine.strip():
                                print('-:',trans_combine,'\t',file)
                            if '.' in trans_combine.strip():
                                print('.:',trans_combine,'\t',file)

        
                            char_set[1].extend(list(trans_combine.strip()))
                            left_letter_set[1].append(trans_combine.strip()[0])
                            right_letter_set[1].append(trans_combine.strip()[-1])
                            
                        if trans_combine in modify_dict.keys():
                            temp_V = trans_combine
                            trans_combine = modify_dict[trans_combine]
                            modify_dict.pop(temp_V)
                            if os.path.splitext(file.replace('_Phrases.txt',''))[0] not in modify_data_set_id:
                                print('modify dataset id error:',file)
                        

                        single_save_content.append(trans_combine)



                        if ori_trans.strip() != trans_combine.strip():
                            with open(os.path.join('\\'.join(outputpath.split('\\')[:-1]),'summary_modify.txt'),'a+',encoding='UTF8') as sav_modify:
                                sav_modify.write('{}\t{}\t{}\n'.format(file.replace('_Phrases.txt',''),ori_trans.strip(),trans_combine.strip()))

                    # trans_combine = trans_combine.replace('.',' ').strip()
                    with open(os.path.join('\\'.join(outputpath.split('\\')[:-1]),'dot_risk.txt'),'a+',encoding='UTF8') as sav_f_dot:
                        with open(os.path.join(outputpath,file),'a+',encoding='UTF8') as sav_f:
                            for single_save_c in sorted(set(single_save_content)):
                                if single_save_c.strip():
                                    sav_f.write(single_save_c.strip()+'\n')
                                    if '.' in single_save_c.strip():
                                        sav_f_dot.write(file+'\t'+single_save_c.strip()+'\n')





                        #在最后的trans  再统计charset
    print('char_set:',''.join(sorted(set(char_set[0]))))
    print('left_letter_set:',''.join(sorted(set(left_letter_set[0]))))
    print('right_letter_set:',''.join(sorted(set(right_letter_set[0]))))

    print('char_set final:',''.join(sorted(set(char_set[1]))))
    print('left_letter_set final:',''.join(sorted(set(left_letter_set[1]))))
    print('right_letter_set final:',''.join(sorted(set(right_letter_set[1]))))
                        
    print('modify_dict_un_used:',modify_dict)


def remove_duplicate_space(input_T):
    if '  ' in input_T:
        input_T = remove_duplicate_space(input_T.replace('  ',' '))
    else:
        return(input_T)




    #                     wav_name,trans = line.strip().split('\t')

    #                     if re.findall('<PName>.*?</PName>',trans):
    #                         for single_pattern in re.findall('<PName>.*?</PName>',trans):
    #                             _,s_c = single_pattern.split('<PName>')
    #                             single_phrases,_ = s_c.split('</PName>')
    #                             phrases_part.append(single_phrases.strip())
    #                             if wav_name not in single_tsv_info.keys():
    #                                 single_tsv_info[wav_name] = 1
    #                             else:
    #                                 single_tsv_info[wav_name] += 1
    #                     if wav_name not in single_tsv_info.keys():
    #                         single_tsv_info[wav_name] = 0
    #                     single_tsv_pname_pair += single_tsv_info[wav_name]
    #                 if single_tsv_pname_pair == 0:
    #                     print(file,' PName 数目为0\n')
    #                     sys.exit()

    #                 with open(os.path.join(sav_ph_path,file.replace('_0_DatasetMeta.tsv','_Phrases.txt')),'a+',encoding='UTF8') as sav_ph:
    #                     for single_ph_word in sorted(set(phrases_part)):
    #                         sav_ph.write(single_ph_word+'\n')
    #                 with open(summery,'a+',encoding='UTF8') as sav_summery:
    #                     sav_summery.write(json.dumps({file.replace('_0_DatasetMeta.tsv',''):{'Pname pair count':single_tsv_pname_pair,'details':single_tsv_info}})+'\n')

    # print('检查{}个tsv'.format(tsv_file))

cjk_locale_list = ["210e8f05-b4b0-4b54-83d9-dbd054f9386d", "98752426-0849-441d-93d6-1696e2c8f861", "562284c1-9396-49df-ac45-40ada7dc6c98", "42d5ef30-a647-44e8-b739-e110a1617096", "734b5f4a-bb7c-4f36-8d5c-5766dac090e3", "0dcd16ca-ac60-402e-ad45-983426b3937e", "d16576e6-ad89-4878-b5f9-f7ff915c006d", "219f8c74-e591-4797-9d24-2362ad227ac8", "6baf849c-fd7f-4b65-868e-d81200a42160", "b1d486cd-5e0d-4e98-a9c9-6648874034db", "ja-JP_display_BTEST", "ja-JP_display_DTEST", "ja-JP_lexical_BTEST", "ja-JP_lexical_DTEST", "ko-KR_display_BTEST", "ko-KR_display_DTEST", "ko-KR_lexical_BTEST", "ko-KR_lexical_DTEST", "zh-CN_display_BTEST", "zh-CN_display_DTEST", "zh-CN_lexical_BTEST", "zh-CN_lexical_DTEST"]

re_process_phrases(sys.argv[1],sys.argv[2],sys.argv[3],cjk_locale_list)

# re_process_phrases(r"E:\v-yuhangxing\data\FY24Q2-IS-Flexible-Data-Collection-TX\Urgent_PName_Tagging\240426_extarct_content_from_PName\final_stage\re-process_for_originalformat\test\input",r"E:\v-yuhangxing\data\FY24Q2-IS-Flexible-Data-Collection-TX\Urgent_PName_Tagging\240426_extarct_content_from_PName\final_stage\re-process_for_originalformat\test\output",cjk_locale_list)
