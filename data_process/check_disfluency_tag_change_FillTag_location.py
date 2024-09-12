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


# def check_pname(filepath):
#     for root,der,files in os.walk(filepath):
#         pair = []
#         tag_all = set()
#         for file in files:
#             if file.endswith('tsv') and sys.argv[3] in root.split('\\')[-1]:
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
#                             single_content = '{} {}'.format(single_content,''.join(trans_list))
#                             all_tag = re.findall('<.*?>',trans)
#                             # print(len(all_tag))
#                             if all_tag:
#                                 if len(all_tag)%2 != 0:
#                                     # print('不成对',file)
#                                     pass
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
#                             single_content = '{} {}'.format(single_content,trans)
                
#                 pair.append([file,single_pair])
            
#             with open(os.path.join(sys.argv[2],root.split('\\')[-1]+'.tsv'),'a+',encoding='UTF8') as save:
#                 save.write('{}\t{}\n'.format(file,single_content))
#             for order,con_i in enumerate(list(single_content)):
#                 if order < len(list(single_content)) -1:
#                     if con_i == '.' and list(single_content)[order+1].strip() != '':
#                         # print('{}\t{}'.format(file,con_i+list(single_content)[order+1].strip()))
#                         print('{}\t{}'.format(file,con_i+list(single_content)[order+1].strip()))
#             # for order,con_i in enumerate(single_content.split(' ')):
#             #     if order < len(single_content.split(' ')) -1:
#             #         if '.' in con_i and list(single_content)[order+1].strip() != '':
#             #             print('{}\t{}'.format(file,con_i+list(single_content)[order+1].strip()))
#     # print(pair) 
#     # print(tag_all)   
#     for sin in pair:
#         # print(sin)
#         with open(os.path.join(sys.argv[2],sys.argv[3]+'_stat_info.tsv'),'a+',encoding='UTF8') as save_tsv:
#             save_tsv.write('{}\t{}\n'.format(sin[0],sin[1]))

def check_disfluency_tag_info(trans,file_AudioName):
    # print('ori_trans---',trans)
    disfluency_tag = ['<disfluency>','</disfluency>']
    real_pair = 0
    error_pair = []
    other_tag_info = []
    fill_in,fill_left,fill_right,fill_left_right,fill_in_real_count = 0,0,0,0,0
    fill_flag = [0,0]
    tags_pair = re.findall('<disfluency>.*?</disfluency>', trans)
    tags_pair_cap_low = re.findall('<disfluency>.*?</disfluency>', trans,re.IGNORECASE)
    if len(tags_pair) != len(tags_pair_cap_low):
        print('tag大小写问题！！！！！',file_AudioName)

    for con in tags_pair:
        if '<FILL/>' in con or '<FILL/>'.lower() in con:
            fill_in += 1
            fill_in_real_count += len(re.findall('<FILL/>',con,re.IGNORECASE))
            # if len(re.findall('<FILL/>',con,re.IGNORECASE)) > 1:
            #     # print(con)
        elif len(re.findall('<.*?>',con.replace('<disfluency>','').replace('</disfluency>',''))) != 0:
            other_tag_info.append(con)

    tag_left = re.findall('<disfluency>',trans)
    tag_right = re.findall('</disfluency>',trans)
    # print('{}\t{}\t{}'.format(len(tags_pair),len(tag_left),len(tag_right)))
    if len(tags_pair) == len(tag_left) and len(tags_pair) == len(tag_right):
        real_pair = len(tags_pair)
    else:
        real_pair = min(len(tags_pair),len(tag_left),len(tag_right))
        error_pair = [len(tags_pair),len(tag_left),len(tag_right)]
        print('disfluency tag 不成对：',error_pair,file_AudioName)
    Placeholder,tag_split_content = list_trans(trans)
    trans_split_content = tag_split_content.split(Placeholder)
    trans_split_content = [word for x in trans_split_content for word in x.strip().split(' ') if word != '']
    # print([word for x in trans_split_content for word in x.strip().split(' ') if word != ''])
    # trans_split_content = [x.strip() for x in trans_split_content if x.strip()]
    # print('empty---',trans_split_content)

    for order,word_content in enumerate(trans_split_content):
        if order != 0:
            if word_content.strip() ==  '<disfluency>':
                if '<FILL/>' == trans_split_content[order-1] or '<FILL/>'.lower() == trans_split_content[order-1]:
                    fill_flag[0] = 1
                    temp = trans_split_content[order-1]
                    trans_split_content[order-1] = word_content.strip()
                    trans_split_content[order] = temp
                    if trans_split_content[order+1] in ['<FILL/>','<FILL/>'.lower()]:
                        print('相同tag相连的错误',file_AudioName)
                        sys.exit()

        if order < len(trans_split_content)-1:
            if word_content.strip() ==  '</disfluency>':
                if '<FILL/>' == trans_split_content[order+1] or '<FILL/>'.lower() == trans_split_content[order+1]:
                    fill_flag[1] = 1
                    temp = trans_split_content[order+1]
                    trans_split_content[order+1] = word_content.strip()
                    trans_split_content[order] = temp
                    if trans_split_content[order-1] in ['<FILL/>','<FILL/>'.lower()]:
                        print('相同tag相连的错误',file_AudioName)
                        sys.exit()

                if fill_flag[0] == 1 and fill_flag[1] == 1:
                    fill_left_right += 1
                    fill_flag = [0,0]
                elif fill_flag[0] == 1 and fill_flag[1] == 0:
                    fill_left += 1
                    fill_flag = [0,0]
                elif fill_flag[0] == 0 and fill_flag[1] == 1:
                    fill_right += 1
                    fill_flag = [0,0]

    # print('final---',' '.join(trans_split_content))
    return real_pair,fill_in,fill_left,fill_right,fill_left_right,' '.join(trans_split_content)
    # print(real_pair,error_pair,fill_in,fill_left,fill_right,fill_left_right)
                
                    
    
    # disfluency_tag = ['<disfluency>','</disfluency>']


def list_trans(trans):
    flag = False   
    some_Placeholder = [',','!',';','#','@','&','*','^','+','?']
    for Placeholder in some_Placeholder:
        if Placeholder not in trans and ' ' in trans:
            trans_pro = trans.replace(' ',Placeholder)
            flag = True
            break
        else:
            trans_pro = trans

    trans_pro = list(trans_pro)

    for i,letter in enumerate(trans_pro):
        if '<' == letter and trans_pro[i-1] != ' ':
            trans_pro.insert(i,' ')
        if i != len(trans_pro)-1:       #防止list index out of range
            if '>' == letter and trans_pro[i+1] != ' ':
                trans_pro.insert(i+1,' ')
    if flag == True:
        return Placeholder,''.join(trans_pro)  #like: , | Be,these <NE:name> restr <NE> restr </NE> d,other </NE:name> supers,onic <NE> re </NE> very <FW:en> a <NE:name> </NE:name> <NE> re </NE> </FW:en> tools
    else:
        return False,''.join(trans_pro)


# with open(sys.argv[2],'a+',encoding='UTF8') as sav:
#     sav.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format('filename','disfluency_pair_count','fill_in_count','fill_left_count','fill_right_count','fill_left_right_count','fill_in_real_count'))

for root,der,files in os.walk(sys.argv[1]):
    for file in files:
        if file.endswith('tsv'):
            print(os.path.join(root,file))
            with open(sys.argv[2],'a+',encoding='UTF8') as sav:
                sav.write("\n"+file+"\n")
                sav.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format('filename','disfluency_pair_count','fill_in_count','fill_left_count','fill_right_count','fill_left_right_count'))
            real_pair_text,fill_in_text,fill_left_text,fill_right_text,fill_left_right_text = 0,0,0,0,0
            changedTrans = []
            recode_title = ''
            with open(os.path.join(root,file),'r',encoding='UTF8') as f:
                for i,line in enumerate(f):
                    # CompareKey,AudioFileName,unmark_trans,trans_line = line.strip().split('\t')
                    #if i == 0 and line.startswith('CompareKey'):
                    if i == 0 and line.strip() == "CompareKey	AudioFileName	Timestamp Trans	trans with disfluency tagging":
                        recode_title = "CompareKey	AudioFileName	Timestamp Trans	trans with disfluency tagging"
                        continue
                    elif i == 0:
                        print("错误的文件头",file)
                        sys.exit()
                    AudioFileName,unmark_trans,trans_line = line.strip().split('\t')
                    trans_line = trans_line   #'sad {} sd'.format(trans_line)
                    real_pair,fill_in,fill_left,fill_right,fill_left_right,changedTrans_line = check_disfluency_tag_info(trans_line,'{}_{}'.format(file,AudioFileName))
                    real_pair_text += real_pair
                    fill_in_text += fill_in
                    fill_left_text += fill_left
                    fill_right_text += fill_right
                    fill_left_right_text += fill_left_right
                    # fill_in_real_count_text += fill_in_real_count

                    CompareKey = ''
                    changedTrans.append('\t'.join([CompareKey,AudioFileName,unmark_trans,changedTrans_line]))

                    # changedTrans.append('\t'.join([AudioFileName,unmark_trans,changedTrans_line]))

                # with open(sys.argv[2],'a+',encoding='UTF8') as sav:
                #     sav.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(file,real_pair_text,fill_in_text,fill_left_text,fill_right_text,fill_left_right_text,fill_in_real_count_text))
                    with open(sys.argv[2],'a+',encoding='UTF8') as sav:
                        sav.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(AudioFileName,real_pair,fill_in,fill_left,fill_right,fill_left_right))
            with open(os.path.join(sys.argv[3],file),'a+',encoding='UTF8') as sav_trans:
                if recode_title != '':
                    sav_trans.write(recode_title+'\n')
                else:
                    print("错误的文件头")
                for single_trans in changedTrans:
                    sav_trans.write(single_trans+'\n')
                    




# check_pname(sys.argv[1])

        # trans_pro = list(trans_pro)
        # for i,letter in enumerate(trans_pro):
        #     if '[' == letter and trans_pro[i-1] != ' ':
        #         trans_pro.insert(i,' ')
        #     if i != len(trans_pro)-1:       #防止list index out of range
        #         if ']' == letter and trans_pro[i+1] != ' ':
        #             trans_pro.insert(i+1,' ')