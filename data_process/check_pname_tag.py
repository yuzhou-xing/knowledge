# import os,sys,re


# def check_pname(filepath):
#     for root,der,files in os.walk(filepath):
#         pair = []
#         tag_all = set()
#         for file in files:
#             if file.endswith('tsv'):
#                 single_content = ''
#                 count = 0
#                 single_pair = 0
#                 with open(os.path.join(root,file),'r',encoding='UTF8') as f:
#                     # print(file)
#                     for i,line in enumerate(f):
#                         timestamp = re.findall('\[.*?\]',line.strip())
#                         timestamp = timestamp[0]

#                         trans = re.sub('S\d',' ',line.strip().split(']',1)[1].strip()).strip()
#                         if 'pname' in trans.lower(): # and len(re.findall('PName',trans)) == 0:

#                             trans_list = list(trans)
#                             # print(trans_list)
#                             for j,letter in enumerate(trans_list):
#                                 if '<' == letter and trans_list[j-1] != ' ':
#                                     trans_list.insert(j,' ')
#                                 if j != len(trans_list) -1:
#                                     if '>' == letter and trans_list[j+1] != ' ':
#                                         trans_list.insert(j+1,' ')
#                             # print(trans)
#                             # print(''.join(trans_list))
#                             single_content = single_content + ''.join(trans_list)
#                             all_tag = re.findall('<.*?>',trans)
#                             # print(len(all_tag))
#                             if all_tag:
#                                 if len(all_tag)%2 != 0:
#                                     print('不成对',file)
#                                 left_tag = 0
#                                 right_tag = 0
#                                 for tag in all_tag:
#                                     tag_all.add(tag)
#                                     if '<pname>' == tag.strip().lower():
#                                         left_tag += 1
#                                     if '</pname>' == tag.strip().lower():
#                                         right_tag += 1
#                                 if left_tag == right_tag:
#                                     single_pair += left_tag
#                                 else:
#                                     single_pair += min(left_tag,right_tag)
#                                     print(file,'left and right error')  
#                                     # with open()    
#                                 # print(single_pair)    
#                         else:
#                             single_content = single_content + trans
                
#                 pair.append([file,single_pair])
            
#             with open(os.path.join(sys.argv[2],root.split('\\')[-1]+'.tsv'),'a+',encoding='UTF8') as save:
#                 save.write('{}\t{}\n'.format(file,single_content))
#     # print(pair) 
#     # print(tag_all)   
#     for sin in pair:
#         # print(sin)
#         with open(os.path.join(sys.argv[2],sys.argv[3]+'_stat_info.tsv'),'a+',encoding='UTF8') as save_tsv:
#             save_tsv.write('{}\t{}\n'.format(sin[0],sin[1]))


# check_pname(sys.argv[1])

#         # trans_pro = list(trans_pro)
#         # for i,letter in enumerate(trans_pro):
#         #     if '[' == letter and trans_pro[i-1] != ' ':
#         #         trans_pro.insert(i,' ')
#         #     if i != len(trans_pro)-1:       #防止list index out of range
#         #         if ']' == letter and trans_pro[i+1] != ' ':
#         #             trans_pro.insert(i+1,' ')


#=================================================1127=======================================

import os,sys,re


def check_pname(filepath):
    empty_trans_set = set()
    tsv_file = 0
    count_all = 0
    file_divide = [[],[],[]]
    pair = []
    whole_line_tag = set()
    for root,der,files in os.walk(filepath):
        tag_all = set()
        for file in files:
            if file.endswith('tsv'):# and sys.argv[3] in root.split('\\')[-1]:
                #print(file)
                tsv_file += 1
                single_content = ''
                count = 0
                single_pair = 0
                #print(file)
                with open(os.path.join(root,file),'r',encoding='UTF8') as f:
                    #print(file)
                    for i,line in enumerate(f):
                        line = line.replace('\ufeff','')
                        if len(line.split(']',1)[1].strip().split(' ',1)) == 1:
                            # empty_trans_set.add(os.path.join(root,file))
                            empty_trans_set.add(file)
                            continue
                        if re.sub('<.*?>|\[.*?\]',' ',line.split(']',1)[1].strip().split(' ',1)[1]).strip() == '':
                            whole_line_tag.add(file)
                            # continue

                        # print('1',line.strip()[1])
                        if line.strip()[0] != '[':
                            print('时间戳格式错误',file)
                            print(line)

                        f_p,s_p = line.split(']',1)
                        s_time,e_time = f_p.replace('[', '').split(' ')
                        sid = s_p.strip().split(' ',1)[0]

                        # print(file)
                        # print(line)
                        trans_info = s_p.strip().split(' ',1)[1]

                        trans_info = '[{} {}] {}'.format(s_time,e_time,trans_info)

                        
                        timestamp = re.findall('\[.*?\]',line.strip())
                        timestamp = timestamp[0]

                        # trans = re.sub('S\d',' ',line.strip().split(']',1)[1].strip()).strip()
                        # print(file)
                        trans = line.split(']',1)[1].strip().split(' ',1)[1]
                        trans = '{} {}'.format(timestamp,trans)

                        if trans_info != trans:
                            print('trans不同',file)
                            # print(trans_info)
                            # print(trans)
                            # print(set(trans_info.split(' '))-set(trans.split(' ')))
                            sys.exit()

                        trans = trans_info
                        # repl_file = re.sub('<.*?>',' ',trans).strip()
                        # if re.sub('S\d',' ',repl_file).strip():
                        if 'pname' in trans.lower(): # and len(re.findall('PName',trans)) == 0:

                            trans_list = list(trans)

                            for j,letter in enumerate(trans_list):
                                if '<' == letter and trans_list[j-1] != ' ':
                                    trans_list.insert(j,' ')
                                if j != len(trans_list) -1:
                                    if '>' == letter and trans_list[j+1] != ' ':
                                        trans_list.insert(j+1,' ')

                            single_content = '{} {}'.format(single_content,''.join(trans_list))
                            all_tag = re.findall('<.*?>',trans)
                            if len(re.findall('<pname>',trans.lower())) == len(re.findall('</pname>',trans.lower())) and len(re.findall('<pname>',trans.lower())) == len(re.findall('<pname>.*?</pname>',trans.lower())):
                                count_all+=len(re.findall('<pname>',trans.lower()))
                            else:
                                print(file,'pname 不成对')

                            if all_tag:
                                if len(all_tag)%2 != 0:
                                    # print('不成对',file)
                                    pass
                                left_tag = 0
                                right_tag = 0
                                for tag in all_tag:
                                    tag_all.add(tag)
                                    if '<pname>' == tag.strip().lower():
                                        left_tag += 1
                                    if '</pname>' == tag.strip().lower():
                                        right_tag += 1
                                if left_tag == right_tag:
                                    single_pair += left_tag
                                else:
                                    single_pair += min(left_tag,right_tag)
                                    print(file,'left and right error')  
                                    # with open()    
                                # print(single_pair)    
                        else:
                            single_content = '{} {}'.format(single_content,trans)
                
                pair.append([file,single_pair])
            
                if os.path.splitext(file)[0].split('_')[-1].lower() == 'display':
                    with open(os.path.join(sys.argv[2],sys.argv[3]+'_display.tsv'),'a+',encoding='UTF8') as save:
                        # save.write('{}\t{}\n'.format(file,single_content))
                        save.write('{}\t{}\n'.format('_'.join(os.path.splitext(file)[0].split('_')[:-1]).replace('&','_')+'.wav',single_content))
                        file_divide[1].append(file)
                elif os.path.splitext(file)[0].split('_')[-1].lower() == 'lexical':
                    with open(os.path.join(sys.argv[2],sys.argv[3]+'_lexical.tsv'),'a+',encoding='UTF8') as save:
                        # save.write('{}\t{}\n'.format(file,single_content))
                        save.write('{}\t{}\n'.format('_'.join(os.path.splitext(file)[0].split('_')[:-1]).replace('&','_')+'.wav',single_content))
                        file_divide[0].append(file)
                else:
                    with open(os.path.join(sys.argv[2],sys.argv[3]+'_other.tsv'),'a+',encoding='UTF8') as save:
                        save.write('{}\t{}\n'.format(os.path.splitext(file)[0]+'.wav',single_content))
                    file_divide[2].append(file)


                # with open(os.path.join(sys.argv[2],root.split('\\')[-1]+'.tsv'),'a+',encoding='UTF8') as save:
                #     save.write('{}\t{}\n'.format(file,single_content))
                        
            # for order,con_i in enumerate(list(single_content)):
            #     if order < len(list(single_content)) -1:
            #         if con_i == '.' and list(single_content)[order+1].strip() != '':
            #             # print('{}\t{}'.format(file,con_i+list(single_content)[order+1].strip()))
            #             print('{}\t{}'.format(file,con_i+list(single_content)[order+1].strip()))
            # for order,con_i in enumerate(single_content.split(' ')):
            #     if order < len(single_content.split(' ')) -1:
            #         if '.' in con_i and list(single_content)[order+1].strip() != '':
            #             print('{}\t{}'.format(file,con_i+list(single_content)[order+1].strip()))
    # print(pair) 
    # print(tag_all)   
    print('检查{}个tsv'.format(tsv_file))
    print('trans为空的tsv:',empty_trans_set)
    print('trans为整行tag的tsv:',whole_line_tag)
    print('正则匹配pname tag 对',count_all)

    if len(empty_trans_set):
        for empty_trans_single in empty_trans_set:
            with open(os.path.join(sys.argv[2],sys.argv[3]+'_error_info.tsv'),'a+',encoding='UTF8') as sav_info:
                sav_info.write('{}\t{}\n'.format('trans为空',empty_trans_single))
    if len(whole_line_tag):
        for wholetag_single in whole_line_tag:
            with open(os.path.join(sys.argv[2],sys.argv[3]+'_error_info.tsv'),'a+',encoding='UTF8') as sav_info:
                sav_info.write('{}\t{}\n'.format('trans为tag',wholetag_single))

    if set(file_divide[0])-set(file_divide[1]) and set(file_divide[1]) - set(file_divide[0]):
        print('lexical 和 display保存的文件不完全相同',len(file_divide[0]),len(file_divide[1]))
    if file_divide[2]:
        print('有除了lexical 和 display外的其余文件',len(file_divide[2]))
    for sin in pair:
        # print(sin)
        with open(os.path.join(sys.argv[2],sys.argv[3]+'_stat_info.tsv'),'a+',encoding='UTF8') as save_tsv:
            save_tsv.write('{}\t{}\n'.format(sin[0],sin[1]))


check_pname(sys.argv[1])

        # trans_pro = list(trans_pro)
        # for i,letter in enumerate(trans_pro):
        #     if '[' == letter and trans_pro[i-1] != ' ':
        #         trans_pro.insert(i,' ')
        #     if i != len(trans_pro)-1:       #防止list index out of range
        #         if ']' == letter and trans_pro[i+1] != ' ':
        #             trans_pro.insert(i+1,' ')